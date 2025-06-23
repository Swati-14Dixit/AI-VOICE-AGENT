# AI Voice Assistant

A simple AI voice assistant built using FastAPI and the DialoGPT model for natural language processing. This project implements a voice assistant that converts text input to speech and responds conversationally.

## Project Structure

```
Ai-voice-agent/
├── app/
│   ├── main.py          # Main FastAPI application with endpoints and logic
│   ├── intents.py       # Intent recognition module
│   ├── router.py        # Additional API routes (if any)
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## Features

- Accepts text input and processes it using the Microsoft DialoGPT-medium conversational model
- Recognizes user intents for custom responses (greet, goodbye, help, thanks, time)
- Generates dynamic conversational responses using DialoGPT
- Converts text responses to speech using Google Text-to-Speech (gTTS)
- Provides a simple HTML interface for user interaction with text input and audio playback
- Maintains chat history for context-aware conversations
- Includes logging for API request and response tracking

## Requirements

- Python 3.9+
- FastAPI
- PyTorch
- Transformers (Hugging Face)
- gTTS

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd Ai-voice-agent
```

2. Install the requirements:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the application locally, execute:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then, visit `http://127.0.0.1:8000` in your web browser to access the voice assistant interface.

## Dockerization

You can also run this application using Docker:

1. Build the Docker image:

```bash
docker build -t ai-voice-assistant .
```

2. Run the Docker container:

```bash
docker run -d -p 8000:8000 ai-voice-assistant
```

Visit `http://localhost:8000` to use the application.

## Video Demo

[Link to your video demo here]

## Logging

The application includes logging to track API requests and responses for debugging and monitoring.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
