from playwright import sync_playwright


def run(playwright, postcode: str, housenumber: str):
    browser = playwright.chromium.launch(headless=True)
    context = browser.newContext()

    # Open new page
    page = context.newPage()

    # Go to https://www.ah.nl/
    page.goto("https://www.ah.nl/")

    # Click //button[normalize-space(.)='Accepteer']
    page.click("//button[normalize-space(.)='Accepteer']")
    # assert page.url == "https://www.ah.nl/"

    # Click text="Online bestellen"
    page.click("text=\"Online bestellen\"")
    # assert page.url == "https://www.ah.nl/kies-een-moment"

    # Click input[name="easyTrial.postalCodeNld"]
    page.click("input[name=\"easyTrial.postalCodeNld\"]")

    # Fill input[name="easyTrial.postalCodeNld"]
    page.fill("input[name=\"easyTrial.postalCodeNld\"]", postcode)

    # Press Tab
    page.press("input[name=\"easyTrial.postalCodeNld\"]", "Tab")

    # Fill input[name="easyTrial.houseNumber"]
    page.fill("input[name=\"easyTrial.houseNumber\"]", housenumber)

    # Click text="Ga verder met online bestellen"
    # with page.expect_navigation(url="https://www.ah.nl/kies-een-moment/bezorgen"):
    with page.expect_navigation():
        page.click("text=\"Ga verder met online bestellen\"")
    
    result_json = None

    with page.expect_response("**/kies-een-moment/csrf/slots") as response:
        result_json = response.value.json()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()
    return result_json


def get_slots_json(postcode: str, housenumber: str):
    with sync_playwright() as playwright:
        return run(playwright, postcode, housenumber)
