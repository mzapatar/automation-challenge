# Automation Challenge

This repository contains my solution to [The Automation Challenge](https://www.theautomationchallenge.com/) using **Playwright** and **Python**. It automates the following workflow:

- Login to the site.
- Start timer.
- Read Excel file with 50 rows of data to input in the form.
- Locate each form field dynamically.
- Fill all fields and submit the data until all 50 rows are used.
- Handle the random reCAPTCHA that sometimes appears after clicking "Submit".

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
python main.py
```
By default, the script runs in headed mode in Chromium (Google Chrome).

## Prerequisites

- Python 3.8+
- Playwright (for browser automation)
- openpyxl (for reading Excel files)

To install all dependencies, run:
```bash
pip install -r requirements.txt
```

## Assumptions made during development

- The user already has Python and pip installed.
- The Excel file (challenge.xlsx) exists in the project root and contains valid test data. The file is provided when cloning the repository, but can also be obtained in [The Automation Challenge](https://www.theautomationchallenge.com/).
- The test credentials (mariana@email.com / 1234) are valid for login. The current iteration of this test suite does not support other users.