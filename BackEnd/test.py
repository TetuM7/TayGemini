import os
from dotenv import load_dotenv
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account

# Load environment variables from .env file
load_dotenv()

urllink = "https://youtu.be/OQEsbP1LVGE?si=QlGG2nrZupSgOJrY"
api_key = os.getenv("APIKEY")

class LinkCleaner:
    def __init__(self, video_url) -> None:
        self.start_index = 17
        self.stop_index = self.start_index + 11
        self.videoid = ""
        self.video_url = video_url

    def testurlextraction(self) -> str:
        self.videoid = self.video_url[self.start_index:self.stop_index]
        return self.videoid

class YoutubeCaptionExtract:
    def __init__(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secret_file = "tayytbtoflashcardgenerator-f77360e14f9e.json"
        self.scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    def get_youtube_caption(self, video_id: str):
        try:
            # Load service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.client_secret_file, scopes=self.scopes)

            # Build the YouTube API client
            youtube = googleapiclient.discovery.build(
                self.api_service_name, self.api_version, credentials=credentials)

            # Request to list captions
            request = youtube.captions().list(
                part="snippet",
                videoId=video_id
            )
            response = request.execute()

            captions = response.get('items', [])
            caption_texts = {}
            for caption in captions:
                caption_id = caption['id']
                # Download the caption track
                download_request = youtube.captions().download(
                    id=caption_id,
                    tfmt='srt'  # Choose the desired format (e.g., 'srt', 'ttml')
                )
                caption_response = download_request.execute()

                # Extract and store the caption text
                caption_texts[caption_id] = caption_response['body']

            return caption_texts
            return response
        
        except googleapiclient.errors.HttpError as e:
            print(f"An HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage

print(linkty)

capsome = YoutubeCaptionExtract()
captiontest = capsome.get_youtube_caption(linkty)
print(captiontest)
