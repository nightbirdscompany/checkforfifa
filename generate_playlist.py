import json
import requests
import os

# Your remote JSON URL
JSON_URL = "https://raw.githubusercontent.com/siamahmeed563-lab/Siam-areana/refs/heads/main/channels.json"

def generate_playlist_from_url():
    print("🌐 Fetching channels from GitHub...")
    
    try:
        # Fetch the JSON data from the URL
        response = requests.get(JSON_URL)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        print("✅ JSON data fetched successfully!")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON: {e}")
        return False

    if not data:
        print("❌ JSON data is empty!")
        return False
    
    lines = ['#EXTM3U']
    count = 0
    
    # Process the 'bangladeshi' group
    for ch in data.get('bangladeshi', []):
        name = ch.get('name', '').strip()
        url = ch.get('url', '').strip()
        if url and name:
            # You can optionally include icon/sub info in the name or as a comment
            # icon = ch.get('icon', '')
            # sub = ch.get('sub', '')
            # display_name = f"{name} {icon} {sub}" if icon or sub else name
            display_name = name
            lines.append(f'#EXTINF:-1 group-title="Bangladeshi",{display_name}')
            lines.append(url)
            count += 1

    # Process the 'sports' group
    for ch in data.get('sports', []):
        name = ch.get('name', '').strip()
        url = ch.get('url', '').strip()
        if url and name:
            # icon = ch.get('icon', '')
            # display_name = f"{name} {icon}" if icon else name
            display_name = name
            lines.append(f'#EXTINF:-1 group-title="Sports",{display_name}')
            lines.append(url)
            count += 1
    
    if count == 0:
        print("❌ No valid channels found with both name and URL!")
        return False
    
    # Write the playlist file
    try:
        with open('playlist.m3u', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        print(f"✅ playlist.m3u generated successfully with {count} channels!")
        return True
    except Exception as e:
        print(f"❌ Error writing playlist file: {e}")
        return False

if __name__ == "__main__":
    generate_playlist_from_url()
