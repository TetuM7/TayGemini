from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from tqdm import tqdm
import logging
import json

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
        loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=True)
        docs = loader.load()
        result = self.text_splitter.split_documents(docs)

        author = result[0].metadata['author']
        length = result[0].metadata['length']
        title = result[0].metadata['title']
        total_size = len(result)

        if verbose:
            print(f"{author}\n{length}\n{title}\n{total_size}")

        return result

    def find_key_concepts(self, documents: list, group_size: int = 2):
        if group_size > len(documents):
            raise ValueError("Group size is larger than the number of documents")

        num_docs_per_group = len(documents) // group_size + (len(documents) % group_size > 0)
        groups = [documents[i:i + num_docs_per_group] for i in range(0, len(documents), num_docs_per_group)]

        batch_concepts = []

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

            batch_concepts.append(output_concept)

            cleaned_concepts = [concept.strip().replace("\n", "").replace("```json", "")for concept in batch_concepts]


            logger.info(f"Model Output: {output_concept}")
            
            
            

        return cleaned_concepts
