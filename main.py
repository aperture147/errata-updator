import requests
from datetime import datetime, timedelta, time

CRITICAL_SEVERITY = 'Critical'
IMPORTANT_SEVERITY = 'Important'
MODERATE_SEVERITY = 'Moderate'

SEVERITY_LIST = [CRITICAL_SEVERITY, IMPORTANT_SEVERITY]
SEVERITY_SET = set(SEVERITY_LIST)

excluded_keywords = ['firefox', 'thunderbird', 'gimp', 'wireshark', 'keylime']

end_datetime = datetime.now()
start_datetime = datetime.combine(end_datetime - timedelta(days=7), time.min)

url = "https://access.redhat.com/hydra/rest/search/kcs"
fq = [
    f'year:[{start_datetime.year} TO {end_datetime.year}]',
    f'portal_publication_date:[{start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")} TO {end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")}]',
    'documentKind:("Errata")',
    'portal_product_filter:Red\ Hat\ Enterprise\ Linux|*|*|x86_64',
    f'portal_severity:({" OR ".join(SEVERITY_LIST)})',
]
fl = [
    "id",
    "portal_severity",
    "portal_synopsis",
    "portal_update_date",
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

with open("erratas.html", "w") as f:
    f.writelines([
        "Em chào anh chị,<br><br>\n",
        "Em xin gửi anh chị danh sách các errata Critical và Important cho RHEL, dành cho tất cả các phiên bản đang được support.<br><br>\n",
        f"Do danh sách errata rất dài, nên em chỉ gửi các errata Critical và Important để mọi người dễ theo dõi. Để xem thêm các errata Moderate, Low và None, mọi người vui lòng xem trên trang <a href=\"https://access.redhat.com/errata-search/\">https://access.redhat.com/errata-search/</a>.<br><br>\n",
        "Sau email này, mong anh chị vui lòng gửi lại cho em danh sách các package không dùng đến để em loại ra khỏi danh sách errata.<br><br>\n",
        "Thống kê tổng quát:<br>\n",
        "<ul>\n",
            f'<li>Tổng errata: {len(erratas)}</li>\n',
            f'<li>Các package đã bỏ qua: {", ".join(excluded_keywords)}</li>\n',
            f'<li>Thời gian quét: {start_datetime.date()} - {end_datetime.date()}</li>\n',
        "</ul>\n"
    ])
    for sev in SEVERITY_LIST:
        matched_erratas = [e for e in erratas if e['portal_severity'] == sev]
        f.write(f"Các Errata {sev}:<br>\n")
        f.write('<ul>\n')
        f.writelines([
            f"\t<li><a href=\"{e['view_uri']}\">{e['id']}: {e['portal_synopsis'].replace(f'{sev}:', '').strip()}</a></li>\n"
            for e in matched_erratas
        ])
        f.write("</ul>\n")
        
    f.writelines([
        "Mong anh chị chú ý cập nhật các errata này sớm nhất để đảm bảo an toàn cho hệ thống.<br><br>\n",
        "Chúc mọi người một ngày làm việc hiệu quả.<br>\n"
    ])

print(f"Written email content to erratas.html")