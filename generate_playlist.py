import json

with open('channels.json', encoding='utf-8') as f:
    data = json.load(f)

lines = ['#EXTM3U']

for ch in data.get('bangladeshi', []):
    name = ch.get('name', '')
    url = ch.get('url', '')
    if url:
        lines.append(f'#EXTINF:-1 group-title="Bangladeshi",{name}')
        lines.append(url)

for ch in data.get('sports', []):
    name = ch.get('name', '')
    url = ch.get('url', '')
    if url:
        lines.append(f'#EXTINF:-1 group-title="Sports",{name}')
        lines.append(url)

with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print("playlist.m3u generated successfully!")
