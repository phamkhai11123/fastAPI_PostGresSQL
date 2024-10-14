from enum import auto
from typing import Optional,List
from fastapi import Depends, FastAPI,status,Response,HTTPException 
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import engine,SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

try: 
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='admin',cursor_factory=RealDictCursor)
    cursor = conn.cursor()        
    print("database connection was successfull")
except Exception as error:
    print("connecting to database failed")
    print("Error:" ,error)

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p
         
# def find_index_post(id):
#     for i,p in enumerate(my_post):
#         if p['id']== id:
#             return i

@app.get("/")
async def read_root():
    # await foo()
    return {"Hello": "Khai"}


@app.get("/posts",response_model=List[schemas.Post])
def get_post(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db:Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,publish)
    # VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(title=post.title,content=post.content,publish=post.publish)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.get("/posts/latest")
# def get_post_latest():
#     post = my_post[len(my_post)-1]
#     return {"data": post}

@app.get("/posts/{id}")
def get_post_by_id(id:int,db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() 
    if not post:
        raise HTTPException(detail=f"Post with id {id} doesn't exist",status_code = status.HTTP_404_NOT_FOUND)
        # return {"message":f"Post with id {id} doesn't exist"}
    return post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id:int,db:Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    
    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post doesn't exist")
    
    delete_post.delete(synchronize_session=False)
    db.commit()

@app.put("/posts/{id}")
def update_post_by_id(id:int,update_post:schemas.PostCreate,db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post doesn't exist")

    post_query.update(update_post.dict(),synchronize_session=False)
    # post_query.title = update_post.title
    # post_query.content = update_post.content
    db.commit()
    return post_query.first()
 
@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):

    #hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


