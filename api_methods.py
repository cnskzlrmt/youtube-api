import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import pandas as pd

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # Örneğin, belirli bir kanalın istatistiklerini almak için
    channel_ids = ["UCfqDD_iRsuThW8rERHNAJNA"]
    channel_stats = collect_channel_stats(youtube, channel_ids)
    print(channel_stats)

    # Örneğin, belirli bir çalma listesindeki videoların detaylarını almak için
    playlist_id = "UUfqDD_iRsuThW8rERHNAJNA"
    video_ids = collect_video_ids(youtube, playlist_id)
    video_details = collect_video_details(youtube, video_ids)
    print(video_details)

def collect_channel_stats(youtube, channel_ids):
    all_data = []

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=",".join(channel_ids)
    )

    response = request.execute()

    # loop through items in response
    for item in response["items"]:
        data = {'channelName': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'totalVideos': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
        }
        all_data.append(data)

    # Dönen liste verisini bir DataFrame'e dönüştür
    return pd.DataFrame(all_data)


def collect_video_ids(youtube, playlist_id):
    video_ids = []

    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])

    return video_ids

def collect_video_details(youtube, video_ids):
    all_video_info = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:
            stats_to_keep = {
                'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                'statistics': ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'],
                'contentDetails': ['duration', 'definition', 'caption']
            }
            video_info = {'video_id': video['id']}

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)

    return all_video_info

if __name__ == "__main__":
    main()
