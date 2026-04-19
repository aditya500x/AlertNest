import os
import json
import numpy as np
import tensorflow as tf
from core.utils import classify_incident
import string

# Ensure we use exactly the same parameters
VOCAB_SIZE = 8000
MAX_LENGTH = 64
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pre-load resources once
def _load_engine_resources():
    try:
        model_path = os.path.join(BASE_DIR, 'epe_model.keras')
        tokenizer_path = os.path.join(BASE_DIR, 'tokenizer.json')
        
        epe_model = tf.keras.models.load_model(model_path)
        with open(tokenizer_path, 'r', encoding='utf-8') as f:
            word_index = json.load(f)
            
        # Reconstruct tokenizer
        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
        tokenizer.word_index = word_index
        return epe_model, tokenizer
    except Exception as e:
        print(f"Warning: EPE loading failed: {e}")
        return None, None

EPE_MODEL, EPE_TOKENIZER = _load_engine_resources()

class EmergencyPriorityEngine:
    def __init__(self):
        self.model = EPE_MODEL
        self.tokenizer = EPE_TOKENIZER
        
        # Mapping constants from ML model
        self.severity_map = {"HIGH": 8, "MEDIUM": 5, "LOW": 2}
        self.cat_map = {"FIRE": 0, "MEDICAL": 1, "SECURITY": 2}

    def _prepare_text(self, text):
        text_lower = text.lower()
        text_clean = text_lower.translate(str.maketrans('', '', string.punctuation))
        words = text_clean.split()
        seq = [self.tokenizer.word_index.get(w, 1) if w in self.tokenizer.word_index else 1 for w in words]
        if len(seq) > MAX_LENGTH: 
            seq = seq[:MAX_LENGTH]
        else: 
            seq = seq + [0] * (MAX_LENGTH - len(seq))
        return seq

    def _determine_reasoning(self, base_type, base_sev, priority, people_at_risk):
        # Fallback heuristic reason generator since purely numeric Keras doesn't generate LLM chat logic
        reasons = []
        if base_type == "FIRE":
            reasons.append("Immediate fire hazard and scale risk.")
        elif base_type == "MEDICAL":
            reasons.append("Urgent medical attention required.")
        else:
            reasons.append("Security threat assessment.")
            
        if people_at_risk > 10:
            reasons.append(f"High risk: {people_at_risk} people structurally affected.")
        elif people_at_risk > 0:
            reasons.append(f"{people_at_risk} individual(s) at immediate risk.")
            
        if priority >= 0.7:
            reasons.append("Critical priority threshold.")
            
        return " - ".join(reasons)

    def rank_emergencies(self, emergencies, available_responders=None):
        """
        Takes a list of unstructured or semi-structured emergencies.
        Returns a sorted JSON dictionary of priorities.
        """
        if not self.model or not self.tokenizer:
            return {"error": "EPE models are not loaded properly."}
            
        if not emergencies:
            return {"prioritized_emergencies": []}
            
        texts = []
        meta_features = []
        results = []
        
        # Batch preparation
        for e in emergencies:
            text = e.get("text", "")
            
            # Step 1: Sub-processing using original nlp_model mappings
            inc_type, inc_severity = classify_incident(text)
            
            # Extract optional numericals or default
            people_affected = e.get("people_affected", 0)
            people_at_risk = e.get("people_at_risk", 0)
            time_reported_mins = e.get("time_reported_mins", 0)
            
            # Encode for neural network
            cat_val = self.cat_map.get(inc_type, 2)
            sev_val = self.severity_map.get(inc_severity, 2)
            
            seq = self._prepare_text(text)
            texts.append(seq)
            
            meta_features.append([cat_val, sev_val, people_affected, people_at_risk, time_reported_mins])
            
            # Store base processed meta for fast formatting later
            results.append({
                "id": e.get("id", "E-Unknown"),
                "text": text,
                "type": inc_type,
                "severity_label": inc_severity,
                "people_at_risk": people_at_risk
            })
            
        # Run dual-input batch inference
        text_inputs = tf.constant(texts, dtype=tf.int32)
        meta_inputs = tf.constant(meta_features, dtype=tf.float32)
        
        predictions = self.model.predict([text_inputs, meta_inputs], verbose=0)
        
        # Construct and scale output
        prioritized = []
        for i, row in enumerate(results):
            score = float(predictions[i][0])
            
            reason = self._determine_reasoning(
                row["type"], 
                row["severity_label"], 
                score, 
                row["people_at_risk"]
            )
            
            prioritized.append({
                "id": row["id"],
                "priority_score": round(score, 3), # normalize precision
                "reason": reason
            })
            
        # Re-Rank! (Highest priority first)
        prioritized = sorted(prioritized, key=lambda x: x["priority_score"], reverse=True)
        
        return {"prioritized_emergencies": prioritized}
