import json
import os
import pathlib

import requests

NOTION = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
    "Notion-Version": "2022-06-28",
}
OUT = pathlib.Path("reports")


def active_clients():
    r = requests.post(
        f"{NOTION}/databases/{os.environ['NOTION_CLIENTS_DB']}/query",
        headers=HEADERS,
        json={"filter": {"property": "Status", "select": {"equals": "Active"}}},
        timeout=30,
    )
    r.raise_for_status()
    clients = []
    for page in r.json()["results"]:
        props = page["properties"]
        clients.append({
            "name": props["Name"]["title"][0]["plain_text"],
            "report_url": props["Latest report"]["url"],
        })
    return clients


def main():
    OUT.mkdir(exist_ok=True)
    clients = active_clients()
    for c in clients:
        if not c["report_url"]:
            continue
        try:
            pdf = requests.get(c["report_url"], timeout=60)
            (OUT / f"{c['name']}.pdf").write_bytes(pdf.content)
        except requests.RequestException:
            pass
    pathlib.Path("clients.json").write_text(json.dumps(clients))
    print(f"fetched {len(clients)} clients")


if __name__ == "__main__":
    main()
