import json
import subprocess
import os

# m3u8 klasörünü oluştur
os.makedirs("m3u8", exist_ok=True)

with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

for channel in channels:
    name = channel.get("name")
    url = channel.get("url")

    print(f"⏳ İşleniyor: {name} - {url}")

    try:
        result = subprocess.run(
            ["yt-dlp", "-g", "-f", "best", url],
            capture_output=True,
            text=True,
            check=True
        )
        m3u8_url = result.stdout.strip()
        if m3u8_url.startswith("http"):
            # Doğrudan HLS URL'sini içeren basit bir m3u8 dosyası oluştur
            with open(f"m3u8/{name}.m3u8", "w", encoding="utf-8") as f_out:
                f_out.write("#EXTM3U\n")
                f_out.write(f"#EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION=1920x1080\n")
                f_out.write(m3u8_url + "\n")
            print(f"✅ Kaydedildi: m3u8/{name}.m3u8")
        else:
            print(f"⚠️ Geçersiz çıktı: {name}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Hata oluştu ({name}): {e.stderr.strip()}")
