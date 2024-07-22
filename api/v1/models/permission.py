from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from api.v1.models.base import Base
from api.v1.models.base_model import BaseModel
from api.v1.models.base import role_permission_association
import uuid

class Permission(BaseModel, Base):
    __tablename__ = 'permissions'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)

    roles = relationship('Role', secondary=role_permission_association, back_populates='permissions')
