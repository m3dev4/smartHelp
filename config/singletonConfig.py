from transformers import pipeline


class ModelSingleton:
    _instance = None
    _models = {}


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def get(self, model_name: str, model_task: str):
        key = (model_task, model_name)
        print(key)
        if key not in self._models:
            print(f"Init du model: {model_name} & son {model_task}")
            self._models[key] = pipeline(task=model_task, model=model_name)
        return self._models[key]
