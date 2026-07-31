from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def get_home():
    return {"message": "Welcome to the SmartHelp API!"}
