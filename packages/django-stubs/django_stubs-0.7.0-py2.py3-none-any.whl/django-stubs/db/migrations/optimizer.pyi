from typing import Any, List, Optional

from django.db.migrations.operations.base import Operation

class MigrationOptimizer:
    def optimize(self, operations: List[Operation], app_label: str = ...) -> List[Operation]: ...
    def optimize_inner(self, operations: List[Operation], app_label: str = ...) -> List[Operation]: ...
