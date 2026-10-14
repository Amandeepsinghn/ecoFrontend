from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    user_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    user_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

class UserProfile(BaseModel):
    id: int
    user_name: str
    email: str
    credit: float | None
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)

class ProfileUpdate(BaseModel):
    user_name: str | None = Field(default=None, min_length=1)
    email: str | None = Field(default=None, min_length=1)
    current_password: str | None = None
    new_password: str | None = Field(default=None, min_length=1)
    