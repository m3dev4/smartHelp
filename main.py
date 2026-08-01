from fastapi import FastAPI
from routes import ingestionsRoute

app = FastAPI()

app.include_router(router=ingestionsRoute.router)


@app.get("/")
def get_home():
    return {"message": "Welcome to the SmartHelp API!"}
