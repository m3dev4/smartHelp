# ======================================
# Script Python pour la validation des fichiers audio
# ======================================
from fastapi import UploadFile, HTTPException

AUDIO_ALLOWED_TYPES = [
    "audio/mpeg",
    "audio/wav"
]

MAX_FILE_SIZE = 1024 * 1024 * 10 # 10mb

async def validate_audio(file: UploadFile):
    content = None
    if file and file.filename:
        if file.content_type not in AUDIO_ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Type de fichier audio non supporté. Seul les fichiers MP3 & WAV sont acceptés"
            )
    
        content = await file.read()
    if content and len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Le fichier ne peut pas depasser 10mb"
        )

        await file.seek(0)
        return file

    else:
        pass