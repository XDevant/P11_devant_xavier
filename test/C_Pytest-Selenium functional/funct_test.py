from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import pytest
from time import sleep


@pytest.fixture(scope="module", params=["chrome", "firefox"])
def selenium(request):
    driver = request.param
    if driver == "chrome":
        service = ChromeService('C:/ProgramData/Miniconda3/Webdrivers/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=800,600")
        options.add_argument("--disable-dev-shm-usage")
        options.set_capability("detach", True)
    elif driver == "firefox":
        service = FirefoxService('C:/ProgramData/Miniconda3/Webdrivers/geckodriver')
        options = webdriver.FirefoxOptions()
        options.binary_location = r"C:\Users\xdeva\AppData\Local\Mozilla Firefox\firefox.exe"
    else:
        return None
    service.start()
    selenium = webdriver.Remote(service.service_url, options=options)
    yield selenium
    selenium.quit()
    service.stop()


class TestUserStories:
    def test_live_server(self, selenium):
        selenium.get('http://127.0.0.1:8000/')
        assert selenium.title == "GUDLFT Registration"

    def test_user_story_1(self, app, selenium):
        selenium.get('http://localhost:8000')
        assert selenium.title == "GUDLFT Registration"
        form_input = selenium.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        form_input.clear()
        form_input.send_keys("john@simplylift.co")
        sleep(1)
        form_input.submit()
        sleep(1)
        assert selenium.current_url == 'http://localhost:8000/showSummary'
        first_link = selenium.find_element(By.CSS_SELECTOR, 'a[href="/book/Spring%20Festival/Simply%20Lift"]')
        first_link.click()
        sleep(1)
        assert selenium.current_url == 'http://localhost:8000/book/Spring%20Festival/Simply%20Lift'
        form_input = selenium.find_element(By.CSS_SELECTOR, 'input[name="places"]')
        form_input.clear()
        form_input.send_keys(1)
        sleep(1)
        form_input.submit()
        sleep(1)
        assert selenium.current_url == 'http://localhost:8000/purchasePlaces'
        rankings_link = selenium.find_element(By.LINK_TEXT, 'Ranking')
        rankings_link.click()
        sleep(1)
        assert selenium.current_url == 'http://localhost:8000/ranking?club=Simply+Lift'

