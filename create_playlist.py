#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

def create_master_playlist():
    """Tüm m3u8 dosyalarını içeren ana M3U playlist'ini oluşturur"""
    
    # channels.json'dan kanal isimlerini al
    with open("channels.json", "r", encoding="utf-8") as f:
        channels = json.load(f)
    
    # M3U başlığı
    m3u_content = "#EXTM3U\n"
    
    # Her kanal için M3U girişi oluştur
    for channel in channels:
        name = channel.get("name")
        m3u8_file = f"m3u8/{name}.m3u8"
        
        # Eğer m3u8 dosyası varsa playlist'e ekle
        if os.path.exists(m3u8_file):
            # GitHub raw content URL'si
            raw_url = f"https://raw.githubusercontent.com/{os.environ.get('GITHUB_REPOSITORY', 'kullanici/repo')}/main/{m3u8_file}"
            
            m3u_content += f"#EXTINF:-1, {name}\n"
            m3u_content += f"{raw_url}\n"
            print(f"✅ Eklendi: {name}")
        else:
            print(f"⚠️ M3U8 dosyası bulunamadı: {m3u8_file}")
    
    # Playlist'i kaydet
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ Ana playlist oluşturuldu: playlist.m3u ({len(channels)} kanal)")

if __name__ == "__main__":
    create_master_playlist()
