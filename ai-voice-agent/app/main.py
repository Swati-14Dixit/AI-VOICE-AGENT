from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import StreamingResponse, HTMLResponse
import io
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from gtts import gTTS

# Initialize FastAPI
app = FastAPI()

# Configure logging for tracking API requests and responses
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the tokenizer and model from Hugging Face
try:
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
except Exception as e:
    logging.error(f"Error loading DialoGPT model: {e}")
    tokenizer = None
    model = None

# Global variable for chat history
chat_history_ids = None

def generate_response(user_input: str) -> str:
    """
    Generates a response based on the user input using DialoGPT.
    """
    global chat_history_ids
    if tokenizer is None or model is None:
        return "Model loading failed."

    # Encode the new user input, add the eos_token and return a tensor in PyTorch
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Concatenate the new user input with the chat history (if it exists)
    if chat_history_ids is not None:
        chat_history_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
    else:
        chat_history_ids = new_user_input_ids

    # Generate a response
    output = model.generate(chat_history_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Extract the bot's response
    bot_response = tokenizer.decode(output[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
    
    # Update the chat history for the next round
    chat_history_ids = output

    return bot_response

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Displays the HTML form for user input.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Voice Assistant</title>
    </head>
    <body>
        <h1>Voice Assistant</h1>
        <form id="inputForm" method="post" action="/speak">
            <input type="text" name="user_input" placeholder="Type something..." required>
            <button type="submit">Speak</button>
        </form>
        <audio id="audioPlayer" controls></audio>

        <script>
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
    """
    Generates speech from the user input after processing with DialoGPT.
    """
    try:
        # Generate response using NLP
        response_text = generate_response(user_input)

        # Generate speech using gTTS
        tts = gTTS(text=response_text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Return the audio as a streaming response
        return StreamingResponse(mp3_fp, media_type="audio/mpeg")

    except Exception as e:
        logging.error(f"Error generating speech: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate speech")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

       
