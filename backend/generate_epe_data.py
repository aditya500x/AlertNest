import json
import random

def calculate_priority(category, severity, people_affected, people_at_risk, time_mins):
    # Base weight by category mapping identical to utils.py classification output
    # 0 = FIRE, 1 = MEDICAL, 2 = SECURITY
    base = 0.0
    if category == 0:
        base += 0.4
    elif category == 1:
        base += 0.3
    else:
        base += 0.1
        
    # Heuristic impact logic for training data regression targets
    score = base + (severity * 0.03) + (people_affected * 0.005) + (people_at_risk * 0.002) - (time_mins * 0.001)
    
    # Sigmoidal squash boundaries
    return max(0.0, min(1.0, score))

def main():
    print("Loading base linguistic dataset...")
    try:
        with open("training_data.json", "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print("Error: Ensure training_data.json exists from generate_data.py")
        return
        
    epe_data = []
    
    print("Generating randomized EPE features and Priority Targets...")
    for item in raw_data:
        # Generate 10 variations of data logic for each linguistic sample
        for _ in range(10):
            # Simulate realistic parsed conditions
            severity = random.randint(1, 10)
            people_affected = random.randint(0, 50)
            people_at_risk = random.randint(0, 100)
            time_reported_mins = random.uniform(0, 120)
            
            target = calculate_priority(
                category=item["label"],
                severity=severity,
                people_affected=people_affected, 
                people_at_risk=people_at_risk,
                time_mins=time_reported_mins
            )
            
            epe_data.append({
                "text": item["text"],
                "nlp_category": item["label"],   # Derived automatically
                "severity": severity,
                "people_affected": people_affected,
                "people_at_risk": people_at_risk,
                "time_reported_mins": time_reported_mins,
                "priority_score": target
            })
        
    with open("epe_training_data.json", "w", encoding="utf-8") as f:
        json.dump(epe_data, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {len(epe_data)} EPE composite samples to epe_training_data.json")

if __name__ == "__main__":
    main()
