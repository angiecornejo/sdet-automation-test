
import pytest
import allure
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )

@pytest.fixture(scope="session")
def browser(pytestconfig):
    headless = pytestconfig.getoption("--headless")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless, 
            slow_mo=1000
        )
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context(
        locale="en-US",
        timezone_id="America/New_York",
        geolocation={"latitude": 37.7749, "longitude": -122.4194},  
        permissions=["geolocation"],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture
def google_setup(page):
    """Fixture that sets up Google search page with English language""" 
    from pages.bookSearch_page import BookSearch
    
    # Apply stealth to the page to avoid being detected as a bot
    # stealth_sync(page)

    page.goto('https://google.com')
    page.wait_for_load_state('networkidle')
    
    # Set to English (if available) to avoid lenguage inconsistencies
    try:
        page.get_by_text('English').click()
        page.wait_for_load_state('networkidle')
    except:
        pass  
    
    book_search = BookSearch(page)
    return book_search

# Hook for attaching screenshot on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = None
        
        page = item.funcargs.get("page")
        
        if not page:
            google_setup = item.funcargs.get("google_setup")
            if google_setup and hasattr(google_setup, 'page'):
                page = google_setup.page
        
        if page and hasattr(page, 'screenshot'):
            try:
                screenshot_bytes = page.screenshot(full_page=True)
                allure.attach(
                    screenshot_bytes,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                print("Screenshot attached to Allure report")
            except Exception as e:
                print(f"Could not take screenshot: {e}")
        else:
            print(f"No page found. Available fixtures: {list(item.funcargs.keys())}")

