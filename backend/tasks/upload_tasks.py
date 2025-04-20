from crewai import Task

class UploadTasks:
    @staticmethod
    def youtube_upload_task(agent, video_details: dict) -> Task:
        return Task(
            description=(
                "Upload video to YouTube with proper metadata:\n"
                f"- Title: {video_details['title']}\n"
                f"- Description: {video_details['description']}\n"
                f"- Tags: {', '.join(video_details['tags'])}\n"
                f"- Category ID: {video_details['category_id']}"
            ),
            agent=agent,
            expected_output="Confirmation of successful video upload with YouTube video ID",
            async_execution=False,
            tools=[agent.tools[0]]  # Reference YouTubeUploaderTool .name
        )