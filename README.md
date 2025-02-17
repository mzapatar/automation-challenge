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

### Clone the Repository
Use the following terminal commands to clone the repository and then open the project folder:
```bash
git clone https://github.com/mzapatar/automation-challenge.git
cd automation-challenge
```

### Create a Virtual Environment (optional)
For Mac/Linux:
```bash
python -m venv venv
source venv/bin/activate
```
For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install Playwright and Browsers
```bash
python -m playwright install --with-deps
```

## Running the script
```bash
python main.py
```
By default, the script runs in **headed** mode in **Chromium (Google Chrome).**

## Assumptions made during development

- The user already has Python and pip installed. Depending on the versions installed, ```python3``` and ```pip3``` may be used instead of ```python``` and ```pip``` in the terminal.
- The Excel file (```challenge.xlsx```) exists in the project root and contains valid test data. The file is provided when cloning the repository, but can also be obtained in [The Automation Challenge](https://www.theautomationchallenge.com/).
- The credentials stored in ```config.py``` are valid for login.