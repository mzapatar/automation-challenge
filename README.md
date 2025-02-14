# Automation Challenge

This repository contains my solution to [The Automation Challenge](https://www.theautomationchallenge.com/) using **Playwright** and **pytest**. It automates the following workflow:

- Login to the site.
- Start timer.
- Read Excel file with 50 rows of data to input in the form.
- Locate each form field dinamucally.
- Fill all fields and submit the data until all 50 rows are used.

---

## Setup

### **Clone the Repository**
```bash
git clone https://github.com/mzapatar/automation-challenge.git
cd automation-challenge
```

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Install Playwright and Browsers**
```bash
python -m playwright install --with-deps
```

## Running the test
Use the following terminal command to run the test with the default configuration:
```bash
pytest
```
By default, the tests runs in headed mode in the Firefox browser (see Known Issues).

## Prerequisites

- Python 3.8+
- Playwright (for browser automation)
- pytest (for test execution)
- openpyxl (for reading Excel files)

To install all dependencies, run:
```bash
pip install -r requirements.txt
```

## Assumptions made during development

- The user already has Python and pip installed.
- The Excel file (challenge.xlsx) exists in the project root and contains valid test data. The file is provided when cloning the repository, but can also be obtained in [The Automation Challenge](https://www.theautomationchallenge.com/).
- The test credentials (mariana@email.com / 1234) are valid for login. The current iteration of this test suite does not support other users.

## Known issues

- During testing, it was determined that the timer for the challenge did not start properlly when using Chromium. The timer works with both Webkit and Firefox, hence using Firefox by default.
- Test suite may get stuck waiting for elements to be visible and/or enabled. This issue is currently being addressed.