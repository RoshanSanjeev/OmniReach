from crewai import Agent, Crew, Task
from backend.agents.masumi_agent import run_agent_flow
from logging_config import get_logger


class MasumiCrew:
    def __init__(self, verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()
        self.logger.info("MasumiCrew initialized")

    def create_crew(self):
        self.logger.info("Creating Masumi access verification crew")

        verifier = Agent(
            name="MasumiVerifier",
            role="Verifies NFT ownership + payment status",
            goal="Ensure only eligible users can unlock access",
            backstory="This agent is the guardian of paid features in the platform.",
            verbose=self.verbose
        )

        task = Task(
            description="Verify NFT ownership and payment status for {wallet}",
            expected_output="Access = True/False + Reason",
            agent=verifier,
            function=run_agent_flow  # crewai will call this with inputs
        )

        crew = Crew(
            agents=[verifier],
            tasks=[task]
        )

        return crew

class ResearchCrew:
    def __init__(self, verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()
        self.logger.info("ResearchCrew initialized")

    def create_crew(self):
        self.logger.info("Creating research crew with agents")
        
        researcher = Agent(
            role='Research Analyst',
            goal='Find and analyze key information',
            backstory='Expert at extracting information',
            verbose=self.verbose
        )

        writer = Agent(
            role='Content Summarizer',
            goal='Create clear summaries from research',
            backstory='Skilled at transforming complex information',
            verbose=self.verbose
        )

        self.logger.info("Created research and writer agents")

        crew = Crew(
            agents=[researcher, writer],
            tasks=[
                Task(
                    description='Research: {text}',
                    expected_output='Detailed research findings about the topic',
                    agent=researcher
                ),
                Task(
                    description='Write summary',
                    expected_output='Clear and concise summary of the research findings',
                    agent=writer
                )
            ]
        )
        self.logger.info("Crew setup completed")
        return crew