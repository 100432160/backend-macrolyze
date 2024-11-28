from pydantic import BaseModel, EmailStr
from uuid import UUID

# Esquema base
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Crear usuario
class UserCreate(UserBase):
    password: str

# Respuesta de usuario
class UserResponse(UserBase):
    id: UUID

    class Config:
        from_attributes = True

# Actualizar usuario
class UserUpdate(BaseModel):
    username: str = None  # Ahora se permite cambiar el username
    password: str = None  # Se permite cambiar la contraseña

# Login de usuario
class UserLogin(BaseModel):
    username: str
    password: str
