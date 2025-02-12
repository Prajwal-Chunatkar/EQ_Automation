import os
import platform
from urllib import request
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from test.ui.ui_pages import UI_Pages
from testdata.cp_testData import LoginDetails


# @pytest.fixture
# def api():
#     # Initiate drive and pass it to the pages
#     client = ApiClient()
#     gc_api = GC_Api(client)
#
#     # yield pages
#     yield gc_api
#     client.close()





@pytest.fixture()
def ui1():
    download_dir = 'C:\\test\\test_data'
    # Initiate drive and pass it to the pages
    # if platform.system() == 'Linux':
    #     download_dir = os.getenv('EQ_PROJECT_PATH', None)
    #     download_dir = 'C:\\test\\test_data'
    #
    #     # This varable is only set in git actions will return non when run locally.
    #     if download_dir is None:
    #         # For jenkins
    #         x = Path(__file__).parent.absolute()
    #         basePath = str(x).split('vitr-testing-vat-compliance')[0]
    #         download_dir = f'{basePath}/'  # other (unix)
    #
    #     download_dir += '_data'
    #
    # if not os.path.exists(download_dir):
    #     os.makedirs(download_dir)

    # browser = os.getenv('GC_BROWSER', 'Chrome')
    browser = 'Chrome'
    print('Running tests with', browser)
    print('Download Directory', download_dir)
    driver_path = "C:\\Users\\Prajwal.Chunatkar\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    if browser.lower() == 'chrome':
        prefs = {'download.default_directory': download_dir}
        if platform.system() == 'Windows':
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--start-maximized')
            options.add_argument('--remote-debugging-port=9222')
            options.add_argument('--disable-extensions')
            options.add_argument('--user-data-dir=C:\\test\\_data\\Chrome_Profile')
            options.add_argument('--profile-directory=Guest')
            options.add_experimental_option('prefs', prefs)
            # driver_options.add_argument('headless')

        elif platform.system() == 'Linux':
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-extensions')
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option('prefs', prefs)

        else:  # Mac
            prefs = {'download.default_directory': download_dir}
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--start-maximized')
            options.add_argument('--remote-debugging-port=9222')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-features=DownloadBubble')
            options.add_argument('--incognito')
            options.add_experimental_option('prefs', prefs)

        try:
            # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
            driver = webdriver.Chrome(driver_path)
            # driver = webdriver.Chrome(service=service, options=options)
        except TypeError:
            from selenium.webdriver.chrome.service import Service
            # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver = webdriver.Chrome(Service = driver_path, options=options)

    elif browser.lower() == 'firefox':
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.preferences.instantApply", True)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
        profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", download_dir)
        options = Options()
        options.headless = False
        if platform.system() == 'Linux':
            options.headless = True

        try:
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options, firefox_profile=profile)
        except TypeError:
            from selenium.webdriver.firefox.service import Service
            driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get(LoginDetails.url)
    ui_pages = UI_Pages(driver)

    # yield pages
    yield ui_pages
    driver.quit()


@pytest.fixture()
def ui2():
    download_dir = 'C:\\test\\test_data'
    browser = 'Chrome'
    print('Running tests with', browser)
    print('Download Directory', download_dir)
    driver_path = "C:\\Users\\Prajwal.Chunatkar\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    # if browser.lower() == 'chrome':
    driver = webdriver.Chrome(driver_path)
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get(LoginDetails.url)
    ui_pages = UI_Pages(driver)

    # yield pages
    yield ui_pages
    driver.quit()

@pytest.fixture()
def ui():
    # global driver
    directory = os.getcwd()
    env = "QA"
    # browser = request.config.getoption("--browser-name")
    browser = "chrome"
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": directory + "\DownloadFiles"})
        # services = Service(executable_path=ChromeDriverManager().install())
        service = Service("C:\\Users\\Prajwal.Chunatkar\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
        driver = webdriver.Chrome(service=service,options=options)
        driver.maximize_window()
        driver.delete_all_cookies()
    elif browser == "firefox":
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", directory + "\DownloadFiles")
        # driver = webdriver.Firefox(executable_path=directory + "\\resources\\drivers\\geckodriver64.exe")
        driver = webdriver.Firefox(firefox_profile=profile)
        driver.maximize_window()
    elif browser == "edge":
        # driver = webdriver.Ie(executable_path=directory + "\\resources\\drivers\\msedgedriver.exe")
        driver = webdriver.Edge()
    if env == "QA":
        driver.get("https://qa.equiscript.com/")
    if env == "DEV":
        driver.get("http://192.168.5.30/ESQFATWeb/")

    driver.implicitly_wait(10)
    # request.cls.driver = driver
    ui_pages = UI_Pages(driver)
    yield ui_pages
    driver.quit()

