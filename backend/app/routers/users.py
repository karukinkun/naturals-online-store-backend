# backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.users import create_user_with_default_payment_method
from app.db.database import SessionLocal
from app.deps.auth import CognitoUser, get_current_user
from app.schemas.users import UserCreateRequest, UserCreateResponse

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserCreateResponse, status_code=201)
def create_user(
    request: UserCreateRequest,
    current_user: CognitoUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user, default_payment_method = create_user_with_default_payment_method(
            db=db,
            data=request,
            cognito_sub=current_user.sub,
            email=current_user.email,
        )

        return {
            "id": user.id,
            "cognito_sub": user.cognito_sub,
            "email": user.email,
            "default_payment_method": default_payment_method.code,
        }

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="すでに登録済みのユーザーです",
        )
