from crewai import Agent, Crew, Task
from backend.agents.masumi_agent import run_agent_flow
from logging_config import get_logger

class MasumiCrew:
    def __init__(self, verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()

    def create_crew(self):
        verifier = Agent(
            name="MasumiVerifier",
            role="Verifies NFT ownership and payment status",
            goal="Grant access only to verified wallets",
            backstory="Protects access to sensitive workflows",
            verbose=self.verbose
        )

        def wrapped_agent_flow(**kwargs):
            import asyncio
            return asyncio.run(run_agent_flow(kwargs.get("wallet"), kwargs.get("collection")))

        task = Task(
            description="Verify wallet access by checking NFT and payment",
            expected_output="Access: true/false with details",
            agent=verifier,
            function=wrapped_agent_flow
        )

        return Crew(agents=[verifier], tasks=[task])