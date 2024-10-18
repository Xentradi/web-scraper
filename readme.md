# Web Scraper

This project is a simple web scraper that downloads a website and all its static assets, such as images, CSS, and JavaScript files, and stores them locally. It uses Python along with the `requests` and `beautifulsoup4` libraries.

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
2. Install the required Python libraries using pip:

   ```bash
   pip install requests beautifulsoup4
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
