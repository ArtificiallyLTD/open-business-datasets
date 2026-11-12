import concurrent.futures as cf
import csv
import datetime as dt
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

TOKEN = os.environ.get('APIFY_TOKEN', '')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = dt.date.today()
TRENDS_COUNTRIES = [['US', 'GB', 'DE', 'FR', 'IN'], ['BR', 'AU', 'JP', 'MX', 'ES'], ['IT', 'NL', 'RO', 'PL', 'TR'], ['ID', 'KR', 'ZA', 'NG', 'CA']]


def api(method, path, body=None):
    for _ in range(30):
        try:
            req = urllib.request.Request(
                'https://api.apify.com/v2' + path,
                method=method,
                data=json.dumps(body).encode() if body is not None else None,
                headers={'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'},
            )
            return json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as error:
            if error.code in (402, 429, 500, 502, 503, 504):
                time.sleep(20)
                continue
            raise
        except (urllib.error.URLError, http.client.IncompleteRead, ConnectionError, TimeoutError):
            time.sleep(10)
            continue
    raise RuntimeError(f'Apify API kept failing for {path}')


def run_actor(actor, run_input):
    run = api('POST', f'/acts/artificially~{actor}/runs?timeout=3000', run_input)['data']
    while True:
        run = api('GET', f"/actor-runs/{run['id']}?waitForFinish=60")['data']
        if run['status'] not in ('READY', 'RUNNING'):
            break
    items, offset = [], 0
    while True:
        page = api('GET', f"/datasets/{run['defaultDatasetId']}/items?clean=1&offset={offset}&limit=1000")
        items += page
        offset += len(page)
        if len(page) < 1000:
            break
    print(f"{actor} {json.dumps(run_input)[:80]}: {run['status']}, {len(items)} items", flush=True)
    return items


def run_many(actor, inputs, key):
    merged = {}
    with cf.ThreadPoolExecutor(2) as pool:
        for items in pool.map(lambda i: run_actor(actor, i), inputs):
            for item in items:
                merged[key(item)] = item
    return list(merged.values())


def cell(value):
    if isinstance(value, list):
        return '; '.join(str(v) for v in value if v not in (None, ''))
    return '' if value is None else value


