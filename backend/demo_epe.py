import os
import sys
import json
import django

# Setup Django Environment for utils.py to load cleanly if it depends on Django settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alertnest.settings')
django.setup()

from core.epe import EmergencyPriorityEngine

def main():
    print("Initializing Engineering Priority Engine (EPE)...")
    engine = EmergencyPriorityEngine()
    
    mock_emergencies = [
        {
            "id": "E1",
            "text": "I see a suspicious person loitering in the parking lot. He might have a weapon.",
            "people_affected": 0,
            "people_at_risk": 0,
            "time_reported_mins": 30
        },
        {
            "id": "E2",
            "text": "Building engulf in aag, people trapped on the 3rd floor!!",
            "people_affected": 5,
            "people_at_risk": 15,
            "time_reported_mins": 2
        },
        {
            "id": "E3",
            "text": "Send an ambulance, my friend is bleeding bad.",
            "people_affected": 1,
            "people_at_risk": 1,
            "time_reported_mins": 5
        }
    ]
    
    print("\n--- INCOMING UNSTRUCTURED EMERGENCIES ---")
    print(json.dumps(mock_emergencies, indent=2))
    
    print("\n--- RUNNING EPE INFERENCE ---")
    output = engine.rank_emergencies(mock_emergencies)
    
    print("\n--- PRIORITIZED ENGINE OUTPUT ---")
    print(json.dumps(output, indent=2))
    
if __name__ == "__main__":
    main()
