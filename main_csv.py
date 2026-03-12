import requests
from datetime import datetime, timedelta, time
import csv

CRITICAL_SEVERITY = 'Critical'
IMPORTANT_SEVERITY = 'Important'
MODERATE_SEVERITY = 'Moderate'

SEVERITY_LIST = [CRITICAL_SEVERITY, IMPORTANT_SEVERITY]
SEVERITY_SET = set(SEVERITY_LIST)

# excluded_keywords = ['firefox', 'thunderbird', 'gimp', 'wireshark', 'keylime']
excluded_keywords = []

end_datetime = datetime.now()
# start_datetime = datetime.combine(end_datetime - timedelta(days=58), time.min)
start_datetime = datetime.combine(end_datetime - timedelta(days=58), time.min)
# product_name = "Red\ Hat\ Enterprise\ Linux|*|9|x86_64"
product_name = "Red\ Hat\ OpenShift\ Container\ Platform|*|4.16|x86_64"
url = "https://access.redhat.com/hydra/rest/search/kcs"
fq = [
    f'year:[{start_datetime.year} TO {end_datetime.year}]',
    f'portal_publication_date:[{start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")} TO {end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")}]',
    'documentKind:("Errata")',
    f'portal_product_filter:{product_name}',
    'portal_advisory_type:("Bug Fix Advisory")'
    # f'portal_severity:({" OR ".join(SEVERITY_LIST)})',
]
fl = [
    "id",
    "portal_severity",
    "portal_synopsis",
    "portal_publication_date",
    "portal_update_date",
    "abstract",
    "view_uri",
]

params = {
    "q": "*:*",
    "start": "0",
    "fl": ",".join(fl),
    "fq": " AND ".join(fq),
    "rows": "5000",
    "sort": "portal_update_date desc",
}

print('Fetching erratas from Red Hat, condition:')
print(f'    - Publication date range: {start_datetime} to {end_datetime}')
print(f'    - Severities: {", ".join(SEVERITY_LIST)}')
resp = requests.get(url, params=params)

data = resp.json()
print(f"Total erratas fetched: {len(data['response']['docs'])}")
print(f"Filtering erratas by keywords {', '.join(excluded_keywords)}...")
erratas = sorted(data['response']['docs'], key=lambda e: e['portal_update_date'], reverse=True)
erratas = [
    e for e in erratas
    if all(kw.lower() not in e['portal_synopsis'].lower() for kw in excluded_keywords)
]

print(f"Total erratas after filtering: {len(erratas)}")

with open("erratas.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Severity", "Synopsis", "Description", "Publication Date", "Update Date", "URL"])
    for e in erratas:
        writer.writerow([
            f"=HYPERLINK(\"{e['view_uri']}\", \"{e['id']}\")",
            e['portal_severity'],
            e['portal_synopsis'],
            e['abstract'],
            e['portal_publication_date'].split('T')[0],
            e['portal_update_date'][0].split('T')[0],
            e['view_uri']
        ])

print(f"Written errata data to erratas.csv")
