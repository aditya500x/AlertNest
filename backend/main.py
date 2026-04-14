from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
import re
import datetime
import json
import os

# TensorFlow / Logic
try:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Suppress CUDA warnings
    import tensorflow as tf
    model_path = os.path.join(os.path.dirname(__file__), 'nlp_model.keras')
    tokenizer_path = os.path.join(os.path.dirname(__file__), 'tokenizer.json')
    if os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path)
        with open(tokenizer_path, 'r') as f:
            word_index = json.load(f)
        HAS_TF = True
    else:
        HAS_TF = False
except Exception as e:
    print("Warning: TensorFlow loading failed, using keyword fallback.")
    HAS_TF = False

import models
import database

# Create DB Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AlertNest API")

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # Convert datetime objects to string before broadcasting
        def default_serializer(obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")
            
        payload = json.dumps(message, default=default_serializer)
        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except:
                pass # ignore closed connections

manager = ConnectionManager()

def classify_incident(text: str):
    text_lower = text.lower()
    cat_id = 2 # default Security
    
    if HAS_TF and model is not None:
        # Preprocess logic (TF)
        import string
        text_clean = text_lower.translate(str.maketrans('', '', string.punctuation))
        words = text_clean.split()
        seq = [word_index.get(w, 1) for w in words] # 1 is OOV
        # pad to max_length 10
        if len(seq) > 10: seq = seq[:10]
        else: seq = seq + [0] * (10 - len(seq))
        
        input_tensor = tf.constant([seq], dtype=tf.int32)
        predictions = model.predict(input_tensor, verbose=0)[0]
        cat_id = int(tf.math.argmax(predictions).numpy())
    else:
        # Fallback keyword logic
        if 'fire' in text_lower or 'smoke' in text_lower: cat_id = 0
        elif 'medical' in text_lower or 'help' in text_lower: cat_id = 1
        
    mapping = {
        0: ("FIRE", "HIGH"),
        1: ("MEDICAL", "MEDIUM"),
        2: ("SECURITY", "LOW")
    }

    # Safety Override: If AI fails but keywords are obvious, force the category
    if 'fire' in text_lower or 'smoke' in text_lower or 'burn' in text_lower:
        return mapping[0]
    if 'medical' in text_lower or 'bleed' in text_lower or 'hurt' in text_lower or 'help' in text_lower:
        return mapping[1]

    return mapping.get(cat_id, ("SECURITY", "LOW"))

def extract_location(text: str) -> str:
    match = re.search(r"(room|floor)\s+([a-zA-Z0-9]+)", text, re.IGNORECASE)
    if match: return f"{match.group(1)} {match.group(2)}"
    return "Unknown"

@app.post("/incident")
async def create_incident(payload: dict, db: Session = Depends(database.get_db)):
    text = payload.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Missing text")
        
    inc_type, inc_severity = classify_incident(text)
    location = extract_location(text)
    
    db_incident = models.Incident(
        text=text,
        type=inc_type,
        severity=inc_severity,
        location=location,
        status="ACTIVE"
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    
    # Broadcast
    await manager.broadcast({
        "event": "new_incident",
        "data": {
            "id": db_incident.id,
            "type": db_incident.type,
            "severity": db_incident.severity,
            "location": db_incident.location,
            "status": db_incident.status
        }
    })
    
    return db_incident

@app.get("/incidents")
async def get_incidents(db: Session = Depends(database.get_db)):
    incidents = db.query(models.Incident).filter(models.Incident.status == "ACTIVE").all()
    
    # Sort HIGH > MEDIUM > LOW
    sev_map = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    return sorted(incidents, key=lambda x: sev_map.get(x.severity, 0), reverse=True)

@app.post("/incident/{id}/resolve")
async def resolve_incident(id: int, db: Session = Depends(database.get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Not Found")
        
    incident.status = "RESOLVED"
    incident.resolved_at = datetime.datetime.utcnow()
    db.commit()
    
    await manager.broadcast({
        "event": "incident_resolved",
        "data": {"id": id}
    })
    return {"success": True}

@app.get("/incident/{id}/chat")
async def get_chat(id: int, db: Session = Depends(database.get_db)):
    msgs = db.query(models.ChatMessage).filter(models.ChatMessage.incident_id == id).order_by(models.ChatMessage.timestamp.asc()).all()
    return msgs

@app.post("/incident/{id}/chat")
async def add_chat(id: int, payload: dict, db: Session = Depends(database.get_db)):
    msg = models.ChatMessage(
        incident_id=id,
        sender=payload.get("sender", "guest"),
        message=payload.get("message", "")
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    
    await manager.broadcast({
        "event": "chat_message",
        "data": {
            "incident_id": id,
            "sender": msg.sender,
            "message": msg.message
        }
    })
    return msg

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We just keep connection open, optionally reading ping/pong
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
