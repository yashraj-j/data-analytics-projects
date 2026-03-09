import pandas as pd
from googleapiclient.discovery import build

# 1. PUT YOUR API KEY HERE
API_KEY = "AIzaSyCxzTt-D0xC5URbHuOwy9RTamMmx2hLNxA"

# 2. PUT THE UPLOADS PLAYLIST ID HERE
UPLOADS_PLAYLIST_ID = "UUoRpKmC6a-DdEa1ohxlCgUA"

youtube = build("youtube", "v3", developerKey=API_KEY)

rows = []
next_page_token = None

while True:
    response = youtube.playlistItems().list(
        part="snippet",
        playlistId=UPLOADS_PLAYLIST_ID,
        maxResults=50,
        pageToken=next_page_token
    ).execute()

    for item in response["items"]:
        rows.append({
            "video_id": item["snippet"]["resourceId"]["videoId"],
            "published_at": item["snippet"]["publishedAt"]
        })

    next_page_token = response.get("nextPageToken")

    if next_page_token is None:
        break

df = pd.DataFrame(rows)
df.to_csv("all_videos.csv", index=False)

print("DONE. Total videos fetched:", len(df))
