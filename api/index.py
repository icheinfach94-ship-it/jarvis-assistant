import os
import requests
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisierung des OpenAI Clients über Umgebungsvariablen
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "DEIN_OPENAI_KEY_HIER"))

NANOLEAF_IP = os.getenv("NANOLEAF_IP", "11.0.0.X") 
NANOLEAF_TOKEN = os.getenv("NANOLEAF_TOKEN", "DEIN_NANOLEAF_AUTH_TOKEN")

# --- HILFSFUNKTIONEN ---
def get_weather(location: str = "Stuttgart") -> str:
    try:
        url = f"https://wttr.in/{location}?format=3"
        response = requests.get(url, timeout=3)
        return response.text.strip() if response.status_code == 200 else "Wetterdaten nicht verfügbar."
    except Exception:
        return "Fehler beim Abrufen der Wetterdaten."

def get_unread_emails() -> list:
    return [
        {"absender": "Tony Stark", "betreff": "Mark 85 Rüstungs-Upgrade fertig"},
        {"absender": "Pepper Potts", "betreff": "Terminverschiebung Board-Meeting"}
    ]

def get_calendar_events() -> list:
    return [
        {"zeit": "14:00 Uhr", "titel": "Projektbesprechung Basis 44"},
        {"zeit": "18:30 Uhr", "titel": "Work-out & Labor-Wartung"}
    ]

def control_magnus_light(on: bool) -> bool:
    try:
        url = f"http://{NANOLEAF_IP}:16021/api/v1/{NANOLEAF_TOKEN}/state"
        data = {"on": {"value": on}}
        response = requests.put(url, json=data, timeout=2)
        return response.status_code == 204
    except Exception:
        return False

class CommandRequest(BaseModel):
    text: str

@app.post("/api/command")
async def handle_command(request: CommandRequest):
    befehl = request.text.lower().strip()
    
    # 1. DIREKTE HARDWARE-STEUERUNG
    if "magnus pro" in befehl or "schreibtisch" in befehl:
        if "stehhöhe" in befehl or "hoch" in befehl:
            return {"reply": "Ich initiiere das Hochfahren des Magnus Pro auf Stehhöhe, Sir.", "action": "magnus_stand"}
        elif "sitzhöhe" in befehl or "runter" in befehl:
            return {"reply": "Verstanden, fahre den Magnus Pro auf Sitzhöhe herunter.", "action": "magnus_sit"}
        elif "licht an" in befehl or "beleuchtung an" in befehl:
            if control_magnus_light(True):
                return {"reply": "Die Magnus Pro RGB-Matrix wurde aktiviert.", "action": "light_on"}
            return {"reply": "Sir, die Lichtsteuerung ist offline.", "action": "error"}
        elif "licht aus" in befehl:
            if control_magnus_light(False):
                return {"reply": "Schalte die Schreibtischbeleuchtung aus.", "action": "light_out"}
            return {"reply": "Sir, die Lichtsteuerung reagiert nicht.", "action": "error"}

    if "basis 44" in befehl:
        if "aktivieren" in befehl or "starten" in befehl:
            return {"reply": "System Basis 44 wird hochgefahren. Alle Relais stehen auf Autopilot.", "action": "basis_44_start"}
        elif "status" in befehl:
            return {"reply": "Basis 44 läuft stabil. Keine Unregelmäßigkeiten im System.", "action": "basis_44_status"}

    # 2. KI-GEHIRN (FUNCTIONS)
    tools = [
        {"type": "function", "function": {"name": "get_weather", "description": "Wetter abrufen", "parameters": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]}}},
        {"type": "function", "function": {"name": "get_unread_emails", "description": "Ungelesene E-Mails abrufen"}},
        {"type": "function", "function": {"name": "get_calendar_events", "description": "Heutige Termine abrufen"}}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist JARVIS aus Iron Man. Sprich fehlerfreies, elegantes, britisches Deutsch. Nenne den Nutzer 'Sir'."},
                {"role": "user", "content": befehl}
            ],
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages = [
                {"role": "system", "content": "Du bist JARVIS. Fasse die Daten für den Sir charmant zusammen."},
                {"role": "user", "content": befehl},
                response_message
            ]
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if function_name == "get_weather":
                    tool_output = get_weather(location=function_args.get("location", "Stuttgart"))
                elif function_name == "get_unread_emails":
                    tool_output = json.dumps(get_unread_emails())
                elif function_name == "get_calendar_events":
                    tool_output = json.dumps(get_calendar_events())
                else:
                    tool_output = "{}"

                messages.append({"tool_call_id": tool_call.id, "role": "tool", "name": function_name, "content": tool_output})
            
            final_response = client.chat.completions.create(model="gpt-4o", messages=messages)
            return {"reply": final_response.choices[0].message.content, "action": "none"}
        return {"reply": response_message.content, "action": "none"}
    except Exception as e:
        return {"reply": f"Sir, es gibt ein Problem mit meinem KI-Kern: {str(e)}", "action": "error"}