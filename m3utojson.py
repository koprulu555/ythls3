import json
import os
import requests
import urllib.parse as urlparse
import time
from datetime import datetime

# m3u8 klasörünü oluştur
os.makedirs("m3u8", exist_ok=True)

# channels.json dosyasını oku
try:
    with open("channels.json", "r", encoding="utf-8") as f:
        channels = json.load(f)
    print(f"✅ {len(channels)} kanal yüklendi")
except FileNotFoundError:
    print("❌ channels.json dosyası bulunamadı!")
    exit(1)

# YouTube API yapılandırması
headers = {
    'origin': 'https://www.youtube.com',
    'referer': 'https://www.youtube.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

client_context = {
    'context': {
        'client': {
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'clientName': 'WEB',
            'clientVersion': '2.20240201.00.00',
        }
    }
}

def extract_video_id(youtube_url):
    """YouTube URL'sinden video ID'sini çıkarır"""
    parsed = urlparse.urlparse(youtube_url)
    qs = urlparse.parse_qs(parsed.query)
    video_id = qs.get('v', [None])[0]
    if not video_id and 'youtu.be' in parsed.netloc:
        video_id = parsed.path.split('/')[-1]
    return video_id

def get_hls_manifest(video_id):
    """YouTube API'sinden HLS manifest URL'sini alır"""
    try:
        # YouTube API endpoint'i
        api_url = "https://www.youtube.com/youtubei/v1/player"
        
        # API isteği için gerekli parametreler
        params = {
            'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
            'prettyPrint': 'false'
        }
        
        # İstek gövdesi
        request_body = {
            'context': client_context['context'],
            'videoId': video_id,
            'params': '8AEB'  # Live stream parametresi
        }
        
        response = requests.post(
            api_url,
            params=params,
            headers=headers,
            json=request_body,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        
        # HLS manifest URL'sini bul
        streaming_data = data.get('streamingData', {})
        hls_url = streaming_data.get('hlsManifestUrl')
        
        if hls_url:
            # HLS manifest içeriğini indir
            hls_response = requests.get(hls_url, headers=headers, timeout=30)
            hls_response.raise_for_status()
            return hls_response.text
        
        return None
        
    except Exception as e:
        print(f"❌ API hatası: {e}")
        return None

# Her kanal için işlemleri gerçekleştir
success_count = 0
for channel in channels:
    name = channel.get("name")
    url = channel.get("url")

    print(f"\n⏳ İşleniyor: {name}")
    video_id = extract_video_id(url)
    
    if not video_id:
        print(f"❌ Video ID alınamadı: {url}")
        continue

    print(f"📹 Video ID: {video_id}")
    
    # HLS manifest'ini al
    hls_content = get_hls_manifest(video_id)
    
    if hls_content:
        # Dosyayı kaydet
        filename = os.path.join("m3u8", f"{name}.m3u8")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(hls_content)
        
        print(f"✅ Kaydedildi: {filename}")
        success_count += 1
    else:
        print(f"❌ HLS manifest alınamadı: {name}")
    
    # Kısa bir bekleme süresi (rate limiting için)
    time.sleep(2)

print(f"\n🎉 İşlem tamamlandı! {success_count}/{len(channels)} kanal başarıyla güncellendi.")
