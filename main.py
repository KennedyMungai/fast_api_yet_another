"""The entry point to the program"""
from fastapi import Depends, FastAPI, HTTPException, security, status
from sqlalchemy import orm

from schemas import UserRequest, UserResponse
from services import get_db, get_user_by_email

app = FastAPI()


@app.post("/api/v1/users")
async def register_user(_user: UserRequest, _db: orm.Session = Depends(get_db())):
    db_user = await get_user_by_email(_user.email, _db)

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The Email address provided is already in use")
