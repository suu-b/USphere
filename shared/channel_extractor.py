import re
from typing import List, Optional
from urllib.parse import urlparse, parse_qs


class ChannelReferenceExtractor:
    """Extract YouTube channel references from text."""
    
    # Pattern for YouTube handles (@username) - more restrictive to avoid false positives
    HANDLE_PATTERN = r'@[a-zA-Z0-9][a-zA-Z0-9_.-]{0,28}[a-zA-Z0-9]'
    
    # Pattern for YouTube channel URLs
    CHANNEL_URL_PATTERN = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:channel/|c/|user/|@)[\w\.-]+|youtu\.be/[\w\.-]+)'
    
    # Pattern for channel IDs (UC followed by 22 characters)
    CHANNEL_ID_PATTERN = r'UC[a-zA-Z0-9_-]{22}'
    
    @staticmethod
    def is_valid_handle(handle: str) -> bool:
        """Validate that a handle looks like a real YouTube handle."""
        # Reject email addresses
        if '@' in handle and '.' in handle and handle.rfind('.') > handle.rfind('@'):
            return False
        
        # Reject handles that are too short or end with special characters
        if len(handle) < 2 or handle[-1] in '._-':
            return False
        
        # Reject handles with consecutive special characters
        if '..' in handle or '__' in handle or '--' in handle:
            return False
        
        return True
    
    @staticmethod
    def extract_handles(text: str) -> List[str]:
        """Extract YouTube handles from text."""
        matches = re.findall(ChannelReferenceExtractor.HANDLE_PATTERN, text)
        # Normalize handles (strip double @) and filter out invalid ones
        normalized = [h.replace('@@', '@') for h in matches]
        return [h for h in normalized if ChannelReferenceExtractor.is_valid_handle(h)]
    
    @staticmethod
    def extract_channel_ids(text: str) -> List[str]:
        """Extract YouTube channel IDs from text."""
        matches = re.findall(ChannelReferenceExtractor.CHANNEL_ID_PATTERN, text)
        return matches
    
    @staticmethod
    def extract_channel_from_url(url: str) -> Optional[str]:
        """
        Extract channel handle or ID from a YouTube URL.
        Returns the handle (with @) or channel ID if found, None otherwise.
        """
        try:
            parsed = urlparse(url)
            
            # Handle various YouTube URL formats
            if 'youtube.com' in parsed.netloc:
                path = parsed.path
                
                # /channel/UC...
                if '/channel/' in path:
                    channel_id = path.split('/channel/')[-1].split('/')[0]
                    if re.match(r'^UC[a-zA-Z0-9_-]{22}$', channel_id):
                        return channel_id
                
                # /c/ or /user/ - these are custom URLs, hard to convert without API
                # /@handle format
                elif path.startswith('/@'):
                    handle = path.split('/')[1]
                    return f'@{handle}'
                
                # Handle query parameters like ?v= (video URLs)
                if parsed.query:
                    query = parse_qs(parsed.query)
                    # Could extract video ID and then get channel via API, but that's expensive
                    pass
            
            return None
        except Exception:
            return None
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract YouTube URLs from text."""
        matches = re.findall(ChannelReferenceExtractor.CHANNEL_URL_PATTERN, text)
        return matches
    
    @staticmethod
    def extract_all_references(text: str) -> List[str]:
        """
        Extract all channel references from text.
        Returns a list of handles (with @) and channel IDs.
        """
        references = []
        
        # Extract handles
        handles = ChannelReferenceExtractor.extract_handles(text)
        references.extend(handles)
        
        # Extract channel IDs
        channel_ids = ChannelReferenceExtractor.extract_channel_ids(text)
        references.extend(channel_ids)
        
        # Extract URLs and parse them
        urls = ChannelReferenceExtractor.extract_urls(text)
        for url in urls:
            channel_ref = ChannelReferenceExtractor.extract_channel_from_url(url)
            if channel_ref:
                references.append(channel_ref)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_refs = []
        for ref in references:
            if ref not in seen:
                seen.add(ref)
                unique_refs.append(ref)
        
        return unique_refs
    
    @staticmethod
    def extract_from_video(video) -> List[str]:
        """
        Extract channel references from a video's title and description.
        video should be a Video model with snippet.title and snippet.description.
        """
        text = f"{video.snippet.title} {video.snippet.description}"
        return ChannelReferenceExtractor.extract_all_references(text)
