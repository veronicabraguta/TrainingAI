import pytest
from pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        ("tomsmith", "SuperSecretPassword!", "You logged into a secure area!"),
        ("tomsmith", "wrongpassword", "Your password is invalid!"),
        ("wronguser", "SuperSecretPassword!", "Your username is invalid!"),
    ]
)
def test_login(page, username, password, expected_message):
    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login(username, password)
    login_page.assert_flash_message(expected_message)