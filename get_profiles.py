from playwright.sync_api import sync_playwright

start_url='https://www.gibsondunn.com/lawyer/cannon-michael-q/'

def get_education(page):
    education_title = page.locator(":has-text('Education')")
    edu_list = education_title.locator("xpath=following-sibling::ul[1]/li")
    education = []
    for i in range(edu_list.count()):
        text = edu_list.nth(i).inner_text()
        education.append(text.strip())
    return education

def extract_each_profile(playwright):
    browser = playwright.chromium.launch(headless=False)
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    context = browser.new_context(extra_http_headers=custom_headers)
    page=browser.new_page()
    page.goto(start_url)
    name = page.locator("div.blurb-int h1").inner_text()
    profile=page.locator("div.contact-details")
    phone=profile.locator("a.tel-number").inner_text()
    email_locator=profile.locator("a[href^='mailto:']:not([href*='?'])").first.get_attribute("href")
    email=email_locator.replace("mailto:","") if email_locator else None
    locations = profile.locator("a[href*='/office/']")
    count = locations.count()
    locations = [locations.nth(i).inner_text() for i in range(count)]
    work_card=page.locator("a.card").get_attribute("href")
    education=get_education(page)
    

with sync_playwright() as playwright:
    extract_each_profile(playwright)
