# Web Scraper

This project is a simple web scraper that downloads a website and all its static assets, such as images, CSS, and JavaScript files, and stores them locally. It uses Python along with the `requests` and `beautifulsoup4` libraries.

## How It Works

The web scraper operates by starting at a given URL and sequentially visiting each page it encounters. It uses a queue to manage the URLs to be visited and a set to keep track of visited URLs to avoid processing the same page multiple times. The scraper downloads images, videos, and audio files from each page and saves the HTML content locally. It only follows internal links to ensure it stays within the target website.

## Features

- Downloads HTML content of a webpage.
- Downloads all images, CSS, and JavaScript files linked in the webpage.
- Saves all downloaded content in a specified local directory.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository to your local machine.
2. Install the required Python libraries using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Open the `webscraper.py` file.
2. Replace the `website_url` variable with the URL of the website you want to scrape.
3. Run the script:

   ```bash
   python webscraper.py
   ```

4. The downloaded content will be saved in the `downloaded_site` directory by default.

## Notes

- Ensure you have permission to scrape the website you are targeting.
- This script is intended for educational purposes and should be used responsibly.

## License

This project is licensed under the MIT License.
