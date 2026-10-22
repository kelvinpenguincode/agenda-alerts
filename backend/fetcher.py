import requests
from bs4 import BeautifulSoup
import os
import time

# Jersey Village setup
jv_url = "https://www.jerseyvillage.gov/AgendaCenter"
jv_base_url = "https://www.jerseyvillage.gov"
jv_response = requests.get(jv_url)
jv_soup = BeautifulSoup(jv_response.text, "html.parser")
jv_links = jv_soup.find_all("a")
agenda_links = []

def fetch_jersey_village():
    # loops through all links and checks for agenda link pattern
    for link in jv_links:
        href = link.get("href")
        if href and "/AgendaCenter/ViewFile/Agenda/" in href:
            if "html=true" not in href and "packet=true" not in href:
                full_url = jv_base_url + href
                if full_url not in agenda_links:
                    agenda_links.append(full_url)

    save_folder = "../docs/test-data"
    os.makedirs(save_folder, exist_ok=True)

    for agenda_url in agenda_links:
        filename = agenda_url.split("/")[-1] + ".pdf"
        filepath = os.path.join(save_folder, filename)

        if os.path.exists(filepath):
            print(f"Already have {filename}, skipping")
            continue

        print(f"Downloading {filename}...")
        pdf = requests.get(agenda_url)

        with open(filepath, "wb") as f:
            f.write(pdf.content)

        print(f"Saved {filename}")
        time.sleep(1)


def fetch_cfisd():
    base_url = "https://manuals.boardbook.org"
    url = "https://manuals.boardbook.org/Public/Organization/668"
    save_folder = "../docs/test-data-cfisd"

    os.makedirs(save_folder, exist_ok=True)

    response = requests.get(url, headers={"User-Agent": "LocalLens/1.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    cfisd_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "/Public/Agenda/" in href:
            full_url = base_url + href if href.startswith("/") else href
            if full_url not in cfisd_links:
                cfisd_links.append(full_url)

    print(f"Found {len(cfisd_links)} CFISD agendas")

    for agenda_url in cfisd_links[:5]:
        filename = agenda_url.split("/")[-1] + ".pdf"
        filepath = os.path.join(save_folder, filename)

        if os.path.exists(filepath):
            print(f"Already have {filename}, skipping")
            continue

        print(f"Downloading {filename}...")
        pdf = requests.get(agenda_url, headers={"User-Agent": "LocalLens/1.0"})

        with open(filepath, "wb") as f:
            f.write(pdf.content)

        print(f"Saved {filename}")
        time.sleep(1)


if __name__ == "__main__":
    fetch_jersey_village()
    fetch_cfisd()