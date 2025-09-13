from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, token, challenges, teams, leaderboard, settings, admin

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
app.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(settings.router, tags=["settings"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the CTF Platform API"}
