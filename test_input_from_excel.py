import re
import pytest
import openpyxl
from playwright.async_api import async_playwright, Page, expect

# STEP 1: Fixture to open the browser and initialize session
@pytest.fixture(scope="session")
async def initialized_page():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.theautomationchallenge.com/")

        # Login process
        await page.get_by_role("button", name="SIGN UP OR LOGIN").click()
        await page.get_by_role("button", name="OR LOGIN", exact=True).click()
        await page.get_by_role("textbox", name="Email").fill("mariana@email.com")
        await page.get_by_role("textbox", name="Password").fill("1234")
        await page.get_by_role("button", name="LOG IN").click()

        # Verify successful login
        await expect(page.get_by_role("button", name="SIGN UP OR LOGIN")).to_be_hidden()

        # Start the challenge
        await page.get_by_role("button", name="Start").click()
        await expect(page.get_by_role("button", name="Submit")).to_be_visible()

        yield page  # Keep session open

        await browser.close()

# STEP 2: Load data from Excel
def read_excel_file(file_path):
    # Define variable to load the Excel workbook
    workbook = openpyxl.load_workbook(file_path)

    # Define variable to read sheet. Then define an empty data list
    sheet = workbook.active
    data = []

    # Append each row to a list, without including the headers
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
    return data[1:]  # This ensures headers are excluded

# Load data from the Excel file
excel_data = read_excel_file("challenge.xlsx")
print(excel_data)

# STEP 3: Function to locate input fields dynamically
async def get_input_field(page: Page, label_text: str):
    locators = await page.locator("div.bubble-element.Group").filter(has_text=f"{label_text}").all()

    for group_locator in locators:
        if await group_locator.is_visible() and await group_locator.text_content() == label_text:
            input_locators = await group_locator.locator("input").all()
            for input_locator in input_locators:
                if await input_locator.is_visible():
                    print("Found visible input within the group")
                    return input_locator  

# STEP 4: Test function with parameterized data
@pytest.mark.parametrize("employer_identification_number, company_name, sector, company_address, automation_tool, annual_automation_saving, date_of_first_project", excel_data)
async def test_input_from_excel(initialized_page: Page, employer_identification_number, company_name, sector, company_address, automation_tool, annual_automation_saving, date_of_first_project):

    page = initialized_page  # Aliasing for readability

    # Steps to handle the random reCAPTCHA
    recaptcha = page.get_by_role("button", name="presentation")
    recaptcha_is_visible = await recaptcha.is_visible()

    if recaptcha_is_visible:
        await recaptcha.click()

    # Company Name
    company_name_input = await get_input_field(page, "Company Name")
    await company_name_input.wait_for(state="visible")
    await company_name_input.fill(company_name)
    print(f"Filled Company Name: {company_name}")

    # Sector
    sector_input = await get_input_field(page, "Sector")
    await sector_input.wait_for(state="visible")
    await sector_input.fill(sector)
    print(f"Filled Sector: {sector}")

    # Address
    address_input = await get_input_field(page, "Address")
    await address_input.wait_for(state="visible")
    await address_input.fill(company_address)
    print(f"Filled Address: {company_address}")

    # EIN
    ein_input = await get_input_field(page, "EIN")
    await ein_input.wait_for(state="visible")
    await ein_input.fill(employer_identification_number)
    print(f"Filled Address: {employer_identification_number}")

    # Automation Tool
    automation_tool_input = await get_input_field(page, "Automation Tool")
    await automation_tool_input.wait_for(state="visible")
    await automation_tool_input.fill(automation_tool)
    print(f"Filled Address: {automation_tool}")

    # Annual Saving
    annual_saving_input = await get_input_field(page, "Annual Saving")
    await annual_saving_input.wait_for(state="visible")
    await annual_saving_input.fill(annual_automation_saving)
    print(f"Filled Address: {annual_automation_saving}")

    # Date
    date_input = await get_input_field(page, "Date")
    await date_input.wait_for(state="visible")
    await date_input.fill(date_of_first_project)
    print(f"Filled Address: {date_of_first_project}")

    # Verify all inputs were filled correctly
    assert await company_name_input.input_value() == company_name, "Company Name mismatch!"
    assert await sector_input.input_value() == sector, "Sector mismatch!"
    assert await address_input.input_value() == company_address, "Address mismatch!"
    assert await ein_input.input_value() == employer_identification_number, "EIN mismatch!"
    assert await automation_tool_input.input_value() == automation_tool, "Automation Tool mismatch!"
    assert await annual_saving_input.input_value() == annual_automation_saving, "Annual Saving mismatch!"
    assert await date_input.input_value() == date_of_first_project, "Date mismatch!"

    print("All fields filled successfully")

    # Submit data
    await page.get_by_role("button", name="Submit").click()
    print("Data was submitted")
