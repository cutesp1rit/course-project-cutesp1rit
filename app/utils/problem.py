import json
from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi.responses import Response


def problem(
    status: int,
    title: str,
    detail: str,
    type_: str = "about:blank",
    extras: Optional[Dict[str, Any]] = None,
) -> Response:
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
    return Response(
        content=json.dumps(payload),
        status_code=status,
        media_type="application/problem+json",
    )
