from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.headless = True


def get_screenshot(url=None, folder="uploads/", filename="screenshot.png"):
    """
    Gets a screenshot using selenium
    """
    path = f"{folder}/{filename}"
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    driver.save_screenshot(path)
    driver.quit()
