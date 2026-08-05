from fastapi import FastAPI
from routes import ingestionsRoute
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",     
    "http://127.0.0.1:3000",     
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Allowed domains
    allow_credentials=True,         # Support cookies/authentication headers
    allow_methods=["*"],             # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],             # Allow all custom request headers
)

app.include_router(router=ingestionsRoute.router)


@app.get("/")
def get_home():
    return {"message": "Welcome to the SmartHelp API!"}
