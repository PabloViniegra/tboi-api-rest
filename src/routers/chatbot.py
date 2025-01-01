from fastapi import APIRouter, HTTPException
from src.schemas.schemas import Message, ChatRequest
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise Exception("No OpenAI API key found. Add it to a .env file as OPEN_API_KEY.")

client = OpenAI(api_key=OPENAI_KEY)

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Soy un asistente especializado en responder preguntas relacionadas exclusivamente con "
        "el videojuego 'The Binding of Isaac: Repentance'. Mis respuestas serán claras, concisas "
        "y enfocadas en proporcionar información útil a los jugadores sobre mecánicas, objetos, "
        "enemigos, secretos, personajes y cualquier otro aspecto del juego. Respondo siempre con cortesía, "
        "sin extenderme demasiado, para evitar abrumar al usuario."
    ),
}

@router.post("", response_model=Message)
async def chat_with_gpt(chat_request: ChatRequest):
    try:
        messages = [SYSTEM_PROMPT] + [message.dict() for message in chat_request.messages]
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
        )
        response_text = chat_completion.choices[0].message.content
        return Message(role="assistant", content=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interacting with OpenAI API: {str(e)}")
