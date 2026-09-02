from pathlib import Path
from urllib.request import Request, urlopen

ASSETS = {
    "aviation": "https://images.unsplash.com/photo-1770334618960-d246fc142297?auto=format&fit=crop&fm=jpg&q=88&w=2600",
    "security": "https://images.pexels.com/photos/38702227/pexels-photo-38702227.jpeg?auto=compress&cs=tinysrgb&w=2200",
    "chef": "https://images.pexels.com/photos/12258207/pexels-photo-12258207.png?cs=srgb&dl=pexels-paolino96-12258207.jpg&fm=jpg",
    "wellness": "https://images.pexels.com/photos/35884502/pexels-photo-35884502.jpeg?cs=srgb&dl=pexels-marine-fougere-2159237528-35884502.jpg&fm=jpg",
    "bespoke": "https://images.pexels.com/photos/8387121/pexels-photo-8387121.jpeg?cs=srgb&dl=pexels-ron-lach-8387121.jpg&fm=jpg",
}

out = Path("_site/assets/images")
out.mkdir(parents=True, exist_ok=True)

for name, url in ASSETS.items():
    target = out / f"{name}.jpg"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 IbizaVIPMoveBuild/1.0"})
    with urlopen(req, timeout=30) as response:
        data = response.read()
    if len(data) < 50_000:
        raise SystemExit(f"Downloaded {name} image is unexpectedly small: {len(data)} bytes")
    target.write_bytes(data)
    print(f"Updated {name}: {len(data):,} bytes")

print("Secondary premium visual assets updated successfully.")
