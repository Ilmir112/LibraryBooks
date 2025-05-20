from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SReaders(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(..., description="Имя читателя")
    email: EmailStr = Field(..., description="Электронная почта читателя")


class SNewReader(BaseModel):
    name: Optional[str] = Field(..., description="Имя читателя")
    email: Optional[EmailStr] = Field(..., description="Электронная почта читателя")
