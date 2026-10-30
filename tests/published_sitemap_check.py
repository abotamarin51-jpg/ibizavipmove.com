"""Read the published sitemap once; never submit, deploy, or send Analytics."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

ORIGIN = 'https://ibizavipmove.com'
URL = ORIGIN + '/sitemap.xml'
DMC = ORIGIN + '/destination-management-ibiza/'
NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
MAX_BYTES = 2 * 1024 * 1024


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate(body: bytes) -> dict:
    if not body or len(body) > MAX_BYTES:
        raise ValueError('Empty or oversized sitemap')
    text = body.decode('utf-8-sig')
    if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        raise ValueError('DTD/entity declarations are not permitted')
    root = ET.fromstring(text)
    if root.tag != NS + 'urlset':
        raise ValueError('Expected a sitemap urlset')
    entries = {}
    today = datetime.now(ZoneInfo('Europe/Madrid')).date()
    for item in root:
        if item.tag != NS + 'url' or len(item.findall(NS + 'loc')) != 1:
            raise ValueError('Invalid sitemap URL entry')
        loc = item.findtext(NS + 'loc') or ''
        parts = urlsplit(loc)
        if (parts.scheme != 'https' or parts.netloc != 'ibizavipmove.com'
                or parts.query or parts.fragment or not parts.path.startswith('/')):
            raise ValueError('Unexpected sitemap origin or noncanonical location')
        if loc in entries or len(item.findall(NS + 'lastmod')) > 1:
            raise ValueError('Duplicate sitemap location or lastmod')
        lastmod = item.findtext(NS + 'lastmod')
        if lastmod is not None:
            if datetime.fromisoformat(lastmod.replace('Z', '+00:00')).date() > today:
                raise ValueError('Future lastmod')
        entries[loc] = lastmod
    if not entries or not entries.get(DMC):
        raise ValueError('DMC location with lastmod is required')
    return {'urlCount': len(entries), 'dmcLastmod': entries[DMC],
            'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def self_test():
    sample = (f'<urlset xmlns="{NS[1:-1]}"><url><loc>{DMC}</loc>'
              '<lastmod>2026-10-18</lastmod></url></urlset>').encode()
    result = validate(sample)
    assert result['urlCount'] == 1 and result['dmcLastmod'] == '2026-10-18'
    bad = [b'', b'x' * (MAX_BYTES + 1), b'<html/>', b'<urlset',
           b'<!DOCTYPE x>' + sample,
           sample.replace(b'ibizavipmove.com', b'example.com'),
           sample.replace(b'https://', b'http://'),
           sample.replace(b'2026-10-18', b'2999-10-18'),
           sample.replace(b'<lastmod>2026-10-18</lastmod>', b''),
           sample.replace(b'</urlset>', sample.split(b'>', 1)[1]),
           sample.replace(b'/</loc>', b'/?utm_source=test</loc>')]
    for body in bad:
        try:
            validate(body)
        except (ValueError, ET.ParseError):
            pass
        else:
            raise AssertionError('Invalid sitemap accepted')
    assert NoRedirect().redirect_request(None, None, 302, '', {}, 'https://example.com') is None
    print(f'PASS: published-sitemap validator, {len(bad) + 2} offline cases; no network requests')


def verify():
    output = Path(os.environ.get('RUNNER_TEMP', '/tmp')) / 'ivm-dmc-context-review'
    if output.resolve().is_relative_to(Path('_site').resolve()):
        raise ValueError('Evidence cannot enter website output')
    output.mkdir(parents=True, exist_ok=True)
    report = {'checkedAt': datetime.now(ZoneInfo('Europe/Madrid')).isoformat(),
              'verificationSourceCommit': os.environ.get('GITHUB_SHA'),
              'url': URL, 'method': 'GET', 'status': 'NOT_RUN',
              'limitation': 'Public HTTP/XML evidence, not a Google crawl or indexing result.'}
    try:
        request = Request(URL, headers={'Accept': 'application/xml, text/xml',
                                       'User-Agent': 'IbizaVIPMove-ReadOnlyVerification/1.0'})
        with build_opener(NoRedirect()).open(request, timeout=20) as response:
            report.update(httpStatus=response.status, finalUrl=response.url,
                          contentType=response.headers.get('Content-Type'))
            if response.status != 200 or response.url != URL:
                raise ValueError('Expected HTTP 200 at the exact approved URL')
            body = response.read(MAX_BYTES + 1)
        report.update(validate(body))
        (output / 'served-sitemap.xml').write_bytes(body)
        report['status'] = 'PASS'
    except Exception as err:
        report.update(status='FAILED_OR_BLOCKED', error=f'{type(err).__name__}: {err}')
        raise
    finally:
        (output / 'sitemap-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print('PUBLISHED_SITEMAP_REPORT ' + json.dumps(report), flush=True)
    return report


def validate_home_vip(home: bytes, target: bytes, require_link: bool) -> dict:
    from html.parser import HTMLParser

    class Document(HTMLParser):
        def __init__(self, body):
            super().__init__()
            self.links, self.canonicals, self.current, self.label = [], [], None, []
            self.headings = 0
            self.feed(body.decode('utf-8'))

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == 'a':
                self.current, self.label = attrs.get('href'), []
            if tag == 'link' and attrs.get('rel') == 'canonical':
                self.canonicals.append(attrs.get('href'))
            if tag == 'h1':
                self.headings += 1

        def handle_data(self, text):
            if self.current is not None:
                self.label.append(text)

        def handle_endtag(self, tag):
            if tag == 'a' and self.current is not None:
                self.links.append((self.current, ' '.join(''.join(self.label).split())))
                self.current = None

    if any(not body or len(body) > MAX_BYTES for body in (home, target)):
        raise ValueError('Empty or oversized Home/VIP response')
    h, t = Document(home), Document(target)
    if h.canonicals != [ORIGIN + '/'] or t.canonicals != [ORIGIN + '/vip-services-ibiza/']:
        raise ValueError('Unexpected Home/VIP canonical')
    if h.headings != 1 or t.headings != 1:
        raise ValueError('Unexpected Home/VIP H1 count')
    matches = h.links.count(('/vip-services-ibiza/', 'VIP hospitality requests'))
    if matches > 1 or (require_link and matches != 1):
        raise ValueError('Published Home VIP link missing or duplicated')
    hrefs = [href for href, _ in t.links]
    if (hrefs.count('/contact/?service=vip-services') != 2
            or 'tel:+34600703303' not in hrefs
            or 'mailto:partnership@ibizavipmove.com' not in hrefs
            or not any(urlsplit(href).scheme == 'https' and urlsplit(href).netloc == 'wa.me'
                       and urlsplit(href).path == '/34600703303' for href in hrefs)):
        raise ValueError('VIP contact routes changed')
    return {'newLinkPresent': matches == 1, 'contactRoutesPreserved': True,
            'scope': 'Static HTML only; no contact activated or scripts executed.'}


def home_vip_self_test():
    home = (f'<link rel="canonical" href="{ORIGIN}/"><h1>Home</h1>'
            '<a href="/vip-services-ibiza/">VIP hospitality requests</a>').encode()
    target = (f'<link rel="canonical" href="{ORIGIN}/vip-services-ibiza/"><h1>VIP</h1>'
              '<a href="/contact/?service=vip-services">Brief</a>'
              + '<a href="/contact/?service=vip-services">Brief</a>'
              + '<a href="tel:+34600703303">Call</a>'
              + '<a href="mailto:partnership@ibizavipmove.com">Email</a>'
              + '<a href="https://wa.me/34600703303">WhatsApp</a>').encode()
    assert validate_home_vip(home, target, True)['newLinkPresent']
    old = home.split(b'<a ', 1)[0]
    assert not validate_home_vip(old, target, False)['newLinkPresent']
    for h, t in [(old, target), (home + home[home.index(b'<a '):], target),
                 (home.replace(b'/vip-services-ibiza/', b'/wrong/'), target),
                 (home, target.replace(b'tel:+34600703303', b'tel:+34000000000'))]:
        try:
            validate_home_vip(h, t, True)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid Home/VIP release accepted')
    print('PASS: Home/VIP published verification; six offline cases, no network')


def verify_home_vip():
    output = Path(os.environ.get('RUNNER_TEMP', '/tmp')) / 'ivm-dmc-context-review' / 'home-vip'
    if output.resolve().is_relative_to(Path('_site').resolve()):
        raise ValueError('Home/VIP evidence cannot enter website output')
    output.mkdir(parents=True, exist_ok=True)
    require_link = os.environ.get('GITHUB_EVENT_NAME') != 'pull_request'
    report = {'checkedAt': datetime.now(ZoneInfo('Europe/Madrid')).isoformat(),
              'verificationSourceCommit': os.environ.get('GITHUB_SHA'),
              'stage': 'published' if require_link else 'pre-release-baseline',
              'status': 'NOT_RUN', 'files': []}
    paths = {'/': 'served-home.html', '/vip-services-ibiza/': 'served-vip-services.html',
             '/assets/images/yacht-priority.avif': 'yacht-priority.avif',
             '/assets/images/yacht-priority.webp': 'yacht-priority.webp'}
    bodies = {}
    try:
        for path, name in paths.items():
            url = ORIGIN + path
            request = Request(url, headers={'Accept-Encoding': 'identity',
                'User-Agent': 'IbizaVIPMove-ReadOnlyVerification/1.0'})
            with build_opener(NoRedirect()).open(request, timeout=20) as response:
                if response.status != 200 or response.url != url:
                    raise ValueError('Expected HTTP 200 at exact allowlisted Home/VIP resource')
                body = response.read(MAX_BYTES + 1)
            if not body or len(body) > MAX_BYTES:
                raise ValueError('Empty or oversized Home/VIP resource')
            bodies[path] = body
            (output / name).write_bytes(body)
            report['files'].append({'path': path, 'httpStatus': 200, 'bytes': len(body),
                                    'sha256': hashlib.sha256(body).hexdigest()})
        report.update(validate_home_vip(bodies['/'], bodies['/vip-services-ibiza/'], require_link))
        report['status'] = 'PASS' if require_link else 'BASELINE_CAPTURED'
    except Exception as err:
        report.update(status='FAILED_OR_BLOCKED', error=f'{type(err).__name__}: {err}')
        raise
    finally:
        (output / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print('HOME_VIP_PUBLIC_REPORT ' + json.dumps(report), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    self_test()
    home_vip_self_test()
    if not args.self_test:
        verify()
        verify_home_vip()
