from fastapi import APIRouter, Depends
from utils.current_user import current_user
from utils.permissions import require_role
from models.user import User

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/secret-admin")
async def admin_panel(user: User = Depends(require_role("admin"))):
    return {"message": "welcome admin", "email": user.email}
