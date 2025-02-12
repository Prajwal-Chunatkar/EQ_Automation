from test.ui import ui_pages
from testdata.cp_testData import LoginDetails


def test_perform_homepagevalidations(ui: ui_pages):
    ui.loginpage.user_login(LoginDetails.username,LoginDetails.password)
