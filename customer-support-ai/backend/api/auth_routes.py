from fastapi import APIRouter, HTTPException

from backend.models.user import UserRegister, UserLogin, TokenResponse
from backend import database
from backend.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(user: UserRegister):
    if database.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    database.create_user(user.name, user.email, hashed)

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token, name=user.name, email=user.email)


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin):
    user = database.get_user_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user["email"]})
    return TokenResponse(access_token=token, name=user["name"], email=user["email"])
