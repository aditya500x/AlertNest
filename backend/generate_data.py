import random
import json

# Data Generator for AlertNest Multilingual AI (v6.0 - Kannada & Southern Fix)
# Specifically includes more colloquial and imperative terms.

categories = {
    "FIRE": 0,
    "MEDICAL": 1,
    "SECURITY": 2
}

languages = {
    "English": {
        "FIRE": ["fire", "smoke", "burning", "flames", "fire in room"],
        "MEDICAL": ["help", "ambulance", "bleeding", "doctor", "emergency"],
        "SECURITY": ["police", "thief", "robbery", "intruder", "security"]
    },
    "Hindi": {
        "FIRE": ["आग", "धुआं", "aag", "dhuan", "jal raha hai", "badi aag"],
        "MEDICAL": ["मदद", "डॉक्टर", "madad", "khoon", "ambulance", "chot"],
        "SECURITY": ["पुलिस", "ಚೋರ್", "police", "chor", "shakki", "badmash"]
    },
    "Kannada": {
        "FIRE": ["ಬೆಂಕಿ", "ಬೆಂಕಿ ಹಚ್ಚಿದೆ", "ಬೆಂಕಿ ಪರವಗಿದೆ", "ಹೊಗೆ ಬರ್ತಿದೆ", "benki", "hoge", "benki hachide", "benki aagide", "hoge barthide"],
        "MEDICAL": ["ಸಹಾಯ ಮಾಡಿ", "ಅಂಬ್ಯುಲೆನ್ಸ್ ಬೇಕು", "ರಕ್ತ ಬರ್ತಿದೆ", "ವೈದ್ಯರು", "sahaya", "vaidyaru", "sahaya madi", "ambulance beku", "raktha barthide"],
        "SECURITY": ["ಕಳ್ಳ ಬಂದಿದ್ದಾನೆ", "ಪೊಲೀಸ್ ಬೇಕು", "ಶಕ್ಕಿ ಇದೆ", "kalla", "police", "kalla bandiddane", "police beku", "shakki ide", "dongalu"]
    },
    "Tamil": {
        "FIRE": ["தீ விಬத்து", "நெருப்பு", "thee", "neruppu", "pukai", "thee paravugiradhu"],
        "MEDICAL": ["உதவி தேவை", "மருத்துவர்", "udhavi", "sahayam", "ratham", "maruthuvar"],
        "SECURITY": ["காவல்துறை", "திருடன்", "police", "kavalthurai", "thirudan", "police beku"]
    },
    "Telugu": {
        "FIRE": ["అగ్ని ప్రమాదం", "మంటలు", "agni", "mantalu", "mantalu vastunayi"],
        "MEDICAL": ["ಸಹಾಯಂ", "వైದ್ಯుడు", "sahayam", "debba", "raktham", "avasaram", "doctor"],
        "SECURITY": ["పోలీసు", "దొంగ", "police", "donga", "dongalthanam", "shakki"]
    }
}

def main():
    dataset = []
    
    # Generate 5,500 samples for high robustness
    for _ in range(5500):
        lang_key = random.choice(list(languages.keys()))
        cat = random.choice(list(categories.keys()))
        
        term = random.choice(languages[lang_key][cat])
        
        # Randomly add "help" or locations to make it conversational
        sentence = term
        if random.random() > 0.4:
            loc = random.choice(["room", "floor", "lobby", "near here", "manzil", "kamra"])
            sentence = f"{loc} {term}" if random.random() > 0.5 else f"{term} in {loc}"
            
        dataset.append({"text": sentence, "label": categories[cat]})
        
    with open("training_data.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(dataset)} samples (v6.0) with deep Kannada and Southern language support.")

if __name__ == "__main__":
    main()
