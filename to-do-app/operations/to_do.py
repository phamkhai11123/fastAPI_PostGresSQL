import sys
sys.path.append('./')
from connection import db_session
from model.sql_model import ToDo
import decoders.todo as decode
#create a todo
def create_to_do(todo: str)->dict:
    try:
        req = ToDo(todo)
        db_session.add(req)
        db_session.commit()
        return {
            'status':"Oke",
            'message' : 'new todo added'
        }
    except Exception as e :
        return{
            'status':'error',
            'message':str(e)
        }
# get all to-do list
def get_all():
    try:
        res = db_session.query(ToDo).all()
        docs = decode.decode_todos(res)
        return{
            'status':'ok',
            'data':docs
        }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    
def get_one(_id:int):
    try:
        criteria = {'_id':_id}
        res = db_session.query(ToDo).filter_by(**criteria).one_or_none()
        if res is not None:
            record = decode.decode_todo(res)
            return {
                'status':'ok',
                'data':record
            }
        else:
            return {
                'status':'error',
                'message':f'Record with id {_id} do not exist'
            }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }

# update todo
def update_todo(_id:int , title:str ):
    try:
        criteria = {'_id':_id}
        res = db_session.query(ToDo).filter_by(**criteria).one_or_none()
        if res is not None:
            res.todo = title
            db_session.commit()
            return {
                'status':'ok',
                'data': 'Updated successfully'
            }
        else:
            return {
                'status':'error',
                'message':f'Record with id {_id} do not exist'
            }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
# delete todo
def delete_todo(_id:int):
    try:
        criteria = {'_id':_id}
        res = db_session.query(ToDo).filter_by(**criteria).one_or_none()
        if res is not None:
            db_session.delete(res)
            db_session.commit()
            return {
                'status':'ok',
                'data': 'Delete successfully'
            }
        else:
            return {
                'status':'error',
                'message':f'Record with id {_id} do not exist'
            }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
# print(res)
# res = update_todo(1,'Learn PHP')
# res = delete_todo(14)
# res = create_to_do("Learn AngularJS")
# print(res)