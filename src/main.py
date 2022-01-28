import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
	return {"Hello": "World"}

uvicorn.run(app, host="localhost", port=8080)