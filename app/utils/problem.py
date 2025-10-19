from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi.responses import JSONResponse


def problem(
    status: int,
    title: str,
    detail: str,
    type_: str = "about:blank",
    extras: Optional[Dict[str, Any]] = None,
) -> JSONResponse:
    correlation_id = str(uuid4())
    payload: Dict[str, Any] = {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail,
        "correlation_id": correlation_id,
    }
    if extras:
        payload.update(extras)
    resp = JSONResponse(payload, status_code=status)
    resp.media_type = "application/problem+json"
    return resp
