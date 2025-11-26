from pydantic import BaseModel, EmailStr, Field

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class RegisterResponse(BaseModel):
    id: str
    email: str
    status: str
    