def write(name, rows):
    if not rows:
        print(f'{name}: no rows returned, keeping the previous files', flush=True)
        return
    folder = os.path.join(ROOT, name)
    os.makedirs(folder, exist_ok=True)
    columns = list(rows[0].keys())
    with open(os.path.join(folder, name + '.csv'), 'w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: cell(row.get(k)) for k in columns})
    with open(os.path.join(folder, name + '.json'), 'w') as handle:
        json.dump(rows, handle, ensure_ascii=False, indent=0)
    card = os.path.join(folder, 'README.md')
    if os.path.exists(card):
        with open(card) as handle:
            text = handle.read()
        with open(card, 'w') as handle:
            handle.write(re.sub(r'- \*\*Rows:\*\* [\d,]+', f'- **Rows:** {len(rows):,}', text))
    print(f'{name}: {len(rows)} rows written', flush=True)


def yc_companies():
    raw = run_many('ycombinator-scraper', [{'batches': [str(y)], 'maxResults': 5000, 'includeSocials': True} for y in range(2005, TODAY.year + 2)], lambda c: c['ycId'])
    rows = [{
        'ycId': c.get('ycId'), 'name': c.get('name'), 'website': c.get('website'), 'oneLiner': c.get('oneLiner'),
        'batch': c.get('batch'), 'status': c.get('status'), 'stage': c.get('stage'), 'industry': c.get('industry'),
        'subindustry': c.get('subindustry'), 'tags': c.get('tags'), 'location': c.get('location'), 'country': c.get('country'),
        'teamSize': c.get('teamSize'), 'yearFounded': c.get('yearFounded'), 'isHiring': c.get('isHiring'),
        'topCompany': c.get('topCompany'), 'linkedin': (c.get('socials') or {}).get('linkedin'), 'ycUrl': c.get('ycUrl'),
    } for c in sorted(raw, key=lambda c: c.get('ycId') or 0)]
    write('yc-companies', rows)


def eu_open_tenders():
    windows = [(TODAY - dt.timedelta(days=a), TODAY - dt.timedelta(days=a)) for a in range(29, -1, -1)]
    inputs = [{'noticeType': 'cn-standard', 'onlyOpenDeadlines': True, 'dateFrom': f.isoformat(), 'dateTo': t.isoformat(), 'maxTenders': 1000, 'includeBuyerProfile': False, 'includeFullDetails': True} for f, t in windows]
    raw = run_many('eu-tenders-scraper', inputs, lambda t: t['noticeId'])

    def buyer(b):
        return b if isinstance(b, str) else (b or {}).get('officialName')

    def code(c):
        return c.get('code') if isinstance(c, dict) else c

    rows = [{
        'noticeId': t.get('noticeId'), 'publicationDate': t.get('publicationDate'), 'submissionDeadline': t.get('submissionDeadline'),
        'title': t.get('titleEnglish') or t.get('title'), 'titleOriginal': t.get('title'), 'buyer': buyer(t.get('buyer')),
        'country': t.get('country'), 'countryCode': t.get('countryCode'), 'city': t.get('city'), 'contractType': t.get('contractType'),
        'procedureType': t.get('procedureType'), 'mainCpvCode': code(t.get('mainCpvCode')),
        'cpvCodes': [code(c) for c in (t.get('cpvCodes') or [])], 'estimatedValue': t.get('estimatedValue'),
        'currency': t.get('currency'), 'numberOfLots': t.get('numberOfLots'), 'url': t.get('url'),
    } for t in sorted(raw, key=lambda t: t.get('publicationDate') or '', reverse=True)]
    write('eu-open-tenders', rows)


def us_federal_open_opportunities():
    windows = [(TODAY - dt.timedelta(days=a), TODAY - dt.timedelta(days=max(a - 4, 0))) for a in range(29, -1, -5)]
    inputs = [{'noticeTypes': ['o', 'k', 'p', 'r'], 'postedFrom': f.isoformat(), 'postedTo': t.isoformat(), 'openForResponsesOnly': True, 'maxResults': 2000, 'includeDescription': False, 'includeAttachments': False} for f, t in windows]
    raw = run_many('samgov-opportunities-scraper', inputs, lambda o: o['noticeId'])
    rows = [{
        'noticeId': o.get('noticeId'), 'title': o.get('title'), 'solicitationNumber': o.get('solicitationNumber'),
        'noticeType': o.get('noticeType'), 'postedDate': (o.get('postedDate') or '')[:10], 'responseDeadline': o.get('responseDeadline'),
        'department': o.get('department'), 'subTier': o.get('subTier'), 'office': o.get('office'), 'naicsCode': o.get('naicsCode'),
        'pscCode': o.get('pscCode'), 'setAside': o.get('setAside'),
        'placeOfPerformanceCity': (o.get('placeOfPerformance') or {}).get('city'),
        'placeOfPerformanceState': (o.get('placeOfPerformance') or {}).get('state'), 'samUrl': o.get('samUrl'),
    } for o in sorted(raw, key=lambda o: o.get('postedDate') or '', reverse=True)]
    write('us-federal-open-opportunities', rows)


def google_trends_trending_now():
    inputs = [{'mode': 'trendingNow', 'trendingNowCountries': g, 'trendingNowHours': '24', 'trendingNowIncludeNews': False, 'proxyConfiguration': {'useApifyProxy': True}} for g in TRENDS_COUNTRIES]
    raw = run_many('google-trends-scraper', inputs, lambda t: (t.get('geo'), t.get('searchTerm')))
    rows = [{
        'date': (t.get('scrapedAt') or '')[:10], 'geo': t.get('geo'), 'rank': t.get('rank'), 'searchTerm': t.get('searchTerm'),
        'searchVolume': t.get('searchVolume'), 'increasePercentage': t.get('increasePercentage'), 'categories': t.get('categories'),
        'startedAt': t.get('startedAt'), 'isActive': t.get('isActive'), 'relatedQueries': (t.get('relatedQueries') or [])[:10],
        'articleCount': t.get('articleCount'), 'trendsUrl': t.get('trendsUrl'),
    } for t in sorted(raw, key=lambda t: (t.get('geo') or '', t.get('rank') or 0))]
    write('google-trends-trending-now', rows)


JOBS = {
    'yc-companies': yc_companies,
    'eu-open-tenders': eu_open_tenders,
    'us-federal-open-opportunities': us_federal_open_opportunities,
}

if __name__ == '__main__':
    if not TOKEN:
        sys.exit('Set APIFY_TOKEN to an Apify API token.')
    for name in sys.argv[1:] or JOBS:
        JOBS[name]()
