from pydantic import BaseModel, ConfigDict, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    role: str = Field(default="buyer", pattern="^(buyer|seller)$", description="Роль 'buyer' or 'seller'")
    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str