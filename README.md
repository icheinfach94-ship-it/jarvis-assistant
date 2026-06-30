# 🤖 JARVIS Assistant

Ein sprachgesteuerter KI-Assistent inspiriert von Tony Starks JARVIS aus Iron Man.

## Features

✨ **Spracherkennung & -ausgabe** – Deutsche Sprachsteuerung mit natürlicher Antwort

✨ **KI-Integration** – Powered by OpenAI GPT-4o

✨ **Hardware-Steuerung** – Steuere deinen Magnus Pro Schreibtisch & Nanoleaf Leuchten

✨ **Progressive Web App** – Funktioniert offline und lässt sich wie eine native App installieren

✨ **Android-kompatibel** – Installierbar als Android-App

## 🚀 Quick Start

### Lokal starten

```bash
# Requirements installieren
pip install -r requirements.txt

# Environment-Variablen setzen
export OPENAI_API_KEY="your-key-here"
export NANOLEAF_IP="192.168.1.100"
export NANOLEAF_TOKEN="your-token-here"

# Server starten
uvicorn api.index:app --reload
```

Dann öffne http://localhost:8000

### Mit Vercel deployen

```bash
npm i -g vercel
vercel
```

Env-Variablen in Vercel Dashboard hinzufügen.

## 📱 Als Android-App installieren

### Option 1: PWA (Empfohlen – Schnell & Einfach)

1. Öffne die JARVIS-Website auf deinem Android-Handy
2. Tippe auf **Menu (⋮)** → **"Zum Startbildschirm hinzufügen"**
3. Fertig! 🎉

### Option 2: APK mit PWABuilder

1. Gehe zu https://www.pwabuilder.com
2. Gib deine Website-URL ein
3. Lade die APK herunter
4. Installiere sie auf deinem Android-Gerät

### Option 3: Native Android-App bauen

Für eine vollständige native App siehe `android/` Verzeichnis (kommend).

## 🗣️ Befehle

```
"Wie ist das Wetter in Stuttgart?"
"Zeige meine E-Mails"
"Was sind meine heutigen Termine?"
"Magnus Pro hochfahren"
"Schreibtisch Licht an"
"Basis 44 aktivieren"
```

## 🔧 Konfiguration

### Environment-Variablen

```env
OPENAI_API_KEY=sk-...
NANOLEAF_IP=192.168.1.100
NANOLEAF_TOKEN=auth-token
```

## 📚 API Endpoints

### POST /api/command

```json
{
  "text": "Was ist das Wetter?"
}
```

**Response:**

```json
{
  "reply": "Sir, in Stuttgart sind es angenehme 22 Grad...",
  "action": "none"
}
```

## 🛠️ Technologie Stack

- **Frontend**: HTML5, Web Speech API, Service Worker
- **Backend**: FastAPI, Python
- **KI**: OpenAI GPT-4o
- **Deployment**: Vercel
- **PWA**: Manifest.json

## 📄 Lizenz

MIT

## 🏗️ Roadmap

- [ ] Native Android App
- [ ] iOS-Unterstützung
- [ ] Offline-Modus für häufige Befehle
- [ ] Smart Home Integration (HomeKit, SmartThings)
- [ ] Voice Profile Recognition

---

*"Good morning, Sir."* 🤖