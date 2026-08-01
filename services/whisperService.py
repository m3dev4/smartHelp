from models.whisperModel import whisper_model


def transcriber(audio_path: str, return_timestamps=False):
    result = whisper_model(audio_path, return_timestamps=return_timestamps)
    return result
