import os
from googleapiclient.discovery import build
from typing import List, Optional

from shared.models import Channel, Video

class YouTubeClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key must be provided either as argument or through YOUTUBE_API_KEY environment variable")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_channel_metadata(self, channel_id: str) -> Channel:
        response = self.youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=channel_id
        ).execute()

        if not response.get('items'):
            raise ValueError(f"Channel not found: {channel_id}")

        return Channel(**response['items'][0])

    def get_channel_metadata_by_handle(self, handle: str) -> Channel:
        response = self.youtube.channels().list(
            part='snippet,contentDetails,statistics',
            forHandle=handle
        ).execute()

        if not response.get('items'):
            raise ValueError(f"Channel not found with handle: {handle}")

        return Channel(**response['items'][0])

    def get_playlist_video_ids(self, playlist_id: str, max_results: int = 50) -> List[str]:
        response = self.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=max_results
        ).execute()

        video_ids = []
        for item in response.get('items', []):
            video_id = item.get('contentDetails', {}).get('videoId')
            if video_id:
                video_ids.append(video_id)
        return video_ids


    def get_all_playlist_video_ids(self, playlist_id: str) -> List[str]:
        video_ids = []
        next_page_token = None

        while True:
            request_params = {
                'part': 'contentDetails',
                'playlistId': playlist_id,
                'maxResults': 50
            }
            if next_page_token:
                request_params['pageToken'] = next_page_token

            response = self.youtube.playlistItems().list(**request_params).execute()

            for item in response.get('items', []):
                video_id = item.get('contentDetails', {}).get('videoId')
                if video_id:
                    video_ids.append(video_id)

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        return video_ids

    def get_playlist_video_ids_limited(self, playlist_id: str, max_videos: int = 50) -> List[str]:
        """
        Get a limited number of video IDs from a playlist.
        
        Args:
            playlist_id: YouTube playlist ID
            max_videos: Maximum number of video IDs to return (default: 50)
        
        Returns:
            List of video IDs up to max_videos
        """
        video_ids = []
        next_page_token = None

        while len(video_ids) < max_videos:
            request_params = {
                'part': 'contentDetails',
                'playlistId': playlist_id,
                'maxResults': min(50, max_videos - len(video_ids))
            }
            if next_page_token:
                request_params['pageToken'] = next_page_token

            response = self.youtube.playlistItems().list(**request_params).execute()

            for item in response.get('items', []):
                video_id = item.get('contentDetails', {}).get('videoId')
                if video_id:
                    video_ids.append(video_id)
                    if len(video_ids) >= max_videos:
                        break

            next_page_token = response.get('nextPageToken')
            if not next_page_token or len(video_ids) >= max_videos:
                break

        return video_ids

    def get_video_metadata(self, video_id: str) -> Video:
        response = self.youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        ).execute()

        if not response.get('items'):
            raise ValueError(f"Video not found: {video_id}")

        return Video(**response['items'][0])


    def get_videos_metadata(self, video_ids: List[str]) -> List[Video]:
        all_metadata = []

        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i + 50]
            response = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(batch)
            ).execute()
            all_metadata.extend(response.get('items', []))

        return [Video(**video) for video in all_metadata]
