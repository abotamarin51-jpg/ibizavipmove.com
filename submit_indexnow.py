from pathlib import Path
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

ROOT = Path('_site')
HOST = 'ibizavipmove.com'
KEY = '5be4dcbeb9a5378b495d37e469e1b27f'
KEY_LOCATION = f'https://{HOST}/{KEY}.txt'
ENDPOINT = 'https://api.indexnow.org/indexnow'

sitemap = ROOT / 'sitemap.xml'
tree = ET.parse(sitemap)
root = tree.getroot()
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [loc.text.strip() for loc in root.findall('sm:url/sm:loc', ns) if loc.text]

payload = json.dumps({
    'host': HOST,
    'key': KEY,
    'keyLocation': KEY_LOCATION,
    'urlList': urls,
}).encode('utf-8')

request = urllib.request.Request(
    ENDPOINT,
    data=payload,
    headers={'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'IbizaVIPMove-IndexNow/1.0'},
    method='POST',
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        code = response.getcode()
        print(f'IndexNow submission received HTTP {code} for {len(urls)} URLs.')
except urllib.error.HTTPError as exc:
    # Discovery notification must never roll back an otherwise healthy site deployment.
    print(f'IndexNow returned HTTP {exc.code}; deployment remains successful.')
except Exception as exc:
    print(f'IndexNow notification unavailable ({exc}); deployment remains successful.')
