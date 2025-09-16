#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

def create_m3u_playlist():
    """channels.json'daki kanalları kullanarak M3U playlist oluşturur"""
    
    # channels.json dosyasını oku
    try:
        with open("channels.json", "r", encoding="utf-8") as f:
            channels = json.load(f)
    except FileNotFoundError:
        print("❌ channels.json dosyası bulunamadı!")
        return False
    
    # M3U başlığı
    m3u_content = "#EXTM3U\n"
    m3u_content += "#EXT-X-VERSION:3\n"
    m3u_content += f"#EXT-X-PLAYLIST-TYPE:VOD\n"
    m3u_content += f"#EXT-X-TARGETDURATION:10\n"
    m3u_content += f"#EXT-X-MEDIA-SEQUENCE:1\n"
    
    # Her kanal için M3U girişi oluştur
    for channel in channels:
        name = channel.get("name", "Bilinmeyen Kanal")
        url = channel.get("url", "")
        
        if not url:
            print(f"⚠️ URL bulunamadı: {name}")
            continue
        
        # M3U formatında kanal bilgisi
        m3u_content += f'#EXTINF:-1 tvg-id="{name.replace(" ", "")}" tvg-name="{name}" group-title="YouTube",{name}\n'
        m3u_content += f"{url}\n"
    
    # M3U playlist sonu
    m3u_content += "#EXT-X-ENDLIST\n"
    
    # Dosyaya yaz
    with open("youtube_live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ M3U playlist oluşturuldu: youtube_live.m3u ({len(channels)} kanal)")
    return True

def create_simple_m3u():
    """Basit M3U formatında playlist oluşturur (VLC ve diğer oynatıcılar için)"""
    
    try:
        with open("channels.json", "r", encoding="utf-8") as f:
            channels = json.load(f)
    except FileNotFoundError:
        print("❌ channels.json dosyası bulunamadı!")
        return False
    
    # Basit M3U formatı
    m3u_content = "#EXTM3U\n"
    
    for channel in channels:
        name = channel.get("name", "Bilinmeyen Kanal")
        url = channel.get("url", "")
        
        if not url:
            continue
        
        m3u_content += f"#EXTINF:-1, {name}\n"
        m3u_content += f"{url}\n"
    
    with open("youtube_simple.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ Basit M3U playlist oluşturuldu: youtube_simple.m3u ({len(channels)} kanal)")
    return True

if __name__ == "__main__":
    print("M3U playlist'ler oluşturuluyor...")
    create_m3u_playlist()
    create_simple_m3u()
    print("İşlem tamamlandı!")
