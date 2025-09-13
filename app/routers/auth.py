from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from datetime import timedelta

from .. import crud, security
from ..config import settings
from ..database import get_db

router = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get('/login/google')
async def login_google(request: Request):
    """
    Redirects the user to Google's authentication page.
    """
    redirect_uri = request.url_for('callback_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/callback/google')
async def callback_google(request: Request, db: Session = Depends(get_db)):
    """
    Handles the callback from Google after user authentication.
    """
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    
    # Get or create the user in the local database
    user = crud.get_or_create_oauth_user(db, user_info=user_info)
    
    crud.create_audit_log(
        db, action="user_login_oauth_success", user_id=user.id,
        details={"provider": "google"}
    )
    
    # Create a local JWT for the user
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Redirect to the frontend with the token
    # In a real app, this URL would come from your config
    frontend_url = f"http://localhost:8080/auth/callback?token={access_token}"
    return RedirectResponse(url=frontend_url)
