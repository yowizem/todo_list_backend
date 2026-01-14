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

class Create_todo(BaseModel):
    todo_id: int
    todo: str
    content: str
    is_done: bool
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

# getting all todos
@app.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todos(db: Session = Depends(get_db)):
    todo = db.query(models.Post).all()
    return {"data": todo}

# getting a specific todo by searching todo_id
@app.get("/todos/{id}", status_code=status.HTTP_200_OK) 
def get_todos_byId(id: int, response: Response, db: Session = Depends(get_db)):

    todo = db.query(models.Post).filter(models.Post.todo_id == id).first()
    
    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The {id} is not found in the database")
    
    return{"todo": todo}

# posting a new todo, basically mag add ka lang ng sarili mong todo
@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(post: Post, db: Session = Depends(get_db)):

    # kwargs type, kumbaga pang dynamiclangh para kung maraminhg imput, hindi na isa isa.
    new_todo = models.Post(**post.model_dump())

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return{"todos": new_todo}

# updating about sa specific todo id number, mag throw lang ng http status kapag walang id na nahanap
@app.put("/todos/{id}", status_code=status.HTTP_201_CREATED)
def update_todo(id: int, post: Post, db: Session = Depends(get_db)):

    todo_query = db.query(models.Post).filter(models.Post.todo_id == id)
    todo = todo_query.first()

    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The {id} is not found in the database")
    
    todo_query.update(post.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(todo)

    return {"todo": todo}

# deleting of todo lang
@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db)):

    # query = f"DELETE FROM todo WHERE todo_id = {id}"
    # todo = cursor.execute(query)

    todo_query = db.query(models.Post).filter(models.Post.todo_id == id)
    todo = todo_query.first()

    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The {id} is not found in the database")
    
    db.delete(todo)    
    db.commit()

    return{"respone": "Success"}
