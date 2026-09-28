from typing import Protocol, runtime_checkable


@runtime_checkable
class IApplicationInfoProvider(Protocol):
    def get_environment(self) -> str: ...

    def get_version(self) -> str: ...
