from transformers import pipeline
from openai import OpenAI
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()


class ModelSingleton:
    _instance = None
    _models = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get(self, model_name: str, model_task: str, provider):
        key = (model_task, model_name, provider)
        if key not in self._models:
            if provider == "local":
                self._models[key] = pipeline(task=model_task, model=model_name)
                return self._models[key]

            elif provider == "hf":
                self._models[key] = OpenAI(
                    base_url="https://router.huggingface.co/v1",
                    api_key=os.environ["HF_TOKEN"],
                )
        return self._models[key]
