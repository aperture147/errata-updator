import requests
from bs4 import BeautifulSoup

def parse(errata_id: str):
    resp = requests.get(f'https://access.redhat.com/errata/{errata_id}')
    soup = BeautifulSoup(resp.content, 'lxml')
    # Solution
    solution_section = soup.find("div", id="solution")
    solution = ', '.join([
        p.get_text(strip=True) for p in solution_section.find_all("p")
    ]) if solution_section else "N/A"

    # Fixes
    fixes_section = soup.find("div", id="fixes")
    fixes = ', '.join([
        p.get_text(strip=True) for p in fixes_section.find_all("li")
    ]) if fixes_section else "N/A"

    # CVEs
    cve_section = soup.find("div", id="cves")
    cves = ', '.join([a.get_text(strip=True) for a in cve_section.find_all("a")]) if cve_section else "N/A"

    with open("test.txt", "w") as f:
        f.write(f"Solution:\n{solution}\n\n")
        f.write(f"CVEs:\n{cves}\n\n")
        f.write(f"Fixes:\n{fixes}\n")
    
    return (solution, cves, fixes)