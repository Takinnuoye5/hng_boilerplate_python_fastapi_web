from fastapi import APIRouter, HTTPException, Request, Depends, status
from sqlalchemy.orm import Session
import logging
from typing import List
from pydantic import ValidationError
from api.db.database import get_db, Base, engine
from api.v1.models.permission import Permission
from api.v1.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse
from api.v1.services.permission_service import (
    create_permission,
    get_permissions,
    get_permission,
    update_permission,
    delete_permission,
)
from api.utils.dependencies import get_current_admin
from api.v1.models.user import User
from api.utils.json_response import JsonResponseDict  # Import the custom response class

Base.metadata.create_all(bind=engine)

class CustomException(HTTPException):
    """
    Custom error handling
    """
    def __init__(self, status_code: int, detail: dict):
        super().__init__(status_code=status_code, detail=detail)
        self.message = detail.get("message")
        self.success = detail.get("success")
        self.status_code = detail.get("status_code")

async def custom_exception_handler(request: Request, exc: CustomException):
    return JsonResponseDict(
        message=exc.message,
        data=None,
        error=exc.message,
        status_code=exc.status_code,
    )

router = APIRouter()

import traceback

@router.post("/permissions", tags=["Permissions"], response_model=PermissionResponse)
async def create_permission_endpoint(
    request: PermissionCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Create a new permission
    """
    try:
        new_permission = create_permission(db, request)
        return JsonResponseDict(
            message="Permission created successfully",
            data={
                "id": new_permission.id,
                "name": new_permission.name,
                "description": new_permission.description,
                "created_at": new_permission.created_at
            },
            status_code=status.HTTP_201_CREATED
        )
    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        if e.status_code == 400:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Invalid permission name or description format",
                    "success": False,
                    "status_code": 400,
                },
            )
        elif e.status_code == 409:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "Permission already exists",
                    "success": False,
                    "status_code": 409,
                },
            )
        else:
            raise CustomException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "An unexpected error occurred",
                    "success": False,
                    "status_code": 500,
                },
            )
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred",
                "success": False,
                "status_code": 500,
            },
        )


@router.get("/permissions", tags=["Permissions"], response_model=List[PermissionResponse])
async def read_permissions(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Get all permissions
    """
    permissions = get_permissions(db, skip=skip, limit=limit)
    return JsonResponseDict(
        message="Permissions fetched successfully",
        data=[{
            "id": permission.id,
            "name": permission.name,
            "description": permission.description,
            "created_at": permission.created_at
        } for permission in permissions],
        status_code=status.HTTP_200_OK
    )

@router.get("/permissions/{permission_id}", tags=["Permissions"], response_model=PermissionResponse)
async def read_permission(
    permission_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Get a specific permission
    """
    db_permission = get_permission(db, permission_id)
    if db_permission is None:
        raise CustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Permission not found",
                "success": False,
                "status_code": 404,
            },
        )
    return JsonResponseDict(
        message="Permission fetched successfully",
        data={
            "id": db_permission.id,
            "name": db_permission.name,
            "description": db_permission.description,
            "created_at": db_permission.created_at
        },
        status_code=status.HTTP_200_OK
    )

@router.put("/permissions/{permission_id}", tags=["Permissions"], response_model=PermissionResponse)
async def update_permission_endpoint(
    permission_id: str,
    request: PermissionUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Update a specific permission
    """
    try:
        updated_permission = update_permission(db, permission_id, request)
        return JsonResponseDict(
            message="Permission updated successfully",
            data={
                "id": updated_permission.id,
                "name": updated_permission.name,
                "description": updated_permission.description,
                "created_at": updated_permission.created_at
            },
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        if e.status_code == 404:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Permission not found",
                    "success": False,
                    "status_code": 404,
                },
            )
        else:
            raise CustomException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "An unexpected error occurred",
                    "success": False,
                    "status_code": 500,
                },
            )

@router.delete("/permissions/{permission_id}", tags=["Permissions"], response_model=PermissionResponse)
async def delete_permission_endpoint(
    permission_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Delete a specific permission
    """
    try:
        deleted_permission = delete_permission(db, permission_id)
        return JsonResponseDict(
            message="Permission deleted successfully",
            data={
                "id": deleted_permission.id,
                "name": deleted_permission.name,
                "description": deleted_permission.description,
                "created_at": deleted_permission.created_at
            },
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        if e.status_code == 404:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Permission not found",
                    "success": False,
                    "status_code": 404,
                },
            )
        else:
            raise CustomException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "An unexpected error occurred",
                    "success": False,
                    "status_code": 500,
                },
            )
