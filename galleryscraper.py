import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to download images or videos from the URL
def download_file(url, folder):
    local_filename = os.path.join(folder, url.split('/')[-1])
    print(f"Downloading: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return local_filename

# Function to scrape an individual post page for media and text
def scrape_post(post_url, download_folder, driver):
    print(f"Scraping post: {post_url}")
    driver.get(post_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find and download images
    images = soup.find_all('img')
    for img in images:
        if img.get('src'):
            image_url = urljoin(post_url, img['src'])
            download_file(image_url, download_folder)

    # Find and download videos
    videos = soup.find_all('video')
    for video in videos:
        if video.get('src'):
            video_url = urljoin(post_url, video['src'])
            download_file(video_url, download_folder)

    # Extract text content
    text_content = soup.get_text()
    with open(os.path.join(download_folder, 'text_content.txt'), 'a') as f:
        f.write(f"Content from {post_url}:\n{text_content}\n\n")

# Main function to scrape the gallery and navigate pagination
def scrape_gallery(start_url, download_folder='downloaded_site'):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(start_url)

    while True:
        print(f"Scraping gallery page: {driver.current_url}")
        # Wait for a specific element that indicates the page has loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
        
        # Use Selenium to find post links
        post_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/post/"]')
        print(f"Found {len(post_links)} post links")
        for link in post_links:
            post_url = link.get_attribute('href')
            scrape_post(post_url, download_folder, driver)

        # Handle pagination by finding the next page link
        try:
            next_button = driver.find_element(By.LINK_TEXT, 'Next')
            next_button.click()
        except:
            print("No more pages to scrape.")
            break

    driver.quit()

scrape_gallery('https://gallery.accords-library.com/posts')
