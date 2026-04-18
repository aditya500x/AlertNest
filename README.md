# 🛡️ AlertNest: Integrated Emergency Response MVP

A robust, hackathon-ready emergency notification and response system. 
Features an **AI-driven Django backend** and a **Real-time Flutter Dashboard** with WebSocket synchronization.

---

## 🏗️ Architecture

- **Backend (`/backend`)**: Python Django + Django Channels server.
  - **AI Engine**: TensorFlow/Keras Dense Neural Network for intent and severity classification.
  - **Database**: Django ORM with SQLite for local persistence.
  - **Real-time**: WebSockets (via Daphne) for instant incident broadcasting and live chat.
- **Frontend (`/frontend`)**: Flutter Cross-Platform App.
  - **Dashboard**: Live feed of active incidents categorized by severity.
  - **Triage**: Detail view with live team chat and incident resolution.
  - **Voice Triage**: Long-press speech-to-text NLP processing for rapid reporting.

---

## 🚀 Getting Started

### 1. Backend Setup (Python / Django)

Ensure you have Python 3.8+ installed (3.12 recommended).

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Environment Variables
Create a `.env` file in the `backend/` directory by copying the example from the root:
```bash
cp ../.env.example .env
```
Ensure you fill out any required API keys (e.g., Speech-to-Text APIs) inside `backend/.env`.

#### Database Setup
Run the initial Django migrations to set up the SQLite database:
```bash
python manage.py migrate
```

#### Pre-Train the AI Model (Important!)
Before testing incident classification, you must train the neural network to recognize the NLP map. 

If you have an **NVIDIA GPU** configured with CUDA (as per `requirements.txt` environment):
```bash
python train_model.py
```

If you are running on a **CPU only** or a non-NVIDIA machine (like a Mac or a lightweight laptop):
```bash
python train_model_cpu.py
```
*Note: The datasets map emergencies to classifications. A Safety Keyword Layer ensures obvious words like "fire" always trigger correctly even if the AI is still learning.*

#### Run the Server
Start the Django ASGI development server (so WebSockets and HTTP requests work simultaneously):
```bash
python manage.py runserver 0.0.0.0:8000
```
- **API Base**: `http://127.0.0.1:8000/`
- **Websocket**: `ws://127.0.0.1:8000/ws/`

---

### 2. Frontend Setup (Flutter)

In a new terminal, ensure you have the [Flutter SDK](https://docs.flutter.dev/get-started/install) installed.

```bash
# Navigate to frontend
cd frontend

# Fetch dependencies
flutter pub get

# (Linux Users Only) Enable Desktop Support if testing natively
flutter config --enable-linux-desktop
sudo apt-get install -y clang cmake ninja-build pkg-config libgtk-3-dev
```

#### Launch the UI
You can run the app on your connected device, emulator, or as a native desktop/web app:
```bash
flutter run
```

*(If testing web compatibility, you can serve using `flutter run -d web-server` or `flutter run -d chrome`)*

---

## 🛠️ Key Hackathon Features

1.  **Smart AI Classification**: Voice or text input like *"Smoke in the lobby"* ➔ Categorized as **[FIRE] - HIGH SEVERITY** instantly via TensorFlow.
2.  **Live Desk**: The dashboard updates instantly via WebSockets without refreshing.
3.  **Voice-to-Text Triage**: Dedicated push-to-talk button for rapid, hands-free field reporting.
4.  **One-Click Resolve**: Responding to an incident clears it from all connected responder screens in real-time.

---

## 📁 Repository Structure
- `backend/`: Django project (`alertnest`), Channels WebSocket routing (`core`), models, and TensorFlow model scripts.
- `frontend/`: Flutter source code, UI components, and platform runners.
- `backend/tokenizer.json`: Word index mapping for the AI engine.
- `backend/nlp_model.keras`: Saved neural network weights (generated after training).