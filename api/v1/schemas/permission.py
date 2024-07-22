from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PermissionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="The name of the permission")
    description: str = Field(..., min_length=1, max_length=100, description="The description of the permission")

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: str

    class Config:
        orm_mode = True

class PermissionsList(BaseModel):
    permissions: List[Permission]

    class Config:
        orm_mode = True

class PermissionResponse(BaseModel):
    id: str
    name: str
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        return cls(id=str(obj.id), name=obj.name, description=obj.description)
