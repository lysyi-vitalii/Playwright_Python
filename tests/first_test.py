from playwright.sync_api import Page, expect

BASE_URL = "https://app.testomat.io/users/sign_in"


def test_login_with_invalid_creds(page: Page):
    open_home_page(page)

    # expect(page.locator(".login_item")).to_be_visible()
    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()

    page.locator("#content-desktop #user_email").fill("lasjhjd@gmail.com")
    page.locator("#content-desktop #user_password").fill("read")
    page.locator("#content-desktop .common-btn-lg").click()

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info-right")).to_have_text("Invalid email or password.")
    expect(page.locator("#content-desktop .common-flash-info-left")).to_be_visible()

    expect(page).to_have_title("Testomat.io")  # AI Test Management Tool |
    # expect(page).to_be_empty()


def test_login_with_valid_creds(page: Page):
    open_home_page(page)

    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()

    page.locator("#content-desktop #user_email").fill("semsonek@gmail.com")
    page.locator("#content-desktop #user_password").fill("tca!byt3hcz5KZG8wax")
    page.locator("#content-desktop .common-btn-lg").click()

    expect(page.locator("#content-desktop .common-flash-success-left")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-success-right")).to_have_text("Signed in successfully")


def test_search_project_in_company(page: Page):
    page.goto(BASE_URL)

    login_user(page, "semsonek@gmail.com", "tca!byt3hcz5KZG8wax")

    target_project = "Python Manufacture_1"

    search_for_project(page, target_project)

    expect(page.get_by_role("heading", name=target_project)).to_be_visible()

    expect(page.locator("ul li h3", has_text=target_project)).to_be_visible()

    expect(page.locator("ul li h3").first).to_have_text(target_project)

    expect(page.locator("ul li h3").filter(has_text=target_project).first).to_be_visible()


def test_should_be_possible_to_open_free_project(page: Page):
    # arrange
    page.goto(BASE_URL)
    login_user(page, email="semsonek@gmail.com", password="tca!byt3hcz5KZG8wax")
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    # act
    target_project = "Python Manufacture_1"
    search_for_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_hidden()

    # assert
    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)
    expect(page.locator("[src*='no-project.svg']")).to_be_visible()


def test_check_free_limits_reached(page: Page):
    page.goto(BASE_URL)
    login_user(page, email="semsonek@gmail.com", password="tca!byt3hcz5KZG8wax")
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    page.locator(".common-page-header-right .common-btn-lg").click()
    expect(page).to_have_url("https://app.testomat.io/benefits")

    expect(page.locator("h1")).to_have_text("Project limit is reached 😢")
    expect(page.locator("p.mt-5.text-xl.text-gray-500")).to_have_text("Subscribe to paid plans to unlock features.")


def search_for_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)


def open_home_page(page: Page):
    page.goto(BASE_URL)


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.locator("#content-desktop .common-btn-lg").click()
