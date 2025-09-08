import os
import json
import random
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "guess_number_log.json")
os.makedirs(LOG_DIR, exist_ok=True)

games = {}
conversation_history = {}

def save_log():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, indent=2, ensure_ascii=False)

def start_new_game(user_id):
    number = random.randint(1, 100)
    games[user_id] = number
    conversation_history.setdefault(user_id, [])
    return "I have chosen a number between 1 and 100. Try to guess it!"

def check_guess(user_id, guess):
    secret = games.get(user_id)
    if secret is None:
        return "No active game. Start a new one with 'start'."
    if guess < secret:
        return "Too low! Try a higher number."
    elif guess > secret:
        return "Too high! Try a lower number."
    else:
        del games[user_id]
        return f"Correct! The number was {guess}. Send 'start' to play again."

@app.post("/guess")
async def guess_number(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "default_user")
    message = data.get("message", "").strip().lower()

    # Inicializar conversación si no existe
    conversation_history.setdefault(user_id, [])

    # Guardar mensaje del usuario
    conversation_history[user_id].append({
        "role": "user",
        "content": message,
        "timestamp": datetime.now().isoformat()
    })

    # Procesar juego
    if message == "start":
        response = start_new_game(user_id)
    elif message.isdigit():
        response = check_guess(user_id, int(message))
    else:
        response = "Send 'start' to begin a new game or guess a number between 1 and 100."

    # Guardar respuesta del asistente
    conversation_history[user_id].append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().isoformat()
    })

    save_log()
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
