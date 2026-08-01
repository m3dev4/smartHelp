from fastapi import APIRouter, UploadFile, File
from validations.audioValidate import validate_audio
from utils.files_manager import save_file_temp
from services.whisperService import transcriber
from rag.rag import get_rag_response

router = APIRouter(prefix="/ingestions", tags=["Ingestions"])


@router.post("/support-ticket")
async def create_ingestion_from_support_ticket(file: UploadFile = File(...)):
    await validate_audio(file)
    temp_file_path = save_file_temp(file)
    transcription_result = transcriber(temp_file_path, return_timestamps=True)

    return {
        "transcription": transcription_result["text"],
        "policy_rule_applied": get_rag_response(transcription_result["text"]),
    }
