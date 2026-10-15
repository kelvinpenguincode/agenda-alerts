import requests
from bs4 import BeautifulSoup
import os
import time

url = "https://www.jerseyvillage.gov/AgendaCenter"

response = requests.get(url)
print(response.status_code)



soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a")


base_url = "https://www.jerseyvillage.gov"
agenda_links = []

def fetch_jersey_village():

    #loops through all the links and checks if they have that agenda link pattern
    #if they do it makes URL complete and adds it to the agenda_links list
    for link in links:
        href = link.get("href")
        if href and "/AgendaCenter/ViewFile/Agenda/" in href:
            if "html=true" not in href and "packet=true" not in href:
                full_url = base_url + href
                if full_url not in agenda_links:
                    agenda_links.append(full_url)

    for agenda in agenda_links:
        print(agenda)






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




if __name__ == "__main__":
    fetch_jersey_village()