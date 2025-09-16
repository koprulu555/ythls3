import json
import subprocess
import os
import time

# m3u8 klasörünü oluştur
os.makedirs("m3u8", exist_ok=True)

# channels.json dosyasını oku
try:
    with open("channels.json", "r", encoding="utf-8") as f:
        channels = json.load(f)
except FileNotFoundError:
    print("❌ channels.json dosyası bulunamadı!")
    exit(1)

success_count = 0
for channel in channels:
    name = channel.get("name")
    url = channel.get("url")

    print(f"⏳ İşleniyor: {name} - {url}")

    try:
        result = subprocess.run(
            ["yt-dlp", "-g", "-f", "best", url],
            capture_output=True,
            text=True,
            timeout=30,
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
            success_count += 1
        else:
            print(f"⚠️ Geçersiz çıktı: {name}")

        # Kısa bir bekleme süresi
        time.sleep(1)

    except subprocess.CalledProcessError as e:
        print(f"❌ Hata oluştu ({name}): {e.stderr.strip()}")
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: {name}")

print(f"\n🎉 Toplam {success_count}/{len(channels)} kanal başarıyla işlendi.")
