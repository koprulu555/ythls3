import json
import subprocess
import os
import time
import requests

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

def get_hls_with_ytdlp(url):
    """yt-dlp ile HLS manifest URL'sini alır"""
    try:
        # yt-dlp ile HLS manifest URL'sini al
        result = subprocess.run(
            ["yt-dlp", "-g", "-f", "best", url],
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )
        
        hls_url = result.stdout.strip()
        if hls_url and hls_url.startswith("http"):
            # HLS manifest içeriğini indir
            response = requests.get(hls_url, timeout=30)
            response.raise_for_status()
            return response.text
        
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"❌ yt-dlp hatası: {e.stderr.strip()}")
        return None
    except subprocess.TimeoutExpired:
        print("⏰ yt-dlp timeout!")
        return None
    except Exception as e:
        print(f"❌ İndirme hatası: {e}")
        return None

# Her kanal için işlemleri gerçekleştir
success_count = 0
for channel in channels:
    name = channel.get("name")
    url = channel.get("url")

    print(f"\n⏳ İşleniyor: {name}")
    print(f"🔗 URL: {url}")
    
    # HLS manifest'ini al
    hls_content = get_hls_with_ytdlp(url)
    
    if hls_content:
        # Dosyayı kaydet
        filename = os.path.join("m3u8", f"{name}.m3u8")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(hls_content)
        
        # Dosya içeriğini kontrol et
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            line_count = len(content.split('\n'))
        
        print(f"✅ Kaydedildi: {filename} ({line_count} satır)")
        success_count += 1
    else:
        print(f"❌ HLS manifest alınamadı: {name}")
    
    # Kısa bir bekleme süresi
    time.sleep(2)

print(f"\n🎉 İşlem tamamlandı! {success_count}/{len(channels)} kanal başarıyla güncellendi.")
