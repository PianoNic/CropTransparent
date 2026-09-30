from fastapi import Request
from mediatorx import Mediator


def get_mediator(request: Request) -> Mediator:
    return request.app.state.mediator
