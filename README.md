# AI-VOICE-AGENT
A simple AI voice assistant built using FastAPI and the DialoGPT model for natural language processing. This project implements a voice assistant that converts text input to speech.  

#Project Structure
ai-voice-agent/
├── app/
│   ├── __init__.py             # Makes 'app' a package (could also be left out in Python 3.3+)
│   ├── __pycache__/            # Auto-generated by Python, usually ignored in version control
│   ├── main.py                  # The main entry point of the application
│   ├── router.py                # FastAPI router for organizing routes
│   ├── service.py               # Service layer for business logic (NLP processing, etc.)
│   ├── intents.py               # File defining intents and potential responses
│   ├── database.py              # Optional: database connection and models (if implemented)
│   ├── utils.py                 # Optional: utility functions (e.g., logging, error handling)
│   ├── templates/               # Optional: HTML templates if rendering server-side
│   ├── static/                  # Optional: Static files (CSS/JS) if needed
│   └── config.py                # Optional: Configuration settings for the project
├── .gitignore                   # Specifies which files to ignore in version control
├── Dockerfile                   # Docker configuration for building the container image
├── requirements.txt             # List of dependencies for the project
├── README.md                    # Project documentation with setup and usage instructions
└── LICENSE                      # Optional: license file for your project

 ## Install the requirement
 
   pip install -r requirements.txt

## Running the Application

   uvicorn app.main:app --reload
   Then, visit `http://127.0.0.1:8000` in your web browser to access the voice assistant interface.

## Logging
The application includes logging to track API requests and responses for debugging and monitoring.

## Project Documentation: Docker Setup

# Overview
This project uses Docker to streamline the development and deployment processes. Below is a step-by-step guide on how to use Docker with this project.

# Dockerfile
- The Dockerfile is located in the root directory of the project. It defines how to build the Docker image for this project.
- Key Sections of the Dockerfile
  • Base Image: The starting point of your Docker image. e.g., FROM python:3.9
  • Working Directory: The directory inside the container where the application will run. e.g., WORKDIR /app
  • Copy Files: Copy your application files into the container. e.g., COPY . .
  • Install Dependencies: Install any necessary packages. e.g., RUN pip install -r requirements.txt
  • Expose Port: The port that the application will use. e.g., EXPOSE 5000
  • Run Command: The command to run your application. e.g., CMD ["python", "app.py"]
  
# Building the Docker Image
To build the Docker image, navigate to the root of your project in the terminal and run the following command:
  bash
  docker build -t yourusername/project-name:tag .
  • Replace yourusername with your Docker Hub username.
  • Replace project-name with the name of your project.
  • Optionally replace tag with a specific version (e.g., v1.0).

# Alternatively, you can run the image using the terminal in VS Code:
1.	Open the Terminal: You can do this by selecting `Terminal` from the top menu and then `New Terminal`.
2.	Run the Docker Command: Execute the following command in the terminal:
   docker run -d --name ai-voice-agent swatidix14/ai-voice-agent:latest
2.	Here, the `-d` flag runs the container in detached mode, and `--name ai-voice-agent` gives your container a name for easier management.
After running this command, your Docker container should start based on the specified image. You can check its status by executing:
docker ps
This will list all running containers, including your newly started one.

Great! Now that you have your Docker image running, let’s go through the steps to log in to Docker Hub and view the image you pulled earlier.
Step 1: Log in to Docker Hub
	1.	Open the Terminal: If you haven’t already, open a new terminal in Visual Studio Code.
	2.	Run the Login Command: Use the following command to log in to Docker Hub:
    docker login


Step 2: Pulling the Docker Image from Docker Hub
Users can access the Docker image on Docker Hub with the following command:
bash
  docker pull yourusername/project-name:tag

  
Step 3: View Your Pulled Image
To view the images that you have pulled (including the one from Docker Hub), you can use the following command:
docker images
This command will list all images on your local machine, including their repository names, tags, and image IDs. Look for `swatidix14/ai-voice-agent` in the list.
  

# Accessing Your Application
Once the container is running, you can access your application in your web browser at:

http://localhost:your_host_port

# Conclusion
This guide should help you navigate the process of building, running, and accessing the Docker container and images for this project. If you have any further questions, feel free to reach out.


