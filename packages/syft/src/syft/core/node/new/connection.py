# stdlib
from typing import Any

# relative
from .syft_object import SYFT_OBJECT_VERSION_1
from .syft_object import SyftObject


class NodeConnection(SyftObject):
    __canonical_name__ = "NodeConnection"
    __version__ = SYFT_OBJECT_VERSION_1

    def get_cache_key() -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{type(self).__name__}"

    @property
    def route(self) -> Any:
        # relative
        from .network_service import connection_to_route

        return connection_to_route(self)
