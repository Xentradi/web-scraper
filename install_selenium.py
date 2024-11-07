import subprocess
import sys

def install_packages():
    # Install Selenium
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])

    # Install WebDriver Manager to handle browser drivers
    subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager"])

if __name__ == "__main__":
    install_packages()
