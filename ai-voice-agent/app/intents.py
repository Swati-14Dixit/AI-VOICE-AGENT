# app/intents.py
def recognize_intent(text):
    # Basic keyword matching for intents
    if "greet" in text.lower():
        return "greet"
    elif "bye" in text.lower():
        return "goodbye"
    elif "help" in text.lower():
        return "help"
    else:
        return "unknown"  