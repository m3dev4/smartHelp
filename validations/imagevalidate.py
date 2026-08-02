# ======================================
# Script Python pour la validation des fichiers images
# ======================================
from PIL import Image, UnidentifiedImageError
from fastapi import HTTPException, UploadFile

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png"
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 Mo


def validate_image(image: UploadFile):

    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="L'image doit être au format JPG ou PNG."
        )

    content = image.file.read()

    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="L'image dépasse 5 Mo."
        )

    image.file.seek(0)

    try:
        Image.open(image.file).verify()
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail="Image invalide ou corrompue."
        )

    image.file.seek(0)