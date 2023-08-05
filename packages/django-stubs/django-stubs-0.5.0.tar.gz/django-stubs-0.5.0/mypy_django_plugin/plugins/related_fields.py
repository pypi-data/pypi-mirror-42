from typing import Optional, cast

from mypy.checker import TypeChecker
from mypy.nodes import StrExpr, TypeInfo
from mypy.plugin import FunctionContext
from mypy.types import CallableType, Instance, Type

from mypy_django_plugin import helpers
from mypy_django_plugin.helpers import fill_typevars_with_any, reparametrize_with


def get_valid_to_value_or_none(ctx: FunctionContext) -> Optional[Instance]:
    api = cast(TypeChecker, ctx.api)
    if 'to' not in ctx.callee_arg_names:
        # shouldn't happen, invalid code
        api.msg.fail(f'to= parameter must be set for {ctx.context.callee.fullname}',
                     context=ctx.context)
        return None

    arg_type = ctx.arg_types[ctx.callee_arg_names.index('to')][0]
    if not isinstance(arg_type, CallableType):
        to_arg_expr = ctx.args[ctx.callee_arg_names.index('to')][0]
        if not isinstance(to_arg_expr, StrExpr):
            # not string, not supported
            return None
        try:
            model_fullname = helpers.get_model_fullname_from_string(to_arg_expr.value,
                                                                    all_modules=api.modules)
        except helpers.SelfReference:
            model_fullname = api.tscope.classes[-1].fullname()

        if model_fullname is None:
            return None
        model_info = helpers.lookup_fully_qualified_generic(model_fullname,
                                                            all_modules=api.modules)
        if model_info is None or not isinstance(model_info, TypeInfo):
            return None
        return Instance(model_info, [])

    referred_to_type = arg_type.ret_type
    if not isinstance(referred_to_type, Instance):
        return None
    if not referred_to_type.type.has_base(helpers.MODEL_CLASS_FULLNAME):
        ctx.api.msg.fail(f'to= parameter value must be '
                         f'a subclass of {helpers.MODEL_CLASS_FULLNAME}',
                         context=ctx.context)
        return None

    return referred_to_type


def extract_to_parameter_as_get_ret_type_for_related_field(ctx: FunctionContext) -> Type:
    try:
        referred_to_type = get_valid_to_value_or_none(ctx)
    except helpers.InvalidModelString as exc:
        ctx.api.fail(f'Invalid value for a to= parameter: {exc.model_string!r}', ctx.context)
        return fill_typevars_with_any(ctx.default_return_type)

    if referred_to_type is None:
        # couldn't extract to= value
        return fill_typevars_with_any(ctx.default_return_type)
    return reparametrize_with(ctx.default_return_type, [referred_to_type])
