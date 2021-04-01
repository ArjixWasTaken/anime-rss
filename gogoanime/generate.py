import requests
import re
import os


def get_latest_by_type(type=1):
    headers = {
        'authority': 'ajax.gogo-load.com',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'accept': 'text/html, */*; q=0.01',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'origin': 'https://gogoanime.vc',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://gogoanime.vc/',
    }

    params = (
        ('page', '1'),
        ('type', str(type)),
    )

    response = requests.get(
        'https://ajax.gogo-load.com/ajax/page-recent-release.html', headers=headers, params=params).text

    regex = r"<li>\s*\n.*\n.*<a\s*href=[\"'](?P<href>.*?-episode-(?P<episode>\d+))[\"']\s*title=[\"'](?P<title>.*?)[\"']"
    matches = list(re.findall(regex, response, re.MULTILINE))
    return matches


def generate_rss_by_type(type=1):
    types = ['(Sub)', '(Dub)', '(Chinese)']
    rss = f"""
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
<title>Gogoanime {types[type-1]} - RSS Feed</title>
<link>https://github.com/ArjixGamer/anime-rss</link>
<description>A simple RSS feed for gogoanime!</description>
"""

    for item in get_latest_by_type(type):
        rss += """
<item>
    <title>{}</title>
    <link>{}</link>
    <description>{}</description>
</item>
""".format(f"{item[2]} - Episode {item[1]}", "https://gogoanime.vc" + item[0], f"Episode <strong>{item[1]}</strong> of <em>{item[2]}</em> is out!")

    rss += '\n</channel>\n</rss>'
    return rss


types = {
    'sub': 1,
    'dub': 2,
    'chinese': 3
}

for type_ in types:
    filename = f'./gogoanime/gogoanime-rss-{type_}.xml'
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        f.write(generate_rss_by_type(types[type_]).strip())
