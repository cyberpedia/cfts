from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.routers import (
    users, token, challenges, teams, leaderboard, settings, 
    admin, notifications, auth as oauth_auth, dynamic_challenges
)
from .config import settings as app_settings
from .limiter import limiter

app = FastAPI()

# Add rate limiter state and middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Custom exception handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request, exc):
    from slowapi import _rate_limit_exceeded_handler
    return await _rate_limit_exceeded_handler(request, exc)

# Add session middleware for OAuthlib's state management
app.add_middleware(SessionMiddleware, secret_key=app_settings.SECRET_KEY)

origins = ["http://localhost", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(token.router, tags=["authentication"])
app.include_router(oauth_auth.router, prefix="/auth", tags=["authentication"])
app.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
app.include_router(dynamic_challenges.router, prefix="/dynamic-challenges", tags=["dynamic_challenges"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(settings.router, tags=["settings"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the CTF Platform API"}
