✅ CrewAI Masumi Access Agent Setup

Included files:
- backend/agents/masumi_agent.py      : Defines the MasumiVerifier CrewAI agent
- backend/tasks/verify_access_task.py : Wraps the agent in a Task using verify_nft_access()

To use:
1. Place contents into your OmniReach project.
2. In your Crew script:

   from backend.tasks.verify_access_task import verify_access_task
   from crewai import Crew

   crew = Crew(tasks=[verify_access_task])
   result = crew.run(input={"wallet": "0x123...", "collection": "omni-nft-v1"})
   print(result)
