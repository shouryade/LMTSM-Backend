from fastapi import Depends, APIRouter, HTTPException, status, Form, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from config.db import collection as user_collection
from models.register import registerUser
from utils import get_current_user
from typing import List, Annotated
from datetime import date
import pydantic
from bson import ObjectId


router = APIRouter(prefix="/v1/admin", tags=["roles"])


@router.get("/roles")
async def get_roles(
    current_user: registerUser = Depends(get_current_user),
):
    if current_user["role"] != "super_admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    results = user_collection.find({"des": "staff"})

    res = []

    for result in results:
        result["_id"] = str(result["_id"])
        res.append(result)

    return res


@router.put("/approve/{id}")
async def approve_roles(
    id: str,
    role: str,
    current_user: registerUser = Depends(get_current_user),
):
    if current_user["role"] != "super_admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    if role not in {"super_admin", "admin"}:
        raise HTTPException(status_code=406, detail="Select a valid role")

    result = user_collection.update_one({"_id": ObjectId(id)}, {"$set": {"role": role}})

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="The role is already assigned to the user."
        )
    return {"success": True, "message": "Role updated successfully!"}


@router.delete("/approve/{id}")
async def revoke_role(
    id: str,
    role: str,
    current_user: registerUser = Depends(get_current_user),
):
    if current_user["role"] != "super_admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    result = user_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": {"role": "user"}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found!")
    return {"success": True, "message": "Role revoked"}
