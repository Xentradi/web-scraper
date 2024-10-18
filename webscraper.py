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

    normalized_url = urlparse(url)._replace(fragment='').geturl()
    if normalized_url in visited:
        return
    visited.add(normalized_url)

    try:
        response = requests.get(normalized_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve {normalized_url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Download all images
    for img in soup.find_all('img'):
        img_url = urljoin(url, img.get('src'))
        download_file(img_url, download_folder)

    # Download all video files
    for video in soup.find_all('video'):
        for source in video.find_all('source'):
            video_url = urljoin(url, source.get('src'))
            download_file(video_url, download_folder)
    for img in soup.find_all('img'):
        img_url = urljoin(url, img.get('src'))
        download_file(img_url, download_folder)

    # Download all CSS
    for css in soup.find_all('link', rel='stylesheet'):
        css_url = urljoin(url, css.get('href'))
        download_file(css_url, download_folder)

    # Download other media files (audio, etc.)
    for audio in soup.find_all('audio'):
        for source in audio.find_all('source'):
            audio_url = urljoin(url, source.get('src'))
            download_file(audio_url, download_folder)
    for css in soup.find_all('link', rel='stylesheet'):
        css_url = urljoin(url, css.get('href'))
        download_file(css_url, download_folder)

    # Save the HTML content of the page
    page_name = urlparse(url).path.strip('/').replace('/', '_') or 'index'
    html_file_path = os.path.join(download_folder, f"{page_name}.html")
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    # Traverse and scrape all links
    for link in soup.find_all('a', href=True):
        link_url = urljoin(url, link.get('href'))
        if urlparse(link_url).netloc == urlparse(url).netloc:  # Only follow internal links
            scrape_website(link_url, download_folder, visited)
if __name__ == "__main__":
    website_url = "https://accords-library.com"  # Replace with the target website URL
    scrape_website(website_url)
