import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 1. Setup download folder
download_folder = "raw_pdfs"
os.makedirs(download_folder, exist_ok=True)

# 2. Main DGHS URL
main_url = "https://dghs.gov.bd/views/latest-news?page=1&page_size=100"
print(f"Connecting to main page: {main_url}")

# Bypass SSL warnings
requests.packages.urllib3.disable_warnings()
response = requests.get(main_url, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')

# 3. Find intermediate links STRICTLY for Measles
detail_links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if not href:
        continue
        
    text = link.get_text().lower()
    
    # THE FIX: We ONLY care if the link text explicitly mentions measles
    if 'measles' in text or 'হাম' in text:
        full_url = urljoin(main_url, href)
        if full_url not in detail_links:
            detail_links.append(full_url)

print(f"Found {len(detail_links)} strictly Measles-related pages. Digging into them now...\n")

# 4. Visit each intermediate page and grab the actual PDF
download_count = 0
for detail_url in detail_links:
    try:
        detail_response = requests.get(detail_url, verify=False)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        
        # Look for the PDF link on this second page
        for link in detail_soup.find_all('a'):
            href = link.get('href')
            
            # Make sure it's actually a PDF file
            if href and href.lower().endswith('.pdf'):
                pdf_url = urljoin(detail_url, href)
                file_name = pdf_url.split("/")[-1]
                file_path = os.path.join(download_folder, file_name)
                
                # Check if we already downloaded it
                if not os.path.exists(file_path):
                    print(f"Downloading Measles Data: {file_name}")
                    pdf_response = requests.get(pdf_url, verify=False)
                    with open(file_path, 'wb') as f:
                        f.write(pdf_response.content)
                    download_count += 1
                    time.sleep(1) # Be polite to the server
                    
    except Exception as e:
        print(f"Error accessing {detail_url}: {e}")

print(f"\nMission Accomplished! Downloaded {download_count} targeted PDFs into your folder.")