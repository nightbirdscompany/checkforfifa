import json
import requests
import sys

JSON_URL = "https://raw.githubusercontent.com/siamahmeed563-lab/Siam-areana/refs/heads/main/channels.json"

def generate_playlist():
    print("🌐 Fetching channels from GitHub...")
    print(f"URL: {JSON_URL}")
    
    try:
        response = requests.get(JSON_URL, timeout=10)
        print(f"Status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        print(f"✅ Success! Found {len(data.get('bangladeshi', []))} Bangladeshi channels and {len(data.get('sports', []))} sports channels")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    lines = ['#EXTM3U']
    count = 0
    
    for group in ['bangladeshi', 'sports']:
        channels = data.get(group, [])
        print(f"Processing {len(channels)} channels in '{group}' group")
        for ch in channels:
            name = ch.get('name', '').strip()
            url = ch.get('url', '').strip()
            if url and name:
                group_title = group.capitalize()
                lines.append(f'#EXTINF:-1 group-title="{group_title}",{name}')
                lines.append(url)
                count += 1
    
    print(f"Added {count} valid channels")
    
    if count == 0:
        print("❌ No valid channels found!")
        return False
    
    try:
        with open('playlist.m3u', 'w', encoding='utf-8') as f:
            content = '\n'.join(lines) + '\n'
            f.write(content)
        print(f"✅ playlist.m3u generated with {count} channels!")
        print(f"File size: {len(content)} bytes")
        return True
    except Exception as e:
        print(f"❌ Error writing playlist: {e}")
        return False

if __name__ == "__main__":
    success = generate_playlist()
    sys.exit(0 if success else 1)
