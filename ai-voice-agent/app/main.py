from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import StreamingResponse, HTMLResponse
import io
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from gtts import gTTS
from app.router import router
from app.intents import recognize_intent

app = FastAPI()

app.include_router(router)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
except Exception as e:
    logging.error(f"Error loading DialoGPT model: {e}")
    tokenizer = None
    model = None

chat_history_ids = None

def generate_response(user_input: str) -> str:
    global chat_history_ids
    if tokenizer is None or model is None:
        return "Model loading failed."

    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    if chat_history_ids is not None:
        chat_history_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
    else:
        chat_history_ids = new_user_input_ids

    output = model.generate(chat_history_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    bot_response = tokenizer.decode(output[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
  
    chat_history_ids = output

    return bot_response

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Voice Assistant</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 0.5em;
            }
            form {
                display: flex;
                margin-bottom: 1em;
            }
            input[type="text"] {
                padding: 0.5em;
                font-size: 1.2em;
                border: none;
                border-radius: 5px 0 0 5px;
                width: 300px;
            }
            button {
                padding: 0.5em 1em;
                font-size: 1.2em;
                border: none;
                border-radius: 0 5px 5px 0;
                background-color: #ff6b6b;
                color: white;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #ff3b3b;
            }
            audio {
                outline: none;
                width: 300px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
            }
            .suggestions {
                margin-top: 1em;
                font-size: 1em;
                background: rgba(255, 255, 255, 0.2);
                padding: 1em;
                border-radius: 10px;
                max-width: 400px;
                text-align: center;
            }
            .suggestions span {
                background: #ff6b6b;
                padding: 0.3em 0.6em;
                border-radius: 5px;
                margin: 0 0.3em;
                cursor: pointer;
                display: inline-block;
                transition: background-color 0.3s ease;
            }
            .suggestions span:hover {
                background: #ff3b3b;
            }
        </style>
    </head>
    <body>
        <h1>Voice Assistant</h1>
        <form id="inputForm" method="post" action="/speak">
            <input type="text" name="user_input" placeholder="Type something..." required>
            <button type="submit">Speak</button>
        </form>
        <audio id="audioPlayer" controls></audio>
        <div class="suggestions">
            Try these: 
            <span onclick="fillInput('Hello')">Hello</span>
            <!-- Removed Weather suggestion as per user request -->
            <span onclick="fillInput('Can you help me?')">Help</span>
            <span onclick="fillInput('Thank you')">Thanks</span>
            <span onclick="fillInput('What time is it?')">Time</span>
        </div>

        <script>
            function fillInput(text) {
                document.querySelector('input[name="user_input"]').value = text;
            }
            document.getElementById('inputForm').onsubmit = async function(event) {
                event.preventDefault();
                const formData = new FormData(this);
                const audioPlayer = document.getElementById('audioPlayer');

                const response = await fetch('/speak', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = URL.createObjectURL(blob);
                    audioPlayer.src = url;
                    audioPlayer.play();
                } else {
                    alert('Error generating speech');
                }
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/speak")
async def speak(user_input: str = Form(...)):
    try:
        intent = recognize_intent(user_input)

        custom_responses = {
            "greet": "Hello! How can I assist you today?",
            "goodbye": "Goodbye! Have a great day!",
            "help": "Sure, I am here to help you. What do you need assistance with?",
            "thanks": "You're welcome! Happy to help."
        }

        if intent == "time":
            from datetime import datetime
            now = datetime.now()
            response_text = f"The current time is {now.strftime('%H:%M:%S')}."
        elif intent in custom_responses:
            response_text = custom_responses[intent]
        else:
            response_text = generate_response(user_input)

        tts = gTTS(text=response_text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        return StreamingResponse(mp3_fp, media_type="audio/mpeg")

    except Exception as e:
        logging.error(f"Error generating speech: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate speech")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

       

