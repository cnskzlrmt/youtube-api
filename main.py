import pandas as pd
from googleapiclient.discovery import build
from IPython.display import JSON
import matplotlib.pyplot as plt
import seaborn as sns

from config.config import YOUTUBE_API_KEY
from api_methods import collect_channel_stats, collect_video_ids, collect_video_details

api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=YOUTUBE_API_KEY)

# Channels to analyze
channel_ids = [
    "UCfqDD_iRsuThW8rERHNAJNA",

]
channel_stats = collect_channel_stats(youtube, channel_ids)
channel_stats['subscribers'] = pd.to_numeric(channel_stats['subscribers'], errors='coerce')
channel_stats['views'] = pd.to_numeric(channel_stats['views'], errors='coerce')
channel_stats['totalVideos'] = pd.to_numeric(channel_stats['totalVideos'], errors='coerce')


# Genel analiz için görüntüleme sayıları, abone sayıları ve video sayıları
print("Toplam Görüntülenme Sayısı:", channel_stats['views'].sum())
print("Toplam Abone Sayısı:", channel_stats['subscribers'].sum())
print("Toplam Video Sayısı:", channel_stats['totalVideos'].sum())

# Görselleştirme için seaborn kullanarak bar plot
plt.figure(figsize=(16, 10))

# Subplot 1: Toplam Görüntülenme Sayıları
plt.subplot(2, 2, 1)
sns.barplot(x='channelName', y='views', data=channel_stats, color='purple')
plt.title('Toplam Görüntülenme Sayıları')
plt.xticks(rotation=45, ha='right')

# Subplot 2: Toplam Abone Sayıları
plt.subplot(2, 2, 2)
sns.barplot(x='channelName', y='subscribers', data=channel_stats)
plt.title('Toplam Abone Sayıları')
plt.xticks(rotation=45, ha='right')


# Subplot 3: Toplam Video Sayıları
plt.subplot(2, 2, 3)
sns.barplot(x='channelName', y='totalVideos', data=channel_stats, color= 'orange')
plt.title('Toplam Video Sayıları')
plt.xticks(rotation=45, ha='right')

# Subplot 4: Video Detayları (örneğin: görüntülenmeler, beğeniler)
video_ids = collect_video_ids(youtube, channel_stats['playlistId'].iloc[0])
video_details = collect_video_details(youtube, video_ids)
video_details_df = pd.DataFrame(video_details)
plt.subplot(2, 2, 4)
sns.scatterplot(x='viewCount', y='likeCount', data=video_details_df, color='salmon')
plt.title('Video Görüntülenme ve Beğeni Sayıları')

# Grafikleri göster
plt.tight_layout()
plt.show()




