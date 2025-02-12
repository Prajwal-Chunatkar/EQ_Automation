import time

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from testdata.cp_testData import EmailNotification


class BasePage(object):

    def __init__(self,driver):
        self.driver = driver

    def send_keys(self, locator, value):
        wait = WebDriverWait(self.driver, 30)
        element = wait.until(ec.presence_of_element_located(locator))
        element.clear()
        element.send_keys(value)

    def scroll_into_view(self, locator):
        # Run JavaScript to scroll until the element is in view
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(ec.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def clear_input_text(self, locator):
        wait = WebDriverWait(self.driver, 30)
        element = wait.until(ec.presence_of_element_located(locator))
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)

    def web_table_handle(self, tableRows, startRow, startColumn, locator1, locator2):
        wait = WebDriverWait(self.driver, 30)
        elements = wait.until(ec.presence_of_all_elements_located(tableRows))
        totalTableCount = len(elements)
        if totalTableCount == 1:
            totalTableCount = totalTableCount + 1
        print(totalTableCount)
        for i in range(startRow, totalTableCount):
            numberofcolumnsinrow = len(self.driver.find_elements(By.XPATH, locator1 + str(i) + locator2))
            time.sleep(1)
            for j in range(startColumn, numberofcolumnsinrow):
                web_element = self.driver.find_element(By.XPATH,
                                                       locator1 + str(i) + locator2 + "[" + str(j) + "]")
                content = web_element.text
                iframe = self.driver.find_element(By.ID, "html_msg_body")
                if content == EmailNotification.login_otp_sub:
                    web_element.click()
                    time.sleep(2)
                    self.driver.switch_to.frame(iframe)
                    otp = self.driver.find_element(By.XPATH, "//table/tbody/tr/td/p[contains(.,'To log into the "
                                                             "application')]").text
                    new = str(otp)
                    new_otp = new.split()[14]
                    return new_otp
                elif content == EmailNotification.reset_password_sub:
                    web_element.click()
                    time.sleep(.5)
                    self.driver.switch_to.frame(iframe)
                    reset_pwd_link = self.driver.find_element(By.XPATH, "//table/tbody/tr/td/p/a/following-sibling::a")
                    link = reset_pwd_link.text
                    time.sleep(.5)
                    return link
                elif content == EmailNotification.app_locked_sub:
                    web_element.click()
                    time.sleep(.5)
                    self.driver.switch_to.frame(iframe)
                    reset_pwd_link = self.driver.find_element(By.XPATH, "//table/tbody/tr/td/p/a/following-sibling::a")
                    unlocked_link = reset_pwd_link.text
                    time.sleep(.5)
                    return unlocked_link
                elif content == EmailNotification.forgot_password_sub:
                    web_element.click()
                    time.sleep(.5)
                    self.driver.switch_to.frame(iframe)
                    reset_pwd_link = self.driver.find_element(By.XPATH, "//table/tbody/tr/td/p/a/following-sibling::a")
                    forgot_password_link = reset_pwd_link.text
                    time.sleep(.5)
                    return forgot_password_link


    def get_url(self, url):
        self.driver.get(url)

    def screenshot(self, fileName):
        self.driver.get_screenshot_as_file(fileName)

        # text may be frame id or frame name or index value

    def switch_to_iframe(self, locator):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(ec.presence_of_element_located(locator))
        self.driver.switch_to.frame(element)

    def verify_element_present(self, locator, duration):
        wait = WebDriverWait(self.driver, duration)
        wait.until(ec.presence_of_element_located(locator))


    def java_script_click(self, locator):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(ec.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def scroll(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    def get_text(self, locator):
        time.sleep(.5)
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(ec.presence_of_element_located(locator))
        return element.text


    def click_element(self, locator):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(ec.presence_of_element_located(locator))
        element.click()

    def element_visible(self, locator):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(ec.presence_of_element_located(locator))
        status = element.is_displayed()
        return status

    def read_email_mailinator(self, username, total_rows, row, column, locator1, locator2,text):
        parentWindow = self.driver.current_window_handle
        self.driver.execute_script("window.open('https://www.mailinator.com/')")
        time.sleep(.2)
        childWindow = self.driver.window_handles
        for child in childWindow:
            if child != parentWindow:
                self.driver.switch_to.window(child)
                self.driver.maximize_window()
                time.sleep(2)
                self.driver.find_element(By.ID, "search").send_keys(username)
                self.driver.find_element(By.XPATH, "//button[text()='GO']").click()
                time.sleep(5)
                otp = self.web_table_handle(total_rows, row, column, locator1,
                                            locator2, text)
                self.driver.close()
                time.sleep(1)
                self.driver.switch_to.window(parentWindow)
                time.sleep(1)
                return otp

    def move_to_Element(self, locator):
        action = ActionChains(self.driver)
        wait = WebDriverWait(self.driver, 30)
        element = wait.until(ec.presence_of_element_located(locator))
        action.move_to_element(element).perform()
    def get_title(self):
        return self.driver.title
