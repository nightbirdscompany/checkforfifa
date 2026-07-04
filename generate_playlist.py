import json
import requests
import sys
import os

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
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"Response content preview: {response.text[:200]}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
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
                # Clean up URL - remove any trailing spaces
                url = url.strip()
                lines.append(f'#EXTINF:-1 group-title="{group_title}",{name}')
                lines.append(url)
                count += 1
    
    print(f"Added {count} valid channels")
    
    if count == 0:
        print("❌ No valid channels found!")
        return False
    
    try:
        # Create the content
        content = '\n'.join(lines) + '\n'
        
        # Write to file
        with open('playlist.m3u', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ playlist.m3u generated with {count} channels!")
        print(f"File size: {len(content)} bytes")
        
        # Verify file was created
        if os.path.exists('playlist.m3u'):
            print(f"✅ File exists at: {os.path.abspath('playlist.m3u')}")
            return True
        else:
            print("❌ File was not created!")
            return False
            
    except Exception as e:
        print(f"❌ Error writing playlist: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Starting playlist generation...")
    print("=" * 50)
    
    success = generate_playlist()
    
    print("=" * 50)
    if success:
        print("✅ SUCCESS! Playlist generated.")
        sys.exit(0)
    else:
        print("❌ FAILED! Playlist not generated.")
        sys.exit(1)
