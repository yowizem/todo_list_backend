from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from pydantic import BaseModel

# documentation by me. the imported libraries is 
app = FastAPI()

class todo(BaseModel):
    title: str
    content: str
    # ratings: Optional[int]

todos = [{
    "id": 123,
    "title": "palatandaan na 1 ka",
    "content": "learning tobe the best"
},{
    "id": 1234,
    "title": "palatandaan na 2 ka",
    "content": "learning tobe the best1"
}]

def get_todo_id(id: int):
    for todo in todos:
        if todo["id"] == id:
            return todo
    
def find_todo_index(id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == id:
            return i

@app.get("/todos")
def get_all_todos():
    find_todo_index(1234)
    return{"todos": todos}

@app.get("/todos/{id}") 
def get_todos_byId(id: int, response: Response):

    my_todo = get_todo_id(id)

    if not my_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The id: {id} is not found in the database!")
    
    print(my_todo)
    return{"todo": my_todo}

@app.post("/todos", status_code=status.HTTP_201_CREATED)
def new_post(todos: todo):

    return{"todos": todos}

@app.put("/todos/{id}")
def update_todo(id: int, up_todo: todo):

    update = get_todo_id(id)

    update["title"] = up_todo.title
    update["content"] = up_todo.content

    return up_todo

@app.delete("/todos/{id}")
def delete_todo(id: int):

    delete_id = find_todo_index(id)

    if delete_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the id {id} is not in the database")

    todos.pop(delete_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

