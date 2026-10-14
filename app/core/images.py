from fastapi import HTTPException, UploadFile

import cloudinary
import cloudinary.uploader

from app.core.config import settings

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_PHOTO_BYTES = 5 * 1024 * 1024


def _configure() -> None:
    if not (
        settings.cloudinary_cloud_name
        and settings.cloudinary_api_key
        and settings.cloudinary_api_secret
    ):
        raise HTTPException(status_code=500, detail="Image upload is not configured")

    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )


def _allowed(file: UploadFile) -> bool:
    if file.content_type in ALLOWED_IMAGE_TYPES:
        return True
    name = (file.filename or "").lower()
    return any(name.endswith(ext) for ext in ALLOWED_EXTENSIONS)


def upload_image(file: UploadFile) -> tuple[str, str]:
    _configure()

    if not _allowed(file):
        raise HTTPException(
            status_code=400,
            detail="Only jpeg, png, webp, and gif photos are allowed",
        )

    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size == 0:
        raise HTTPException(status_code=400, detail="Photo file is empty")
    if size > MAX_PHOTO_BYTES:
        raise HTTPException(status_code=400, detail="Each photo must be 5MB or smaller")

    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder="ecommerce/products",
            resource_type="image",
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=502, detail="Photo upload failed")

    return result["secure_url"], result["public_id"]


def delete_image(public_id: str) -> None:
    try:
        _configure()
        cloudinary.uploader.destroy(public_id, resource_type="image")
    except Exception:
        return
