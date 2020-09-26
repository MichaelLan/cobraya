from typing import List
from fastapi import APIRouter, Body, Query, Depends, HTTPException, status
from app.app.api import deps
from app.app import crud, models, schemas
from sqlalchemy.orm import Session

router = APIRouter()


# ----------------------------------------------------------------------
@router.get('/', response_model=List[schemas.UserInDB])
def read_users(db: Session = Depends(deps.get_db),
               skip: int = 0,
               limit: int = 100,
               current_user: models.User = Depends(deps.get_current_active_user)):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Unauthorized user')
    users = crud.user.get_multi(db=db, skip=skip, limit=limit)
    return users


# ----------------------------------------------------------------------
@router.post('/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    return crud.user.create_user(db=db, obj_in=user)


# ----------------------------------------------------------------------
@router.put('/{user_id}', response_model=schemas.User)
def update_user(user_id: str,
                user_in: schemas.UserUpdate,
                db: Session = Depends(deps.get_db),
                current_user: models.User = Depends(deps.get_current_active_user)):

    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="The user with this id doesn't exist")

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=404,
                            detail="You don't have sufficient "
                                   "permissions to modify another user")
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


# ----------------------------------------------------------------------
@router.delete('/{user_id}', response_model=schemas.User)
def delete_user(user_id: str, db: Session = Depends(deps.get_db)):
    return crud.user.remove(db=db, id=user_id)
