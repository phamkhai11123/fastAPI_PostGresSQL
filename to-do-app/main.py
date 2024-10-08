from fastapi import FastAPI
from routes.todo import todo_route

app = FastAPI()

app.include_router(todo_route)


# create virtual environment
# python -m venv env
# .\env\Scripts\activate