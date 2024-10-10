from fastapi import FastAPI,status,HTTPException
from database import SessionLocal
from pydantic import BaseModel
import models

app = FastAPI()
db = SessionLocal()

class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True

class User(OurBaseModel):
    id:int
    name:str
    email:str
    password:str

@app.get('/',response_model=list[User],status_code=status.HTTP_200_OK)
def getAll_User():
    getAll_User = db.query(models.User).all()
    return getAll_User

@app.get('/getUserById/{user_id}', status_code =status.HTTP_200_OK)
def getUser_by_id(user_id:int):
    find_User = db.query(models.User).filter(models.User.id == user_id).first()
    if find_User is not None:
        return find_User
    raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE,detail="User is not found")

@app.post('/addUser',response_model=User,status_code=status.HTTP_200_OK)
def addUser(user : User):
    newUser = models.User(
        id = user.id,
        name = user.name,
        email = user.email,
        password = user.password
    )
    find_User = db.query(models.User).filter(models.User.id == user.id).first()
    if find_User is not None:
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE,detail="User exists")
    db.add(newUser)
    db.commit()
    return newUser

@app.put('/update_user/{user_id}',response_model=User,status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id:int,user:User):
    find_user = db.query(models.User).filter(models.User.id == user_id).first()
    if find_user is not None:
        find_user.id = user.id
        find_user.name = user.name
        find_user.email = user.email
        find_user.password = user.password

        db.commit()
        return find_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User is not found")

@app.delete("/deleteUser/{user_id}",response_model=User,status_code=200)
def deleteUser(user_id:int):
    find_user = db.query(models.User).filter(models.User.id == user_id).first()
    if find_user is not None:
        db.delete(find_user)
        db.commit()
        return find_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User to delete is not found")