import time

from selenium.webdriver.common.by import By

from test.lib.ui_lib.BasePage import BasePage


class LoginPage(BasePage):

    def __init__(self,driver):
        BasePage.__init__(self,driver)

    CONTRACT_PHARMACY = (By.XPATH, "//strong[text()='Contract Pharmacy']")
    STARTER_KIT = (By.XPATH, "//strong[text()='STARTER KIT']")
    WELCOME = (By.XPATH, "//strong[text()='Welcome!']")
    SIGN_IN_LABEL = (By.XPATH, "//strong[text()='Sign in']")
    USERNAME = (By.ID, "normal_login_username")
    PASSWORD = (By.ID, "normal_login_password")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    LOGIN_BUTTON = (By.XPATH, "//span[text()='Login']")
    OTP_TEXT = (By.XPATH, "//span[text()='Enter the One Time Password sent to your Email ID']")
    OTP_TEXT1 = (By.XPATH, "//span[text()='to your registered email account']")
    VERIFY_BUTTON = (By.XPATH, "//span[text()='Verify']")
    BACK = (By.XPATH, "//span[text()='Back']")
    Resend = (By.XPATH, "//span[text()='Resend']")
    VERIFY_YOUR_IDENTITY = (By.XPATH, "//strong[text()='Verify your identity']")
    ENTER_OTP = (By.XPATH, "//div/child::input")
    SENT_SUCCESSFULLY_TEXT = (
        By.XPATH, "//span[text()='A One Time Password has been sent to your registered Email ID']")
    TOTAL_ROWS = (By.XPATH, "//div[@class='os-content']/table/tbody/tr")
    MAIL_SINGLE_ROW = "//div[@class='os-content']/table/tbody/tr["
    MAIL_SINGLE_COLUMN = "]/td"
    SINGLE_ROW = "//table/tbody/tr["
    SINGLE_COLUMN = "]/td"
    LOGOUT_DOWN_ARROW = (By.CSS_SELECTOR, ".ant-avatar.ant-avatar-circle.css-1gaypts")
    LOGOUT = (By.XPATH, "//span[text()='Logout']")
    DOT_BUTTON = (
        By.XPATH,
        "//table/tbody/tr[1]/td/span[text()='testuser1686123877']/parent::td/following-sibling::td/button/span")
    INCORRECT_LOGIN_DETAILS = (By.XPATH, "//b[text()='Invalid Password. Please try again.']")
    NUMBER_OF_LOGIN_ATTEMPTS_TWO = (By.XPATH, "//div[contains(.,'Remaining attempts: 2')]/b")
    NUMBER_OF_LOGIN_ATTEMPTS_ONE = (By.XPATH, "//div[contains(.,'Remaining attempt: 1')]/b")
    LOGIN_ATTEMPT_FAILED = (By.XPATH, "//b[text()='Your account is Locked due to 3 failed attempts.']")
    REGISTRATION_LINK_SENT_TO_EMAIL = (By.XPATH, "//div[contains(text(),'We have sent a password reset link to your "
                                                 "registered Email ID. If it does not appear within a few minutes, "
                                                 "check your spam folder, or contact administrator.')]")

    def get_total_rows(self):
        return self.driver.find_elements(*LoginPage.TOTAL_ROWS)

    def user_lock_login(self, username, password):
        self.verify_element_present(self.CONTRACT_PHARMACY, 30)
        self.element_visible(self.STARTER_KIT)
        self.element_visible(self.WELCOME)
        self.element_visible(self.SIGN_IN_LABEL)
        self.element_visible(self.LOGIN_BUTTON)
        self.clear_input_text(self.USERNAME)
        self.send_Keys(self.USERNAME, username)
        self.clear_input_text(self.PASSWORD)
        self.send_Keys(self.PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON)

    def user_login(self, username, password):
        title = self.get_title()
        assert title.lower() == "PATIENT FIRST".lower()
        # self.verify_element_present(self.CONTRACT_PHARMACY, 30)//these element not present on dashboard
        # self.element_visible(self.STARTER_KIT)
        self.element_visible(self.WELCOME)
        self.element_visible(self.SIGN_IN_LABEL)
        self.element_visible(self.LOGIN_BUTTON)
        self.send_keys(self.USERNAME, username)
        self.send_keys(self.PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON)
        self.verify_element_present(self.SENT_SUCCESSFULLY_TEXT, 60)
        text = self.get_text(self.SENT_SUCCESSFULLY_TEXT)
        assert text == "A One Time Password has been sent to your registered Email ID"
        # self.verify_element_present(self.OTP_TEXT, 30)//need to modify this logic
        otp = []
        otp = self.read_email_mailinator(username, self.TOTAL_ROWS, 1, 1, LoginPage.MAIL_SINGLE_ROW,
                                         LoginPage.MAIL_SINGLE_COLUMN, "Your login verification - One "
                                                                       "Time Password (OTP)")
        print(otp)
        if text == 'A One Time Password has been sent to your registered Email ID':
            self.driver.find_element(By.XPATH, "//div/child::input[1]").send_keys(otp[0])
            self.driver.find_element(By.XPATH, "//div/child::input[2]").send_keys(otp[1])
            self.driver.find_element(By.XPATH, "//div/child::input[3]").send_keys(otp[2])
            self.driver.find_element(By.XPATH, "//div/child::input[4]").send_keys(otp[3])
            self.driver.find_element(By.XPATH, "//div/child::input[5]").send_keys(otp[4])
            self.driver.find_element(By.XPATH, "//div/child::input[6]").send_keys(otp[5])
        self.click_element(self.VERIFY_BUTTON)
        time.sleep(2)

    def user_logout(self):
        time.sleep(.5)
        self.verify_element_present(self.LOGOUT_DOWN_ARROW, 30)
        # self.move_to_Element(self.LOGOUT_DOWN_ARROW)
        # self.click_element(self.LOGOUT_DOWN_ARROW)
        self.move_to_Element(self.LOGOUT_DOWN_ARROW)
        time.sleep(.5)
        self.click_element(self.LOGOUT)
        self.verify_element_present(self.USERNAME, 30)
