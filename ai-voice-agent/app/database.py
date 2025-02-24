# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.ai_virtual_agent
async def insert_interaction(intent):
    document = {"intent": intent}
    result = await db.interactions.insert_one(document)
    return str(result.inserted_id)
    