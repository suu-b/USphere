from lib.youtube import YouTubeClient
from shared.models import ChannelWithVideos
from shared.channel_extractor import ChannelReferenceExtractor
from dotenv import load_dotenv
import os
import pprint

import json

load_dotenv()
client = YouTubeClient(api_key=os.getenv('YOUTUBE_API_KEY'))

with open('./discovery/data/seed.json', 'r') as f:
    seed = json.load(f)

# Track discovered channels by canonical channel ID to avoid duplicates
discovered_channel_ids = set()

# Core: Process seeded channels
print("=" * 60)
print("CORE: Processing seeded channels")
print("=" * 60)

core_channels = []
for channel in seed['channels']:
    handle = channel['handle']
    print(f"\nProcessing seeded channel: {handle}")
    
    try:
        channel_model = client.get_channel_metadata_by_handle(handle)
    except Exception as e:
        print(f"  Error fetching channel {handle}: {e}")
        continue
    
    # Check if already discovered by canonical ID
    canonical_id = channel_model.id
    if canonical_id in discovered_channel_ids:
        print(f"  Channel {handle} (ID: {canonical_id}) already discovered, skipping")
        continue
    
    uploads_playlist_id = channel_model.contentDetails.relatedPlaylists.uploads
    
    try:
        # Start with 50 videos per channel to limit API usage
        video_ids = client.get_playlist_video_ids_limited(uploads_playlist_id, max_videos=50)
        video_models = client.get_videos_metadata(video_ids)
    except Exception as e:
        print(f"  Error fetching videos for channel {handle}: {e}")
        continue
    
    # Extract channel references from videos
    all_references = set()
    for video in video_models:
        try:
            refs = ChannelReferenceExtractor.extract_from_video(video)
            all_references.update(refs)
        except Exception as e:
            print(f"  Error extracting references from video {video.id}: {e}")
            continue
    
    print(f"  Found {len(all_references)} channel references in videos")
    for ref in all_references:
        print(f"    - {ref}")
    
    core_channels.append({
        'handle': handle,
        'channel': channel_model.model_dump(),
        'videos': [video.model_dump() for video in video_models],
        'references': list(all_references)
    })
    
    discovered_channel_ids.add(canonical_id)

# Mantle: Process channels found in core descriptions
print("\n" + "=" * 60)
print("MANTLE: Processing channels from core descriptions")
print("=" * 60)

mantle_channels = []
for core_data in core_channels:
    for ref in core_data['references']:
        # Determine if it's a handle or channel ID
        if ref.startswith('@'):
            print(f"\nProcessing discovered channel (handle): {ref}")
            try:
                channel_model = client.get_channel_metadata_by_handle(ref)
            except Exception as e:
                print(f"  Error fetching channel {ref}: {e}")
                continue
        else:
            print(f"\nProcessing discovered channel (ID): {ref}")
            try:
                channel_model = client.get_channel_metadata(ref)
            except Exception as e:
                print(f"  Error fetching channel {ref}: {e}")
                continue
        
        # Check if already discovered by canonical ID
        canonical_id = channel_model.id
        if canonical_id in discovered_channel_ids:
            print(f"  Channel {ref} (ID: {canonical_id}) already discovered, skipping")
            continue
        
        uploads_playlist_id = channel_model.contentDetails.relatedPlaylists.uploads
        
        try:
            # Start with 50 videos per channel to limit API usage
            video_ids = client.get_playlist_video_ids_limited(uploads_playlist_id, max_videos=50)
            video_models = client.get_videos_metadata(video_ids)
        except Exception as e:
            print(f"  Error fetching videos for channel {ref}: {e}")
            continue
        
        # Extract channel references from videos
        all_references = set()
        for video in video_models:
            try:
                refs = ChannelReferenceExtractor.extract_from_video(video)
                all_references.update(refs)
            except Exception as e:
                print(f"  Error extracting references from video {video.id}: {e}")
                continue
        
        print(f"  Found {len(all_references)} channel references in videos")
        for ref in all_references:
            print(f"    - {ref}")
        
        mantle_channels.append({
            'reference': ref,
            'channel': channel_model.model_dump(),
            'videos': [video.model_dump() for video in video_models],
            'references': list(all_references)
        })
        
        discovered_channel_ids.add(canonical_id)

# Crust: Process channels found in mantle descriptions
print("\n" + "=" * 60)
print("CRUST: Processing channels from mantle descriptions")
print("=" * 60)

crust_channels = []
for mantle_data in mantle_channels:
    for ref in mantle_data['references']:
        # Determine if it's a handle or channel ID
        if ref.startswith('@'):
            print(f"\nProcessing discovered channel (handle): {ref}")
            try:
                channel_model = client.get_channel_metadata_by_handle(ref)
            except Exception as e:
                print(f"  Error fetching channel {ref}: {e}")
                continue
        else:
            print(f"\nProcessing discovered channel (ID): {ref}")
            try:
                channel_model = client.get_channel_metadata(ref)
            except Exception as e:
                print(f"  Error fetching channel {ref}: {e}")
                continue
        
        # Check if already discovered by canonical ID
        canonical_id = channel_model.id
        if canonical_id in discovered_channel_ids:
            print(f"  Channel {ref} (ID: {canonical_id}) already discovered, skipping")
            continue
        
        uploads_playlist_id = channel_model.contentDetails.relatedPlaylists.uploads
        
        try:
            # Start with 50 videos per channel to limit API usage
            video_ids = client.get_playlist_video_ids_limited(uploads_playlist_id, max_videos=50)
            video_models = client.get_videos_metadata(video_ids)
        except Exception as e:
            print(f"  Error fetching videos for channel {ref}: {e}")
            continue
        
        # Extract channel references from videos
        all_references = set()
        for video in video_models:
            try:
                refs = ChannelReferenceExtractor.extract_from_video(video)
                all_references.update(refs)
            except Exception as e:
                print(f"  Error extracting references from video {video.id}: {e}")
                continue
        
        print(f"  Found {len(all_references)} channel references in videos")
        for ref in all_references:
            print(f"    - {ref}")
        
        crust_channels.append({
            'reference': ref,
            'channel': channel_model.model_dump(),
            'videos': [video.model_dump() for video in video_models],
            'references': list(all_references)
        })
        
        discovered_channel_ids.add(canonical_id)

# Save to files
print("\n" + "=" * 60)
print("Saving data to files")
print("=" * 60)

try:
    with open('./discovery/data/core.json', 'w') as f:
        json.dump(core_channels, f, indent=2)
    print(f"Saved {len(core_channels)} channels to core.json")
except Exception as e:
    print(f"Error saving core.json: {e}")

try:
    with open('./discovery/data/mantle.json', 'w') as f:
        json.dump(mantle_channels, f, indent=2)
    print(f"Saved {len(mantle_channels)} channels to mantle.json")
except Exception as e:
    print(f"Error saving mantle.json: {e}")

try:
    with open('./discovery/data/crust.json', 'w') as f:
        json.dump(crust_channels, f, indent=2)
    print(f"Saved {len(crust_channels)} channels to crust.json")
except Exception as e:
    print(f"Error saving crust.json: {e}")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Core (seeded): {len(core_channels)} channels")
print(f"Mantle (from core): {len(mantle_channels)} channels")
print(f"Crust (from mantle): {len(crust_channels)} channels")
print(f"Total unique channels discovered: {len(discovered_channel_ids)}")


