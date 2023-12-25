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
# Channel stats'ları çek
channel_stats = collect_channel_stats(youtube, channel_ids)

# Görüntüleme sayıları, abone sayıları ve video sayıları üzerine genel analiz
print("Toplam Görüntülenme Sayısı:", channel_stats['views'].sum())
print("Toplam Abone Sayısı:", channel_stats['subscribers'].sum())
print("Toplam Video Sayısı:", channel_stats['totalVideos'].sum())

# Görselleştirme için seaborn kullanarak bar plot
plt.figure(figsize=(12, 6))
sns.barplot(x='channelName', y='views', data=channel_stats)
plt.title('Kanal Görüntülenme Sayıları')
plt.xticks(rotation=45, ha='right')
plt.show()


