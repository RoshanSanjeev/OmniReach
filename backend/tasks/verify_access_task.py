from crewai import Task
from backend.agents.masumi_agent import masumi_agent
from backend.integrations.masumi import verify_nft_access

verify_access_task = Task(
    description="Check whether the wallet owns the required NFT.",
    expected_output="Access granted if NFT is held.",
    agent=masumi_agent,
    async_execution=False,
    tools=[],
    process=lambda input: verify_nft_access(input["wallet"], input["collection"])
)
