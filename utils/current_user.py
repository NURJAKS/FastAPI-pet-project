from fastapi import Request, HTTPException, Depends
from utils.sessions import get_session
from db.database import get_db
from models.user import User

async def current_user(request: Request, db=Depends(get_db)):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = await get_session(session_id)
    if not session or "user_id" not in session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    user = db.query(User).filter(User.id == session["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
