from crewai import Agent

masumi_agent = Agent(
    name="MasumiVerifier",
    role="Verifies NFT ownership",
    goal="Ensure only users with required NFT can proceed",
    backstory="This agent acts as a gatekeeper before executing other agents.",
)
