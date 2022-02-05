db = db.getSiblingDB('gettingStarted');

db.createCollection('toDoList');

db.toDoList.insertMany([
	{
		topic: "First Topic",
		description: "Loren Ipsum"
	},
	{
		topic: "fix : solve todo_service pymongo cannot connect to todo_mongo",
		description: "no description"
	}
])