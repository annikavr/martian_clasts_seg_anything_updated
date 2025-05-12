import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://pds-imaging.jpl.nasa.gov/data/mars2020/mars2020_mastcamz_ops_calibrated"
TARGET_DIR = os.path.expanduser("~/Desktop/mars_zcam07114_xmls")
SOLS = range(1000, 1010)  # Change this range as needed

def download_xmls():
    os.makedirs(TARGET_DIR, exist_ok=True)
    for sol in SOLS:
        url = f"{BASE_URL}/sol{sol:05d}/fdr/"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to access {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")

        for link in links:
            href = link.get("href")
            if href and href.endswith(".xml") and "zcam07114" in href.lower():
                xml_url = url + href
                xml_path = os.path.join(TARGET_DIR, href)
                try:
                    with requests.get(xml_url, stream=True) as r:
                        r.raise_for_status()
                        with open(xml_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                    print(f"Downloaded: {href}")
                except Exception as e:
                    print(f"Failed to download {href}: {e}")

if __name__ == "__main__":
    download_xmls()
