from playwright.sync_api import expect

def test_login_success(page):
    page.goto("https://the-internet.herokuapp.com/login")

    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")

    page.get_by_role("button", name="Login").click()

    success_message = page.locator("#flash")

    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text("You logged into a secure area!")
