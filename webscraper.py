import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_file(url, folder):
    local_filename = os.path.join(folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def scrape_website(url, download_folder='downloaded_site', visited=None):
    if visited is None:
        visited = set()
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Download all images
    for img in soup.find_all('img'):
        img_url = urljoin(url, img.get('src'))
        download_file(img_url, download_folder)

    # Download all CSS
    for css in soup.find_all('link', rel='stylesheet'):
        css_url = urljoin(url, css.get('href'))
        download_file(css_url, download_folder)

    # Extract and save text content
    text_content = soup.get_text(separator='\n', strip=True)
    text_file_path = os.path.join(download_folder, 'content.txt')
    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(text_content)

    # Traverse and scrape all links
    for link in soup.find_all('a', href=True):
        link_url = urljoin(url, link.get('href'))
        if urlparse(link_url).netloc == urlparse(url).netloc:  # Only follow internal links
            scrape_website(link_url, download_folder, visited)
    website_url = "https://accords-library.com"  # Replace with the target website URL
    scrape_website(website_url)
