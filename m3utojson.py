import json
import os
import requests
import urllib.parse as urlparse
import time

# m3u8 klasörünü oluştur (zaten varsa hata vermez)
os.makedirs("m3u8", exist_ok=True)

# channels.json dosyasını oku
try:
    with open("channels.json", "r", encoding="utf-8") as f:
        channels = json.load(f)
except FileNotFoundError:
    print("❌ channels.json dosyası bulunamadı!")
    exit(1)

# Ortak YouTube API yapılandırması
headers = {
    'origin': 'https://www.youtube.com',
    'referer': 'https://www.youtube.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}
params = {
    'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
}
client_context = {
    'client': {
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36,gzip(gfe)',
        'clientName': 'WEB',
        'clientVersion': '2.20231101.05.00',
    }
}

# Video ID çıkarıcı
def extract_video_id(youtube_url):
    parsed = urlparse.urlparse(youtube_url)
    qs = urlparse.parse_qs(parsed.query)
    video_id = qs.get('v', [None])[0]
    if not video_id and 'youtu.be' in parsed.netloc:
        video_id = parsed.path.split('/')[-1]
    return video_id

# Her kanal için işlemleri gerçekleştir
success_count = 0
for channel in channels:
    name = channel.get("name")
    url = channel.get("url")

    print(f"⏳ İşleniyor: {name} - {url}")
    video_id = extract_video_id(url)
    if not video_id:
        print(f"❌ Video ID alınamadı: {url}")
        continue

    json_data = {
        'context': client_context,
        'videoId': video_id
    }

    try:
        response = requests.post(
            'https://www.youtube.com/youtubei/v1/player',
            params=params,
            headers=headers,
            json=json_data,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        hls_url = data.get("streamingData", {}).get("hlsManifestUrl")

        if not hls_url:
            print(f"⚠️ HLS manifest URL bulunamadı: {name}")
            continue

        # .m3u8 içeriğini indir
        hls_response = requests.get(hls_url, headers=headers, timeout=30)
        hls_response.raise_for_status()

        # Dosya yolunu oluştur ve kaydet
        filename = os.path.join("m3u8", f"{name}.m3u8")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(hls_response.text)

        print(f"✅ Kaydedildi: {filename}")
        success_count += 1

        # Kısa bir bekleme süresi (rate limiting için)
        time.sleep(1)

    except requests.RequestException as e:
        print(f"❌ Hata oluştu ({name}): {e}")

print(f"\n🎉 Toplam {success_count}/{len(channels)} kanal başarıyla işlendi.")
