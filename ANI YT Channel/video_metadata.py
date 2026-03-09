import pandas as pd
from googleapiclient.discovery import build

API_KEY = "AIzaSyCxzTt-D0xC5URbHuOwy9RTamMmx2hLNxA"

youtube = build("youtube", "v3", developerKey=API_KEY)

videos = pd.read_csv("all_videos.csv")

rows = []

for i in range(0, len(videos), 50):
    batch = videos["video_id"].iloc[i:i+50].tolist()

    response = youtube.videos().list(
        part="snippet,contentDetails,topicDetails",
        id=",".join(batch)
    ).execute()

    for item in response["items"]:
        rows.append({
            "video_id": item["id"],
            "channel_id": item["snippet"]["channelId"],
            "title": item["snippet"]["title"],
            "published_at": item["snippet"]["publishedAt"],
            "duration": item["contentDetails"]["duration"],
            "category_id": item["snippet"].get("categoryId")
        })

df = pd.DataFrame(rows)
df.to_csv("dim_src_all_youtube_videos_metadata.csv", index=False)

print("DONE: video metadata file created")
