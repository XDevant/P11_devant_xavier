from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import pytest
from time import sleep
from flask import url_for
from gudlft import create_app
from test.conftest import TestConfig
from pytest_flask.live_server import LiveServer
from urllib.request import urlopen


@pytest.fixture(scope="session")
def app():
    app = create_app(config_class=TestConfig)
    yield app


@pytest.fixture(scope="session")
def live_server(app):
    live_server = LiveServer(app, 'localhost', 8000, 6)
    live_server.start()
    yield live_server


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


class TestLogin:
    def test_live_server(self, live_server, selenium):
        selenium.get(url_for('/'))
        assert selenium.title == "GUDLFT Registration"

    def test_login_page(self, selenium):
        selenium.get(url_for('/'))
        assert selenium.title == "GUDLFT Registration"
        form_input = selenium.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        form_input.clear()
        form_input.send_keys("john@simplylift.co")
        sleep(2)
        form_input.submit()
        sleep(2)
        assert selenium.current_url == 'http://localhost:8000/showSummary'
