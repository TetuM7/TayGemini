
# YouTube Flashcard Generator

Developed a full-stack application for generating flashcards from YouTube videos. The application uses React and Vite for the front end, with a Python-based backend built using FastAPI and Uvicorn. It leverages Google's Vertex AI to extract key concepts from video transcripts, making learning from video content more interactive and accessible.

## Features

- **Automated Transcript Extraction**: Utilizes `youtube-transcript-api` to fetch transcripts from YouTube videos.
- **Key Concept Identification**: Uses `langchain` and Google's `Vertex AI` to extract key concepts from the video transcripts.
- **Flashcard Generation**: Converts extracted key concepts into downloadable flashcards.
- **Interactive UI**: Built with React and Vite for a responsive and engaging user experience.
- **Backend API**: Implemented using FastAPI and Uvicorn to handle data processing and interactions.

## Requirements

The following dependencies are required for running the application:

### Frontend

- React
- Vite

### Backend

- Python
- FastAPI
- Uvicorn
- Pytube
- Langchain
- Langchain-core
- Langchain-community
- Langchain-google-vertexai
- Langchain-text-splitters
- Tqdm
- Pydantic
- Youtube-transcript-api

List of required Python packages is also included in `requirements.txt`:

\`\`\`plaintext
fastapi
uvicorn
mangum
pytube
langchain
langchain-core
langchain-community
langchain-google-vertexai
langchain-text-splitters
tqdm
pydantic
youtube-transcript-api
\`\`\`

## Setup Instructions

### Backend

1. **Clone the Repository**:

   \`\`\`bash
   git clone <repository-url>
   cd <repository-name>
   \`\`\`

2. **Setup Google Cloud Credentials**:

   - Create a service account on Google Cloud and download the credentials JSON file.
   - Place the credentials JSON file in your backend directory.
   - Set the environment variable to use the Google Cloud credentials:

     \`\`\`bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
     \`\`\`

   Replace `"/path/to/your/credentials.json"` with the absolute path to your credentials file.

3. **Run the Backend**:

   - Activate the virtual environment:

     \`\`\`bash
     source venv/bin/activate
     \`\`\`

   - Install dependencies:

     \`\`\`bash
     pip install -r requirements.txt
     \`\`\`

   - Start the FastAPI server:

     \`\`\`bash
     uvicorn main:app --reload
     \`\`\`

   - Use `/docs` endpoint to test out the backend API.

### Frontend

1. **Navigate to the frontend directory**:

   \`\`\`bash
   cd frontend
   \`\`\`

2. **Install Dependencies**:

   \`\`\`bash
   npm install
   \`\`\`

3. **Run the Frontend**:

   \`\`\`bash
   npm start
   \`\`\`

4. **Browser Configuration**: You may need to run a command in the terminal to open Chrome with security features disabled to allow FastAPI to accept HTTP requests:

   \`\`\`bash
   open -na "Google Chrome" --args --disable-web-security --user-data-dir="/tmp/chrome_dev"
   \`\`\`

## Usage

- Once both the backend and frontend are running, you can access the application interface to input YouTube video links.
- The app will process the video transcript, extract key concepts, and generate flashcards.
- Flashcards can be downloaded and used for study.

## Notes

- Make sure to replace the placeholder path for Google Cloud credentials with your actual path.
- Ensure the virtual environment is activated before running the backend server.
- Use the `/docs` FastAPI endpoint for interactive API documentation.
