from fastapi import Depends, HTTPException
from utils.current_user import current_user
from models.user import User

def require_role(role: str):
    def wrapper(user: User = Depends(current_user)):
        if user.role != role:
            raise HTTPException(403, "Forbidden: requires role " + role)
        return user
    return wrapper
