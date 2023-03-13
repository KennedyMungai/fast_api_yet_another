"""The entry point to the program"""
from fastapi import FastAPI, Depends
from fastapi import security
from sqlalchemy import orm
from schemas import UserRequest, UserResponse
from services import get_db

app = FastAPI()


@app.post("/api/v1/users")
async def register_user(user: UserRequest, _db: orm.Session = Depends(get_db())):
    pass
