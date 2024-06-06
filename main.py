from fastapi import FastAPI, Form, HTTPException

app = FastAPI()

# Definición del endpoint POST
@app.post("/webhook")
async def receive_message(
    app: str = Form(...),
    sender: str = Form(...),
    message: str = Form(...),
    group_name: str = Form(None),
    phone: str = Form(None)
):
    # Aquí puedes procesar el mensaje como necesites
    try:
        # Por ejemplo, imprimir el mensaje recibido
        print(f"App: {app}, Sender: {sender}, Message: {message}, Group: {group_name}, Phone: {phone}")
        return {"reply": f"Hola {sender}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ejecutar con uvicorn para pruebas locales
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
