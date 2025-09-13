from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, token

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(token.router, tags=["authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the CTF Platform API"}
