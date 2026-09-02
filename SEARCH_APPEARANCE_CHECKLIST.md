# Search appearance checklist

After deployment:

1. Confirm https://ibizavipmove.com/favicon.png returns the PNG icon.
2. Confirm the homepage head contains `rel="icon"` pointing to `/favicon.png`.
3. Confirm the homepage and Private Office retain absolute `og:image` URLs.
4. Inspect the homepage in Google Search Console and request recrawl once.
5. Allow Google time to recrawl; favicon changes are not guaranteed to appear immediately.
6. Keep the favicon URL stable on future releases.
