from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from datetime import date
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings
from . import models
from .db import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

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
    conn = psycopg2.connect(host=settings.HOST, database=settings.DATABASE, user=settings.USER, password=settings.DB_PASSWORD, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was succesfull")
except Exception as error:
    print("Connection has failed :(")
    print("error: ", error)
    print(settings.model_dump())

@app.get("/sql")
def test_todo(db: Session = Depends(get_db)):
    todo = db.query(models.Post).all()
    return {"data": todo}

# getting all todos
@app.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todos():
    cursor.execute("SELECT * FROM todo") 
    todoss = cursor.fetchall()
    return{"todos": todoss}

# getting a specific todo by searching todo_id
@app.get("/todos/{id}", status_code=status.HTTP_200_OK) 
def get_todos_byId(id: int, response: Response):
    
    db_query = f"SELECT * from todo WHERE todo_id = {id}"
    cursor.execute(db_query)
    todo = cursor.fetchone()
    
    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The {id} is not found in the database")
    
    return{"todo": todo}

# posting a new todo, basically mag add ka lang ng sarili mong todo
@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(post: Post):

    db_query = "INSERT INTO todo (todo, content, is_done, is_collaborative) VALUES (%s, %s, %s , %s) RETURNING *"
    cursor.execute(db_query, (post.todo, post.content, post.is_done, post.is_collaborative))

    new_todo = cursor.fetchone()
    conn.commit()
    return{"todos": new_todo}

# updating about sa specific todo id number, mag throw lang ng http status kapag walang id na nahanap
@app.put("/todos/{id}", status_code=status.HTTP_201_CREATED)
def update_todo(id: int, post: Post):

    sql = f"UPDATE todo SET todo = %s, content = %s, is_done = %s, is_collaborative = %s WHERE todo_id = {id} RETURNING *"

    cursor.execute(sql, (post.todo, post.content, post.is_done, post.is_collaborative))
    todo = cursor.fetchone()

    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The {id} is not found in the database")
    conn.commit()
    return {"todo": post}

# deleting of todo lang
@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):

    query = f"DELETE FROM todo WHERE todo_id = {id}"
    todo = cursor.execute(query)

    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The {id} is not found in the database")
    
    conn.commit()

    return{"respone": "Success"}
