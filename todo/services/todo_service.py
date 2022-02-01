import os
from traceback import print_tb
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
from pymongo import MongoClient
import json
from bson import json_util, ObjectId

#import motor.motor_asyncio

client = MongoClient('mongodb+srv://Kan:mk8cTFBpg7Vvg5W@gettingstarted.wb0qj.mongodb.net/GettingStarted?retryWrites=true&w=majority')
db = client.gettingStarted
toDoList = db.toDoList

def parse_json(data):
    return json.loads(json_util.dumps(data))

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ToDoModel(BaseModel):
    
    topic: str = Field(...)
    description: str = Field(...)
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    


class UpdateToDoModel(BaseModel):
    topic: str = Field(...)
    description: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


def create_todo(todo : UpdateToDoModel):
    todo = jsonable_encoder(todo)
    new_todo = toDoList.insert_one(todo)
    return {
            "status": "success",
            "id": str(new_todo.inserted_id)
        }

def read_todo(topic : Optional[str],description : Optional[str]):
    if(topic==None and description==None)  : cur =  toDoList.find()
    elif(topic!=None and description==None): cur =  toDoList.find({"topic" : topic})
    elif(topic==None and description!=None): cur =  toDoList.find({"description" : description})
    elif(topic!=None and description!=None): cur =  toDoList.find({"topic" : topic,"description" : description})
    find_list=parse_json(cur)
    for i in range(len(find_list)):
        find_list[i]["_id"]=find_list[i]["_id"]["$oid"]

    return find_list

def update_todo(id:str,todo : UpdateToDoModel):
    try:
         ObjectId(id)
    except:
         return [False,{"status": "failed"}]

    todo = jsonable_encoder(todo)
    updated_todo=toDoList.update_one({"_id": ObjectId(id)},{"$set" :{"topic": todo['topic'],"description":todo['description']}})

    if(updated_todo.matched_count>0):
        return [True,{"status": "success","id": id}]
    else:
        return [False,{"status": "failed"}]

def delete_todo(id:str):
    try:
         ObjectId(id)
    except:
         return [False,{"status": "failed"}]

    updated_todo=toDoList.delete_one({"_id": ObjectId(id)})

    if(updated_todo.deleted_count>0):
        return [True,{"status": "success","id": id}]
    else:
        return [False,{"status": "failed"}]

