from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from validations.audioValidate import validate_audio
from validations.imageValidate import validate_image
from utils.files_manager import save_file_temp
from utils.file_manager_img import save_file_temp_img
from services.whisperService import transcriber
from services.vitService import image_classifier
from rag.rag import get_rag_response

router = APIRouter(prefix="/ingestions", tags=["Ingestions"])


@router.post("/support-ticket")
async def create_ingestion_from_support_ticket(
    audio: UploadFile = File(...),
    image: UploadFile = File(...),
    description: str | None = Form(None),
):
    await validate_audio(audio)
    validate_image(image)
    audio_path = save_file_temp(audio)
    image_path = save_file_temp_img(image)

    audio_transcription = transcriber(audio_path)
    image_classification = image_classifier(image_path)

    rag_result = get_rag_response(audio_transcription["text"])

    return {
        "transcription": audio_transcription["text"],
        "defect_detected": image_classification,
        "policy_rule_applied": rag_result["message"],
        "diagnostic_status": rag_result["status"],
    }
