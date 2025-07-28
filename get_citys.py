
from playwright.sync_api import sync_playwright




def put_varibles(playwright):
    browser = playwright.chromium.launch(headless=False)
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Custom-Header": "MyValue"
    }
    context = browser.new_context(extra_http_headers=custom_headers)
    page = browser.new_page()
    page.goto(start_url)


    # Get the stable container once
    container = page.locator("input[placeholder='Location']").locator(
        "xpath=ancestor::div[contains(@class, 'wpgb-select')]")

    for loc in locations:
        # Ensure toggle is clicked (opens the dropdown)
        toggle_button = container.locator("button.wpgb-select-toggle")
        toggle_button.click()

        # Locate fresh input inside dropdown after toggle
        input_box = container.locator("input[placeholder='Location']")

        # Wait for it to be visible
        input_box.wait_for(state="visible")

        # Fill and select
        input_box.fill(loc)
        page.keyboard.press("Enter")

        # Optional: wait for selection to be applied before next loop
        page.wait_for_timeout(500)  # Adjust if needed
    print("wuehuwherfu")
    container.locator("div.wpgb-select-placeholder").click()


with sync_playwright() as playwright:
    put_varibles(playwright)