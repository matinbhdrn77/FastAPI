from typing import Dict, Optional, List
from fastapi import Body, FastAPI, status, HTTPException, Response, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .routers import post, user, auth
# Create database
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("connected")
        break
    except Exception as error:
        print(error)
        time.sleep(3)


@app.get("/")
async def root():
    return {"message": "Hello World!!!"}
