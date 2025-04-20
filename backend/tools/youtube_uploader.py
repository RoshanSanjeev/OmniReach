from crewai.tools import BaseTool
from typing import ClassVar, Optional
from pydantic import Field, ConfigDict, PrivateAttr
import os
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from backend.utils.path_manager import path_manager

class YouTubeUploader(BaseTool):
    name:        str = Field(
        "YouTube Uploader",
        description="Tool name – what this tool is called in the agent registry"
    )
    description: str = Field(
        "Uploads videos to YouTube channel with metadata",
        description="Tool functionality – brief summary of what this tool does"
    )
    credentials_path: str = Field(
        default="credentials.json",
        description="Path to Google API credentials"
    )
    token_path: str = Field(
        default="token.json",
        description="Path to authentication token"
    )
    # Class variables should be annotated with ClassVar
    SCOPES: ClassVar[list] = ['https://www.googleapis.com/auth/youtube.upload']
    VALID_CATEGORIES: ClassVar[dict[int, str]] = {
        1: "Film & Animation",
        2: "Autos & Vehicles",
        10: "Music",
        15: "Pets & Animals",
        17: "Sports",
        20: "Gaming",
        22: "People & Blogs",  # Now valid
        23: "Comedy",
        24: "Entertainment",
        25: "News & Politics",
        26: "Howto & Style",
        27: "Education",
        28: "Science & Technology"
        # Add more categories as needed
        }  
        
    # Declare private runtime-only attributes
    _logger:        logging.Logger = PrivateAttr()
    _youtube_client: object         = PrivateAttr()

   # Pydantic configuration
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **kwargs):
        # Initialize Pydantic model first
        super().__init__(**kwargs)
        
        # Post-initialization setup
        object.__setattr__(self, "_logger", logging.getLogger(self.__class__.__name__))
        object.__setattr__(self, "_youtube_client", self.authenticate_youtube())

    def authenticate_youtube(self):
        """Authentication logic remains the same"""
        credentials = None
        if os.path.exists(self.token_path):
            try:
                credentials = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            except Exception as e:
                self._logger.warning(f"Token load failed: {e}")

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                credentials = flow.run_local_server(port=0)

            with open(self.token_path, "w") as token_file:
                token_file.write(credentials.to_json())

        return build("youtube", "v3", credentials=credentials)

    def _run(self, video_path: str, title: str, description: str, tags: list, category_id: int) -> str:
        """Your existing upload logic here"""
        try:
            # Convert to absolute path
            abs_video_path = path_manager.get_path(video_path)
            
            if not path_manager.verify_path(abs_video_path):
                self._logger.error(f"File not found: {abs_video_path}")
                raise FileNotFoundError(f"Video file missing at: {abs_video_path}")
            
            body = {
                "snippet": {
                    "title": title[:100],
                    "description": description[:5000],
                    "tags": tags[:500],
                    "categoryId": str(category_id)
                },
                "status": {
                    "privacyStatus": "public"
                }
            }

            media = MediaFileUpload(abs_video_path, mimetype="video/mp4", chunksize=-1, resumable=True)
            request = self._youtube_client.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    self._logger.info(f"Upload progress: {int(status.progress() * 100)}%")

            return f"Video uploaded successfully! ID: {response['id']}"
        
        except Exception as e:
            self._logger.error(f"Upload failed: {e}", exc_info=True)
            raise



# if __name__ == "__main__":
#     uploader = YouTubeUploader()
#     uploader._run(
#         video_file="backend/content/sample_road.mp4",
#         title="pretty road",
#         description="uploading  stuff here",
#         tags=["test", "automation"],
#         category_id=2,  # Category 22 = People & Blogs
#         privacy_status="public"  # Keep it private for testing
#     )
