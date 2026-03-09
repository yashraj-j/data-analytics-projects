import pandas as pd
from googleapiclient.discovery import build

API_KEY = "AIzaSyCxzTt-D0xC5URbHuOwy9RTamMmx2hLNxA"
youtube = build("youtube", "v3", developerKey=API_KEY)

channels = pd.read_csv("src_youtube_channel_list.csv")
rows = []

for cid in channels["channel_id"]:
    r = youtube.channels().list(
        part="snippet,statistics,brandingSettings,contentDetails,topicDetails",
        id=cid
    ).execute()

    if not r["items"]:
        continue

    it = r["items"][0]

    rows.append({
        "channel_id": it["id"],
        "channel_title": it["snippet"].get("title"),
        "channel_description": it["snippet"].get("description"),
        "channel_published_at": it["snippet"].get("publishedAt"),
        "country": it["snippet"].get("country"),

        "subscriber_count": it["statistics"].get("subscriberCount"),
        "view_count": it["statistics"].get("viewCount"),
        "video_count": it["statistics"].get("videoCount"),

        "uploads_playlist_id": it["contentDetails"]["relatedPlaylists"]["uploads"],

        "keywords": it.get("brandingSettings", {})
                        .get("channel", {})
                        .get("keywords"),

        "topic_categories": ",".join(
            it.get("topicDetails", {}).get("topicCategories", [])
        )
    })

pd.DataFrame(rows).to_csv(
    "dim_src_all_youtube_channel_metadata.csv",
    index=False
)

print("DONE: enriched channel metadata")
