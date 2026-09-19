from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import UserRepository
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.schemas.user import UserRegister, UserLogin, Token, UserResponse
from app.models.user import User


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, data: UserRegister) -> Token:
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        hashed_pwd = hash_password(data.password)
        user = await self.user_repo.create(email=data.email, password_hash=hashed_pwd)

        token_str = create_access_token({"sub": user.id, "email": user.email})
        return Token(
            access_token=token_str,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )

    async def login(self, data: UserLogin) -> Token:
        user = await self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        token_str = create_access_token({"sub": user.id, "email": user.email})
        return Token(
            access_token=token_str,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )
