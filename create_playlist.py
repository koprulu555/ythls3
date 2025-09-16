#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import glob

def create_master_playlist():
    """Tüm m3u8 dosyalarını içeren ana M3U playlist'ini oluşturur"""
    
    # Önce m3u8 klasörünü oluştur
    os.makedirs("m3u8", exist_ok=True)
    
    # channels.json'dan kanal isimlerini al
    try:
        with open("channels.json", "r", encoding="utf-8") as f:
            channels = json.load(f)
    except FileNotFoundError:
        print("❌ channels.json dosyası bulunamadı!")
        return False
    
    # M3U başlığı
    m3u_content = "#EXTM3U\n"
    
    # Önce mevcut m3u8 dosyalarını bul
    existing_m3u8_files = glob.glob("m3u8/*.m3u8")
    print(f"📁 Bulunan m3u8 dosyaları: {len(existing_m3u8_files)}")
    
    # Her kanal için M3U girişi oluştur
    added_channels = 0
    for channel in channels:
        name = channel.get("name")
        m3u8_file = f"m3u8/{name}.m3u8"
        
        # Eğer m3u8 dosyası varsa playlist'e ekle
        if os.path.exists(m3u8_file):
            # GitHub raw content URL'si
            repo_name = os.environ.get('GITHUB_REPOSITORY', 'kullanici/repo')
            branch = os.environ.get('GITHUB_REF', 'refs/heads/main').replace('refs/heads/', '')
            raw_url = f"https://raw.githubusercontent.com/{repo_name}/{branch}/{m3u8_file}"
            
            m3u_content += f"#EXTINF:-1, {name}\n"
            m3u_content += f"{raw_url}\n"
            added_channels += 1
            print(f"✅ Eklendi: {name}")
        else:
            print(f"⚠️ M3U8 dosyası bulunamadı: {m3u8_file}")
    
    # Playlist'i kaydet
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ Ana playlist oluşturuldu: playlist.m3u ({added_channels} kanal)")
    return added_channels > 0

if __name__ == "__main__":
    create_master_playlist()
