# agents/campaign_agent.py
from crewai import Agent
from typing import List
from backend.tools.youtube_uploader import YouTubeUploader  # Update path as needed
from crewai.tools import BaseTool

class CampaignPostingAgent:
    def __init__(self):
        self.tools = self._initialize_tools()

    def _initialize_tools(self) -> List[BaseTool]:  # Changed to return instances
        return [YouTubeUploader()]  # Instantiate the tool

    def create_agent(self) -> Agent:
        return Agent(
            role="Social Media Campaign Manager",
            goal="Upload marketing content to YouTube following brand guidelines",
            backstory=(
                "A specialized AI agent that handles automated content distribution "
                "for automotive marketing campaigns."
            ),
            tools=self.tools,  # Now passing tool instances
            verbose=True,
            allow_delegation=False
        )