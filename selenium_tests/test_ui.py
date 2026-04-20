"""
Selenium UI tests for the Streamlit app.
Requires: Chrome + chromedriver, app running at http://localhost:8501
Run: pytest selenium_tests/
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:8501"
TIMEOUT = 15


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(TIMEOUT)
    yield drv
    drv.quit()


class TestHomePage:
    def test_page_title(self, driver):
        driver.get(BASE_URL)
        WebDriverWait(driver, TIMEOUT).until(EC.title_contains("Smart Resume Analyzer"))
        assert "Smart Resume Analyzer" in driver.title

    def test_upload_widget_present(self, driver):
        driver.get(BASE_URL)
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        upload = driver.find_element(By.XPATH, '//input[@type="file"]')
        assert upload is not None

    def test_heading_visible(self, driver):
        driver.get(BASE_URL)
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        heading = driver.find_element(By.TAG_NAME, "h1")
        assert "Resume Analyzer" in heading.text
