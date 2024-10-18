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

def scrape_website(url, download_folder='downloaded_site'):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Download all images
    for img in soup.find_all('img'):
        img_url = urljoin(url, img.get('src'))
        download_file(img_url, download_folder)

    # Download all CSS
    for css in soup.find_all('link', rel='stylesheet'):
        css_url = urljoin(url, css.get('href'))
        download_file(css_url, download_folder)

    # Download all JS
    for script in soup.find_all('script'):
        if script.get('src'):
            js_url = urljoin(url, script.get('src'))
            download_file(js_url, download_folder)

    # Save the HTML file
    html_file_path = os.path.join(download_folder, 'index.html')
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

if __name__ == "__main__":
    website_url = "https://accords-library.com"  # Replace with the target website URL
    scrape_website(website_url)
