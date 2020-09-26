from typing import Any
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.app.api import deps
from app.app import models, schemas, crud
from app.app.core.config import settings
from app.app.core import security

router = APIRouter()


@router.post('/login/access-token', response_model=schemas.Token)
def login_access_token(db: Session = Depends(deps.get_db),
                       form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'access_token': security.create_access_token(user.id, access_token_expires),
        'token_type': 'bearer',
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


