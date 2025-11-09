from fastapi import APIRouter, File, UploadFile

from app.services.upload import secure_save
from app.utils.problem import problem

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("")
async def upload_image(file: UploadFile = File(...)):
    data = await file.read()
    try:
        path = secure_save("var/uploads", data)
        return {"ok": True, "path": path}
    except ValueError as e:
        code = str(e)
        if code == "too_big":
            return problem(
                413, "Payload Too Large", "body too big", extras={"code": code}
            )
        return problem(400, "Bad Request", code, extras={"code": code})
