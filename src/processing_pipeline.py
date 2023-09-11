from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)


class ProcessingPipeline:
    """
    Class to manage the processing pipeline for adding timecodes to GitHub issues based on video transcripts.
    """

    def __init__(self, github_util, youtube_util, transcript_processor):
        """
        Initialize the ProcessingPipeline.

        :param github_util: GitHubUtility instance for GitHub operations
        :param youtube_util: YouTubeUtility instance for YouTube operations
        :param transcript_processor: TranscriptProcessor instance for transcript operations
        """
        self.github_util = github_util
        self.youtube_util = youtube_util
        self.transcript_processor = transcript_processor

    def match_titles_and_urls(self, issues_titles, video_info):
        """
        Match video titles to their corresponding URLs.

        :param issues_titles: List of issue titles
        :param video_info: List of video information (title, url)
        :return: Dictionary with matched video titles and their video IDs
        """
        matched_videos = {}
        for title in issues_titles:
            for video_title, url in video_info:
                if title.lower() == video_title.lower():
                    video_id = url.split("watch?v=")[1]
                    matched_videos[title] = video_id
                    break
        return matched_videos

    def process_video(self, repo_name, playlist_id, issues_titles):
        """
        Process videos to add timecodes to GitHub issues.

        :param repo_name: GitHub repository name
        :param playlist_id: YouTube playlist ID
        :param issues_titles: List of GitHub issue titles to process
        """
        # Get the video info from YouTube
        video_info = self.youtube_util.get_video_urls_and_titles()

        # Match titles and URLs
        matched_videos = self.match_titles_and_urls(issues_titles, video_info)

        for title, video_id in matched_videos.items():
            print(title)

            new_title = f'Timecodes for "{title}"'
            if self.github_util.is_already_processed(new_title):
                print(f"Issue '{new_title}' has already been processed. Skipping...")
                continue

            print(new_title)
            video_duration = self.youtube_util.get_video_duration(video_id)
            print(f"Video duration: {video_duration} seconds")

            chunk_size = 150 if video_duration <= 600 else 400

            error_messages = {
                TranscriptsDisabled: "Transcripts are disabled for the video.",
                NoTranscriptFound: "No transcript was found in the requested language for video.",
            }

            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                comment_body = self.transcript_processor.process_transcript(
                    transcript, chunk_size
                )
                self.github_util.add_issue_comment_with_confirmation(
                    new_title, comment_body
                )
            except (TranscriptsDisabled, NoTranscriptFound) as e:
                print(
                    f"Encountered an issue with the video `{video_id}`: {error_messages[type(e)]}"
                )
                self.github_util.add_issue_comment_with_confirmation(
                    new_title, error_messages[type(e)]
                )
            except Exception as e:
                print(
                    f"An unexpected error occurred while processing the video `{video_id}`: {e}"
                )
