from typing import Annotated

from fastapi import Depends, Request
from mediatorx import Mediator


def get_mediator(request: Request) -> Mediator:
    return request.app.state.mediator


MediatorDependency = Annotated[Mediator, Depends(get_mediator)]
