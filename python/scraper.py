import json
import hashlib
import os
from datetime import datetime

import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


WEBSITE_URL = "https://consumeraffairs.gov.in/pages/legal-metrology-act"

DOWNLOAD_DIR = "downloads"
DATABASE_FILE = "documents.json"


INITIAL_DOCUMENTS = [
    "9 The Legal Metrology (Package Commodities) Rules, 2011.pdf",
    "National_Std_Rules2019_1732709005.pdf",
    "6_0_1732709495.pdf"
]


def load_database():
    if not os.path.exists(DATABASE_FILE):
        return {
            "documents": []
        }

    with open(DATABASE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_database(database):
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=4, ensure_ascii=False)


def get_pdf_links():
    response = requests.get(
        WEBSITE_URL,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        verify=False
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    pdfs = []

    for link in soup.find_all("a", href=True):

        href = link["href"]

        if ".pdf" not in href.lower():
            continue

        url = urljoin(WEBSITE_URL, href)
        url = url.replace("http://", "https://")

        filename = unquote(url.split("/")[-1])

        pdfs.append({
            "filename": filename,
            "url": url
        })
    return pdfs


def is_initial_document(filename):
    filename_lower = filename.lower()
    if filename_lower == INITIAL_DOCUMENTS[1].lower():
        return True

    if filename_lower == INITIAL_DOCUMENTS[2].lower():
        return True
    if filename_lower.startswith(
        "9 the legal metrology (package commodities) rules, 2011"
    ):
        return True
    if filename_lower.startswith("9_"):
        return True

    return False


def calculate_hash(filepath):

    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def download_pdf(pdf):

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    filename = pdf["filename"]
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    print(f"\nDownloading:")
    print(filename)

    response = requests.get(
        pdf["url"],
        timeout=60,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        verify=False
    )

    response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(response.content)

    file_hash = calculate_hash(filepath)

    print(f"Saved: {filepath}")

    return filepath, file_hash

def process_documents():

    database = load_database()

    discovered_pdfs = get_pdf_links()

    print(f"Found {len(discovered_pdfs)} PDFs on website.")

    selected = []

    for pdf in discovered_pdfs:

        if is_initial_document(pdf["filename"]):
            selected.append(pdf)

    print(f"Initial target documents found: {len(selected)}")
    for pdf in selected:

        filename = pdf["filename"]
        url = pdf["url"]

        already_exists = any(
            doc["url"] == url
            for doc in database["documents"]
        )

        if already_exists:

            print(f"\nAlready tracked:")
            print(filename)

            continue

        try:

            filepath, file_hash = download_pdf(pdf)

            document = {
                "filename": filename,
                "url": url,
                "sha256": file_hash,
                "downloaded_at": datetime.now().isoformat(),
                "processed": False
            }

            database["documents"].append(document)

            save_database(database)

            print("Added to database.")

        except Exception as e:

            print(f"FAILED: {filename}")
            print(e)


if __name__ == "__main__":
    process_documents()