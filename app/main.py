from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import date
import random
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings

# documentation by me. the imported libraries is 
app = FastAPI()

# this is a model, kung baga ito ang susundan ng pag popost(blueprint)
class Post(BaseModel):
    todo: str
    content: str
    is_done: bool = False
    is_collaborative: Optional[bool]

class Create_todo(BaseModel):
    todo_id: int
    todo: str
    content: str
    is_done: bool
    is_collaborative: Optional[bool]
    created_at: str
    updated_at: str

# connection for the app to db

try:
    conn = psycopg2.connect(host=settings.HOST, database=settings.DATABASE, user=settings.USER, password=settings.PASSWORD, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was succesfull")
except Exception as error:
    print("Connection has failed :(")
    print("error: ", error)

    
# static data for testing(localstorage)
todos = [{
    "todo_id": 1,
    "todo": "Upskill",
    "content": "learning tobe the best",
    "is_done": False,
    "is_collaborative": None,
    "created_at": "2026-01-07",
    "updated_at": "2025-01-07"
},{
    "todo_id": 2,
    "todo": "Being the best",
    "content": "learning tobe the best",
    "is_done": False,
    "is_collaborative": None,
    "created_at": "2026-01-07",
    "updated_at": "2026-01-07"
}]

# function for a specific use
def get_todo_id(id: int):
    for todo in todos:
        if todo["todo_id"] == id:
            return todo
    
def find_todo_index(id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == id:
            return i
        
def date_now():
    today = date.today()
    return str(today)

def id_generator():
    id = random.randrange(0, 99999)
    return id

# ito na yung pinaka routing lang(URI type shi)

# getting all todos
@app.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todos():
    print(settings.HOST)
    return{"todos": todos}

# getting a specific todo by searching todo_id
@app.get("/todos/{id}") 
def get_todos_byId(id: int, response: Response):

    my_todo = get_todo_id(id)

    if not my_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The id: {id} is not found in the database!")
    
    # print(my_todo) -> para lang to sa debugging purposes
    return{"todo": my_todo}

# posting a new todo, basically mag add ka lang ng sarili mong todo
@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(post: Post):
    
    # converting the post to be a json format
    todo = post.model_dump()

    # this is the server side(hindi control ng user yung patungkol sa inout na ito)
    todo["todo_id"] = id_generator()
    todo["created_at"] = date_now()
    todo["updated_at"] = date_now()

    todos.append(todo)
    
    return{"todos": todo}

# updating about sa specific todo id number, mag throw lang ng http status kapag walang id na nahanap
@app.put("/todos/{id}", status_code=status.HTTP_201_CREATED)
def update_todo(id: int, up_todo: Post):

    update = get_todo_id(id)

    if not update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The id of {id} is not found on the database")

    update["todo"] = up_todo.todo
    update["content"] = up_todo.content
    update["is_done"] = up_todo.is_done
    update["is_collaborative"] = up_todo.is_collaborative
    update["updated_at"] = date_now()

    return {"todo": update}

# deleting of todo lang
@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):

    delete_id = find_todo_index(id)

    if delete_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the id {id} is not in the database")

    todos.pop(delete_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

