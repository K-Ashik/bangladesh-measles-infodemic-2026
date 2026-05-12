import os
import time
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 1. SETUP
# --- PASTE YOUR API KEY HERE ---
API_KEY = "AIzaSyCmIZKhOAhlEYNAqe95r-RaNO3cX7Mj8fQ" 
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 2. THE GLOBAL QUERY
# Using OR operators to catch different variations of the topic
search_query = "হামের টিকা OR হাম রোগ OR measles outbreak bangladesh"

published_after = "2026-03-01T00:00:00Z"
published_before = "2026-05-15T00:00:00Z"

master_comments = []

print(f"Starting GLOBAL Digital Surveillance for: '{search_query}'...\n")

try:
    # Step A: Find the videos across ALL of YouTube
    search_request = youtube.search().list(
        part="id,snippet",
        q=search_query,
        publishedAfter=published_after,
        publishedBefore=published_before,
        type="video",
        relevanceLanguage="bn", # Force it to look for Bengali context
        maxResults=50 # Grab the top 50 most relevant videos globally
    )
    search_response = search_request.execute()
    
    videos = []
    for item in search_response.get('items', []):
        videos.append({
            'id': item['id']['videoId'],
            'channel': item['snippet']['channelTitle']
        })
        
    print(f" -> Found {len(videos)} videos globally. Extracting comments...")

    # Step B: Get the comments for each video
    for video in videos:
        video_id = video['id']
        channel_name = video['channel']
        
        try:
            comment_request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100, 
                order="relevance" 
            )
            comment_response = comment_request.execute()
            
            for item in comment_response.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']
                
                text = comment['textDisplay']
                # Keep only comments with Bengali characters
                if any(char in text for char in 'অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ'):
                    master_comments.append({
                        'Channel': channel_name,
                        'Video_ID': video_id,
                        'Author': comment['authorDisplayName'],
                        'Comment': text,
                        'Likes': comment['likeCount'],
                        'Published_At': comment['publishedAt']
                    })
            
            time.sleep(1) # API rate limit protection
            
        except HttpError as e:
            pass # Silently skip videos with disabled comments

except Exception as e:
     print(f"Error searching YouTube: {e}")

# 4. SAVE THE DATA
if master_comments:
    df = pd.DataFrame(master_comments)
    df = df.drop_duplicates(subset=['Comment', 'Author']) 
    df.to_csv("youtube_measles_comments.csv", index=False)
    print(f"\nSurveillance Complete! Extracted {len(df)} Bengali comments.")
    print("Saved to 'youtube_measles_comments.csv'.")
else:
    print("\nStill 0 comments. The API may be struggling to index recent Bengali videos.")