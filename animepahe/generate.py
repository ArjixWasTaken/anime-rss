import requests
import json
import re
import os


def get_latest():
    link = 'https://animepahe.com/api?m=airing&page=1'

    response = requests.get(link).json()

    return [
        [
            '{}/{}'.format(x['anime_session'], x['session']),
            x['episode'],
            x['anime_title']
        ] for x in response['data']
    ]


def generate_rss():
    rss = f"""
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
<title>AnimePahe - RSS Feed</title>
<link>https://github.com/ArjixGamer/gogoanime-rss</link>
<description>A simple RSS feed for animepahe!</description>
"""

    for item in get_latest():
        rss += """
<item>
    <title>{}</title>
    <link>{}</link>
    <description>{}</description>
</item>
""".format(f"{item[2]} - Episode {item[1]}", "https://animepahe.com/play/" + item[0], f"Episode <strong>{item[1]}</strong> of <em>{item[2]}</em> is out!")

    rss += '\n</channel>\n</rss>'
    return rss


filename = f'./animepahe/animepahe-rss.xml'
if os.path.exists(filename):
    os.remove(filename)
with open(filename, 'w') as f:
    f.write(generate_rss().strip())
