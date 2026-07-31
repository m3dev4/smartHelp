from config.singletonConfig import ModelSingleton
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("OPENAI_WHISPER_MODEL_NAME")


registered_model = ModelSingleton()
model = registered_model.get(model_task="automatic-speech-recognition", model_name=MODEL_NAME)
