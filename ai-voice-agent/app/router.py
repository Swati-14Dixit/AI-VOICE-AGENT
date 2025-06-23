# app/router.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.intents import recognize_intent
from app.database import insert_interaction

router = APIRouter()
class InputText(BaseModel):
    text: str


@router.post("/process/")
async def process_input(data: InputText):
    intent = recognize_intent(data.text)
    await insert_interaction(intent)  # Save interaction to the database
    return {"intent": intent}
   
