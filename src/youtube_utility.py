import isodate
from googleapiclient.discovery import build


class YouTubeUtility:
    """
    Class to manage YouTube operations.
    """

    def __init__(self, api_key, playlist_id):
        """
        Initialize the YouTubeUtility class.

        :param api_key: YouTube API key
        :param playlist_id: YouTube playlist ID
        """
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist_id = playlist_id

    def update_playlist(self, new_playlist_id):
        """
        Update the playlist ID.

        :param new_playlist_id: New YouTube playlist ID
        """
        self.playlist_id = new_playlist_id

    def get_video_urls_and_titles(self):
        """
        Retrieve video URLs and titles from a playlist.

        :return: List of tuples containing video titles and URLs
        """
        video_info = []
        try:
            request = self.youtube.playlistItems().list(
                part="snippet", maxResults=500, playlistId=self.playlist_id
            )

            while request:
                response = request.execute()
                for item in response.get('items', []):
                    snippet = item.get('snippet', {})
                    video_id = snippet.get('resourceId', {}).get('videoId', '')
                    video_title = snippet.get('title', '')
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    video_info.append((video_title, video_url))

                request = self.youtube.playlistItems().list_next(request, response)
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        return video_info

    def get_video_duration(self, video_id):
        """
        Retrieve the duration of a video.

        :param video_id: YouTube video ID
        :return: Video duration in seconds
        """
        try:
            request = self.youtube.videos().list(part="contentDetails", id=video_id)
            response = request.execute()
            video_duration = (
                response.get('items', [{}])[0]
                .get('contentDetails', {})
                .get('duration', '')
            )
            return isodate.parse_duration(video_duration).total_seconds()
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0
