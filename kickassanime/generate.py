import requests
import re
import os

rss = """
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
<title>KickassAnime - RSS Feed</title>
<link>https://github.com/ArjixGamer/anime-rss</link>
<description>A simple cleaned RSS feed for kickassanime!</description>
"""

html = requests.get('https://www2.kickassanime.ro/feed/latest')
rss += re.sub(r'[.A-Za-z"><0-9\s\v\n\r?\/-:-,+=]+\/height>[\n\s]+<\/image>|[\s]+<guid.+guid>', '', html.text)

try:
    filename = f'./kickassanime/kickassanime-rss.xml'
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        f.write(rss.strip())
except:
    print('KickassAnime failed.')
