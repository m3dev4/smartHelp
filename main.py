from fastapi import FastAPI
import models.whisperModel

app = FastAPI()

@app.get("/")
def get_home():
    return {"message": "Welcome to the SmartHelp API!"}
