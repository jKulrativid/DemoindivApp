from fastapi import FastAPI, Query, HTTPException
import services.todo_service as todo_service
from typing import Optional
import json
from bson import json_util

from todo.cors import setup_cors

app = FastAPI()
setup_cors(app)

def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.get('/')
async def root():
	return {"Hello": "World"}

@app.post("/todo", status_code=201)
def create_todo(todo : todo_service.UpdateToDoModel):
    return todo_service.create_todo(todo)

@app.get("/todo")
def read_todo(uid : Optional[str] = Query(None), topic : Optional[str] = Query(None), description : Optional[str] = Query(None) ):
    return todo_service.read_todo(uid, topic,description)

@app.put("/todo")
def update_todo(todo : todo_service.UpdateToDoModel,id : str = Query(...)):
    update =  todo_service.update_todo(id,todo)
    if not update[0]:
         raise HTTPException(status_code=400 ,detail = "failed")
    else:
        return update[1]

@app.delete("/todo")
def delete_todo(id : str = Query(...)):
    delete =  todo_service.delete_todo(id)
    if not delete[0]:
         raise HTTPException(status_code=400 ,detail = "failed")
    else:
        return delete[1]
