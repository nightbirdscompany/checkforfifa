import json
import requests
import os

JSON_URL = "https://raw.githubusercontent.com/siamahmeed563-lab/Siam-areana/refs/heads/main/channels.json"

def generate_playlist_from_url():
    print("🌐 Fetching channels from GitHub...")
    
    try:
        response = requests.get(JSON_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("✅ JSON data fetched successfully!")
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON: {e}")
        return False

    lines = ['#EXTM3U']
    count = 0
    
    for group in ['bangladeshi', 'sports']:
        channels = data.get(group, [])
        for ch in channels:
            name = ch.get('name', '').strip()
            url = ch.get('url', '').strip()
            if url and name:
                group_title = group.capitalize()
                lines.append(f'#EXTINF:-1 group-title="{group_title}",{name}')
                lines.append(url)
                count += 1
    
    if count == 0:
        print("❌ No valid channels found!")
        return False
    
    try:
        with open('playlist.m3u', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        print(f"✅ playlist.m3u generated with {count} channels!")
        return True
    except Exception as e:
        print(f"❌ Error writing playlist: {e}")
        return False

if __name__ == "__main__":
    success = generate_playlist_from_url()
    exit(0 if success else 1)
