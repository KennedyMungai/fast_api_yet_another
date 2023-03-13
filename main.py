"""The entry point to the program"""
from fastapi import FastAPI
from fastapi import security
from sqlalchemy import orm

app = FastAPI()
