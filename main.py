import config
import openpyxl
import asyncio
from playwright.async_api import async_playwright, Page, expect

# Function to load data from Excel
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

# Function to locate input fields dynamically
async def get_input_field(page: Page, label_text: str):
    # Locate all elements that include the label text
    locators = await page.locator("div.bubble-element.Group").filter(has_text=f"{label_text}").all()

    # Loop over each found element
    for group_locator in locators:
        if await group_locator.is_visible() and await group_locator.text_content() == label_text: # Checks that the elements are visible and include the label text
            input_locators = await group_locator.locator("input").all() # Finds all input fields inside the current group
            for input_locator in input_locators:
                if await input_locator.is_visible():
                    return input_locator # Returns the first visible input field 

# Main function to input data
async def main(page: Page, employer_identification_number, company_name, sector, company_address, automation_tool, annual_automation_saving, date_of_first_project):

    # Steps to handle the random reCAPTCHA (if visible)
    recaptcha_checkbox = page.get_by_role("button", name="presentation")
    if await recaptcha_checkbox.is_visible():
        await recaptcha_checkbox.click()

    # Fill the form fields dynamically
    fields = {
        "Company Name": company_name,
        "Sector": sector,
        "Address": company_address,
        "EIN": employer_identification_number,
        "Automation Tool": automation_tool,
        "Annual Saving": annual_automation_saving,
        "Date": date_of_first_project,
    }

    for label, value in fields.items():
        input_field = await get_input_field(page, label)
        await input_field.wait_for(state="visible", timeout = 3000)
        await input_field.fill(value, timeout = 3000)
        print(f"Filled {label}: {value}")
        await expect(input_field, f"{label} mismatch!").to_have_value(value) # Verify all inputs were filled correctly

    print("All fields filled successfully.")

    # Submit data
    await page.get_by_role("button", name="Submit").click()
    print("Data was submitted.")

# Function to run the script
async def run():
    excel_data = read_excel_file("challenge.xlsx")  # Read data from Excel
    
    # Open the browser and keep it open for all iterations
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.theautomationchallenge.com/") # Navigate to The Automation Challenge

        # Login process
        await page.get_by_role("button", name="SIGN UP OR LOGIN").click()
        await page.get_by_role("button", name="OR LOGIN", exact=True).click()
        await page.get_by_role("textbox", name="Email").fill(config.email)
        await page.get_by_role("textbox", name="Password").fill(config.password)
        await page.get_by_role("button", name="LOG IN").click()
        await expect(page.get_by_role("button", name="SIGN UP OR LOGIN"), "Faliure to login").to_be_hidden() # Verify successful login

        # Start the challenge
        await page.get_by_role("button", name="Start").click()
        await expect(page.get_by_role("button", name="Submit"), "Faliure to start the challenge, Submit button is not visible.").to_be_visible() # Verify that the Submit button is visible

        # Iterate through the Excel data, fill all fields, and submit data
        for row in excel_data:
            retries = 0  # Initialize retry counter
            max_retries = 3  # Maximum retry attempts
    
            while retries < max_retries:
                try:
                    await page.wait_for_timeout(30)  # Wait for reCAPTCHA
                    await main(page, *row)  # Call main function with row data
                    break  # If successful, exit the loop
                except Exception as e:
                    print(f"Error encountered: {e}")
                    retries += 1  # Increment retry counter
                    print(f"Retrying... Attempt {retries} of {max_retries}")

            if retries == max_retries:
                print(f"Skipping row after {max_retries} failed attempts.")

        # Verify that the data input had 100% accuracy
        await expect(page.get_by_text("Your success rate is"), "Success rate should be 100%.").to_contain_text("100%")
        print(f"All rows were submitted with 100% accuracy.")

        # Close browser after all iterations are done
        await browser.close()

# Run the script
if __name__ == "__main__":
    asyncio.run(run())