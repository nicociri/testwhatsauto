from fastapi import FastAPI, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from database import SessionLocal, init_db, Message

app = FastAPI()

# Inicializar la base de datos
init_db()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Definición del endpoint POST
@app.post("/webhook")
async def receive_message(
    app: str = Form(...),
    sender: str = Form(...),
    message: str = Form(...),
    group_name: str = Form(None),
    phone: str = Form(None)    
):
    
    try:
        timestamp = datetime.fromisoformat(timestamp)
        
        # Obtener el último mensaje del sender
        last_message = db.query(Message).filter(Message.sender == sender).order_by(desc(Message.timestamp)).first()
        
        if last_message:
            # Verificar la diferencia de tiempo
            timestamp = datetime.now().isoformat()
            time_diff = timestamp - last_message.timestamp
            if time_diff > timedelta(hours=1):
                # Borrar todo el historial del sender
                db.query(Message).filter(Message.sender == sender).delete()
                db.commit()
                return {"status": "reset", "message": "Tu última interacción fue hace más de una hora. Empezamos de nuevo?"}

            # Concatenar prevstatus y el mensaje del último registro
            prevstatus = f"{last_message.prevstatus or ''} {last_message.message}".strip()
        else:
            prevstatus = ""

        # Crear un nuevo mensaje y guardarlo en la base de datos
        db_message = Message(
            app=app,
            sender=sender,
            message=message,
            group_name=group_name,
            phone=phone,
            timestamp=timestamp,
            prevstatus=prevstatus
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        print(f"App: {app}, Sender: {sender}, Message: {message}, Group: {group_name}, Phone: {phone}, Timestamp: {timestamp}, PrevStatus: {prevstatus}")
        return {"status": "success", "message": "Message received"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ejecutar con uvicorn para pruebas locales
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
