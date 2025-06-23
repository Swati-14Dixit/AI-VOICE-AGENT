# app/intents.py
def recognize_intent(text):
    # Expanded keyword matching for intents
    text_lower = text.lower()
    if any(greet in text_lower for greet in ["hello", "hi", "hey", "greetings", "good morning", "good evening"]):
        return "greet"
    elif any(bye in text_lower for bye in ["bye", "goodbye", "see you", "farewell", "take care"]):
        return "goodbye"
    elif any(help_word in text_lower for help_word in ["help", "support", "assist", "can you help", "need assistance"]):
        return "help"
    elif any(thank in text_lower for thank in ["thank you", "thanks", "appreciate it", "grateful"]):
        return "thanks"
    elif any(weather in text_lower for weather in ["weather", "temperature", "forecast", "rain", "sunny"]):
        return "weather"
    elif any(time in text_lower for time in ["time", "clock", "current time", "what time"]):
        return "time"
    else:
        return "unknown"
