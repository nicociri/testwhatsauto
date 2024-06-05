from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Definición del modelo de datos
class Message(BaseModel):
    app: str
    sender: str
    message: str
    group_name: str
    phone: str

# Definición del endpoint POST
@app.post("/webhook")
async def receive_message(message: Message):
    # Aquí puedes procesar el mensaje como necesites
    try:
        # Por ejemplo, imprimir el mensaje recibido
        print(f"Mensaje de {message.sender}: {message.message} at {message.phone}")
        print (message)
        return {"reply": f"Hola {message.sender}!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
