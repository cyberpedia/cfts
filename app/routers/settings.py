from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.get("/settings/public", response_model=schemas.PublicCTFSetting)
def read_public_settings(db: Session = Depends(get_db)):
    """
    Retrieve the public CTF settings.
    """
    return crud.get_settings(db)
