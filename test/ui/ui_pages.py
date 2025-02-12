from test.lib.ui_lib.UI_loginpage import LoginPage


class UI_Pages(object):

    def __init__(self,driver):
        self.loginpage = LoginPage(driver)
