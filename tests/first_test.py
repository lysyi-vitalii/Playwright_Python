from playwright.sync_api import Page, expect


def login_with_invalid_creds(page: Page):
    page.goto("https://testomat.io")

    #expect(page.locator(".login_item")).to_be_visible()
    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()

    page.locator("#content-desktop #user_email").fill("lasjhjd@gmail.com")
    page.locator("#content-desktop #user_password").fill("wqead")
    page.locator("#content-desktop .common-btn-lg").click()

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info-right")).to_have_text("Invalid Email or password.")
    expect(page.locator("#content-desktop .common-flash-info-left")).to_be_visible()

    expect(page).to_have_title("Testomat.io") #AI Test Management Tool |
    #expect(page).to_be_empty()

