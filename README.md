# 🛡️ AlertNest: Integrated Emergency Response MVP

A robust, hackathon-ready emergency notification and response system. 
Features an **AI-driven FastAPI backend** and a **Real-time Flutter Dashboard** with WebSocket synchronization.

---

## 🏗️ Architecture

- **Backend (`/backend`)**: Python FastAPI server.
  - **AI Engine**: TensorFlow/Keras Dense Neural Network for intent classification.
  - **Database**: SQLAlchemy/SQLite for local persistence.
  - **Real-time**: WebSockets for instant incident broadcasting and live chat.
- **Frontend (`/frontend`)**: Flutter Cross-Platform App.
  - **Dashboard**: Live feed of active incidents categorized by severity.
  - **Triage**: Detail view with live team chat and incident resolution.

---

## 🚀 Getting Started

### 1. Backend Setup (Python)

Ensure you have Python 3.8+ installed (3.12 recommended).

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Pre-Train the AI Model
Before launching, train the neural network to recognize your NLP map:
```bash
python train_model.py
```
*Note: I have augmented the training data and added a **Safety Keyword Layer** in `main.py` so that obvious words like "fire" or "medical" will always trigger correctly even if the AI is still learning.*

#### Run the Server
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
- **API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Websocket**: `ws://127.0.0.1:8000/ws`

---

### 2. Frontend Setup (Flutter)

In a new terminal, ensure you have the [Flutter SDK](https://docs.flutter.dev/get-started/install) installed.

```bash
# Navigate to frontend
cd frontend

# Fetch dependencies
flutter pub get

# (Linux Users Only) Enable Desktop Support if needed
flutter config --enable-linux-desktop
sudo apt-get install -y clang cmake ninja-build pkg-config libgtk-3-dev
```

#### Launch the UI
```bash
flutter run
```

---

## 🛠️ Key Hackathon Features

1.  **Smart Classification**: Type *"Smoke in the lobby"* ➔ Categorized as **[FIRE] - HIGH SEVERITY** instantly.
2.  **Live Desk**: The dashboard updates via WebSockets without refreshing.
3.  **Chat & Sync**: Every incident has a dedicated real-time chat room for responder coordination.
4.  **One-Click Resolve**: Responding to an incident clears it from all connected responder screens in real-time.

---

## 📁 Repository Structure
- `backend/`: FastAPI, SQLAlchemy models, and TensorFlow logic.
- `frontend/`: Flutter source code and platform runners.
- `src/`: (Optional) Legacy Node.js implementation if pivoting.
- `tokenizer.json`: Word index mapping for the AI engine.
- `nlp_model.keras`: Saved neural network weights.