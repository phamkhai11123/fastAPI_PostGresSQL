from enum import auto
from typing import Optional,List
from fastapi import Depends, FastAPI,status,Response,HTTPException 
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import engine,get_db
from sqlalchemy.orm import Session
from .router import post,user,auth

models.Base.metadata.create_all(bind=engine)



app = FastAPI()



try: 
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='admin',cursor_factory=RealDictCursor)
    cursor = conn.cursor()        
    print("database connection was successfull")
except Exception as error:
    print("connecting to database failed")
    print("Error:" ,error)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
@app.get("/")
async def read_root():
    # await foo()
    return {"Hello": "Khai"}



 
