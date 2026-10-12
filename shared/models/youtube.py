from typing import Optional
from pydantic import BaseModel, Field


class Thumbnail(BaseModel):
    url: str
    width: Optional[int] = None
    height: Optional[int] = None

class Thumbnails(BaseModel):
    default: Optional[Thumbnail] = None
    medium: Optional[Thumbnail] = None
    high: Optional[Thumbnail] = None
    standard: Optional[Thumbnail] = None
    maxres: Optional[Thumbnail] = None

class LocalizedContent(BaseModel):
    title: str
    description: str

class ChannelSnippet(BaseModel):
    title: str
    description: str = ""
    customUrl: Optional[str] = None
    publishedAt: str
    thumbnails: Thumbnails = Field(default_factory=Thumbnails)
    localized: Optional[LocalizedContent] = None
    country: Optional[str] = None

class VideoSnippet(BaseModel):
    title: str
    description: str = ""
    channelId: str
    channelTitle: str
    publishedAt: str
    thumbnails: Thumbnails = Field(default_factory=Thumbnails)
    localized: Optional[LocalizedContent] = None
    categoryId: Optional[str] = None
    liveBroadcastContent: str = "none"
    defaultLanguage: Optional[str] = None

class RelatedPlaylists(BaseModel):
    likes: str = ""
    uploads: str

class ChannelContentDetails(BaseModel):
    relatedPlaylists: RelatedPlaylists

class ContentRating(BaseModel):
    model_config = {"extra": "allow"}

class VideoContentDetails(BaseModel):
    duration: str
    caption: str
    definition: str
    dimension: str
    licensedContent: bool
    projection: str
    contentRating: ContentRating = Field(default_factory=ContentRating)

class ChannelStatistics(BaseModel):
    viewCount: str
    subscriberCount: Optional[str] = None
    videoCount: str
    hiddenSubscriberCount: bool = False

class VideoStatistics(BaseModel):
    viewCount: Optional[str] = None
    likeCount: Optional[str] = None
    commentCount: Optional[str] = None

class Channel(BaseModel):
    kind: str = "youtube#channel"
    etag: str
    id: str
    snippet: ChannelSnippet
    contentDetails: ChannelContentDetails
    statistics: ChannelStatistics

class Video(BaseModel):
    kind: str = "youtube#video"
    etag: str
    id: str
    snippet: VideoSnippet
    contentDetails: VideoContentDetails
    statistics: VideoStatistics

class ChannelWithVideos(BaseModel):
    channel: Channel
    videos: list[Video]
