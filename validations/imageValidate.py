# ======================================
# Script Python pour la validation des fichiers images
# ======================================
from fastapi import UploadFile, HTTPException

IMAGE_ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
]


MAX_FILE_SIZE = 1024 * 1024 * 10  # 10mb


def validate_image(file: UploadFile):
    if file.content_type not in IMAGE_ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Type de fichier image non supporté. Seul les fichiers JPEG & PNG sont acceptés",
        )

    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, detail="Le fichier ne peut pas depasser 10mb"
        )

    file.file.seek(0)
    return file
