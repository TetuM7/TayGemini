from fastapi import FastAPI
from pydantic import BaseModel , HttpUrl
from fastapi.middleware.cors import CORSMiddleware
from services.genai import YoutubeProcessor,GeminiProcessor

class VideoAnalysisRequest(BaseModel):
    youtube_link:HttpUrl
    

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  # You can list the specific frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai_processor= GeminiProcessor(
        model_name="gemini-pro",
        project="taygeminiai"
    )

@app.post("/analyze-video")
def analyze_video(request: VideoAnalysisRequest): 

    processor = YoutubeProcessor(genai_processor=genai_processor)
    result =processor.retrieve_youtube_documents(str(request.youtube_link))

    key_concepts= processor.find_key_concepts(result, group_size=2)

    return {"key_concepts":key_concepts
            }