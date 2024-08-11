from fastapi import FastAPI
from pydantic import BaseModel , HttpUrl
from fastapi.middleware.cors import CORSMiddleware
from services.genai import YoutubeProcessor,GeminiProcessor

class VideoAnalysisRequest(BaseModel):
    youtube_link:HttpUrl
    

app=FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], 
                   allow_credentials=True, 
                   allow_methods=["*"],
                     allow_headers=["*"])


@app.post("/analyze-video")
def analyze_video(request: VideoAnalysisRequest): 

    processor = YoutubeProcessor()
    result =processor.retrieve_youtube_documents(str(request.youtube_link))

    genai_processor= GeminiProcessor(
        model_name="gemini-pro",
        project="taygeminiai"
    )

    summary= genai_processor.generate_document_summary(result, verbose =True)

    return {"summary":summary
            }