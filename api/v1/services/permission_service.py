from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging
from api.v1.models.permission import Permission
from api.v1.schemas.permission import PermissionCreate, PermissionUpdate
from uuid import uuid4

def create_permission(db: Session, permission: PermissionCreate):
    try:
        db_permission = Permission(**permission.dict())
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission
    except Exception as e:
        logging.error(f"Failed to create permission: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def get_permissions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Permission).offset(skip).limit(limit).all()

def get_permission(db: Session, permission_id: str):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

def update_permission(db: Session, permission_id: str, permission: PermissionUpdate):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")

    db_permission.name = permission.name
    db_permission.description = permission.description
    db.commit()
    db.refresh(db_permission)
    return db_permission

def delete_permission(db: Session, permission_id: str):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(db_permission)
    db.commit()
    return db_permission
