from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from tqdm import tqdm
import logging
import json
from pytube.exceptions import PytubeError  # Import PytubeError for handling exceptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiProcessor:
    def __init__(self, model_name, project):
        self.model = VertexAI(model_name=model_name, project=project)

    def generate_document_summary(self, documents, **args):
        if len(documents) > 10:
            chain_type = "map_reduce"
        else:
            chain_type = "stuff"

        chain = load_summarize_chain(llm=self.model, chain_type=chain_type, **args)
        return chain.run(documents)

    def get_model(self):
        return self.model

class YoutubeProcessor:
    def __init__(self, genai_processor: GeminiProcessor) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        self.GeminiProcessor = genai_processor

    def retrieve_youtube_documents(self, video_url: str, verbose=False):
     try:
        yt = YouTube(video_url)
        video_id = yt.video_id
        
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        if verbose:
            for transcript in transcript_list:
                print(f"Language Code: {transcript.language_code}")
                print(f"Language: {transcript.language}")
                print(f"Is Translatable: {transcript.is_translatable}")
                print(f"Is Manually Created: {transcript.is_generated}")
                print("-" * 40)
        
        transcript = transcript_list.find_transcript(['en'])
        transcript_data = transcript.fetch()
        
        full_transcript = " ".join([entry['text'] for entry in transcript_data])
        
        return full_transcript

     except Exception as e:
        print(f"An error occurred: {e}")
        return None


    def find_key_concepts(self, documents: list, group_size: int = 2):
        if group_size > len(documents):
            raise ValueError("Group size is larger than the number of documents")

        num_docs_per_group = len(documents) // group_size + (len(documents) % group_size > 0)
        groups = [documents[i:i + num_docs_per_group] for i in range(0, len(documents), num_docs_per_group)]

        batch_concepts = {}
        arrayofkeyconcepts = []

        for group in tqdm(groups):
            group_content = ""

            for doc in group:
                group_content += doc.page_content

            prompt = PromptTemplate(
                template="""
                Find and define key concepts or terms found in the text:
                {text}

                Respond in the following format as a JSON object without any backticks separating each concept with a comma:
                {{"concept":"definition", "concept":"definition", ...}}""",
                input_variables=["text"]
            )
            chain = prompt | self.GeminiProcessor.get_model()

            output_concept = chain.invoke({"text": group_content})

            cleaned_output = output_concept.strip().replace("```json", "").replace("```", "").replace("\n", "")

            logger.info(f"Model Output: {output_concept}")
            try:
                parsed_output = json.loads(cleaned_output)
                batch_concepts.update(parsed_output)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {cleaned_output}\nError: {e}")

        arrayofkeyconcepts = [{"concept": key, "definition": value} for key, value in batch_concepts.items()]
        return arrayofkeyconcepts
