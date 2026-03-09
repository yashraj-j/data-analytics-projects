from googleapiclient.discovery import build

# PUT YOUR API KEY HERE
API_KEY = "AIzaSyCxzTt-D0xC5URbHuOwy9RTamMmx2hLNxA"

# PUT THE CHANNEL ID HERE (ANI example)
CHANNEL_ID = "UCoRpKmC6a-DdEa1ohxlCgUA"

youtube = build("youtube", "v3", developerKey=API_KEY)

response = youtube.channels().list(
    part="contentDetails",
    id=CHANNEL_ID
).execute()

uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

print("UPLOADS PLAYLIST ID:")
print(uploads_playlist_id)
