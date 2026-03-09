import pandas as pd
from datetime import date
from googleapiclient.discovery import build

API_KEY = "AIzaSyCxzTt-D0xC5URbHuOwy9RTamMmx2hLNxA"

youtube = build("youtube", "v3", developerKey=API_KEY)

videos = pd.read_csv("all_videos.csv")

rows = []
today = date.today().isoformat()

for i in range(0, len(videos), 50):
    batch = videos["video_id"].iloc[i:i+50].tolist()

    response = youtube.videos().list(
        part="statistics",
        id=",".join(batch)
    ).execute()

    for item in response["items"]:
        rows.append({
            "video_id": item["id"],
            "views": item["statistics"].get("viewCount", 0),
            "likes": item["statistics"].get("likeCount", 0),
            "comments": item["statistics"].get("commentCount", 0),
            "snapshot_date": today
        })

df = pd.DataFrame(rows)
df.to_csv("dim_src_youtube_video_stats.csv", index=False)

print("DONE: video stats snapshot created")
