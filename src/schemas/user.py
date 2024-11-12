from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=24)


class UserSchema(UserBase):
    username: str = Field(min_length=3, max_length=50)


class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
