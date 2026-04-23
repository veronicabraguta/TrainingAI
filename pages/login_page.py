from playwright.sync_api import expect

class LoginPage:

    def __init__(self, page):
        self.page = page
        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.flash_message = page.locator("#flash")

    def navigate(self):
        self.page.goto("https://the-internet.herokuapp.com/login")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def assert_flash_message(self, expected_text):
        expect(self.flash_message).to_be_visible()
        expect(self.flash_message).to_contain_text(expected_text)