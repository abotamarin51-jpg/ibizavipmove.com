from pathlib import Path
from html import unescape
import re

p=Path('_site/ar/ibiza-intelligence/index.html')
if not p.exists(): raise SystemExit('Arabic Black Book hub missing')
text=p.read_text(encoding='utf-8')
desc='دليل تخطيط خاص في إيبيزا يغطي الوصول والفلل واليخوت وموسم أغسطس والحياة الليلية والطيران وتنسيق تفاصيل الإقامة الفاخرة.'
text=re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")',lambda m:m.group(1)+desc+m.group(2),text,count=1,flags=re.I)
for attr,key in [('property','og:description'),('name','twitter:description')]:
    pat=rf'(<meta\s+{attr}="{re.escape(key)}"\s+content=")[^"]*(")'
    if re.search(pat,text,re.I): text=re.sub(pat,lambda m:m.group(1)+desc+m.group(2),text,count=1,flags=re.I)
p.write_text(text,encoding='utf-8')
m=re.search(r'<meta\s+name="description"\s+content="([^"]+)"',text,re.I)
assert m and len(unescape(m.group(1)).strip())>=50
print('PASS: Phase 71 Arabic Black Book metadata strengthened')