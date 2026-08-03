from config.singletonConfig import ModelSingleton
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("GOOGLE_VIT_BASE_PATCHED_MODEL_NAME")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER_HF")

registered_model = ModelSingleton()
google_vit_model = registered_model.get(
    model_task="Image-Text-to-Text", model_name=MODEL_NAME, provider=MODEL_PROVIDER
)
