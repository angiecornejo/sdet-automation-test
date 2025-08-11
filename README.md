# SDET-automation-test
#### 

### Overview
This repository provides an automated testing solution for a Google Shopping book search scenario, developed as part of the Swapcard SDET assessment. The framework is built with **Python**, **Pytest**, **Playwright**, and **Allure** reporting, following industry best practices for modern web automation testing.

### Project Structure
<img width="418" height="249" alt="image" src="https://github.com/user-attachments/assets/e39a5fe2-7a07-4b3a-949e-d00cec4879f6" />

## Quick Start

### Prerequisites
- Python **3.8+**
- `pip` (Python package manager)

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/angiecornejo/sdet-automation-test.git
cd sdet-automation-test
```

#### 2.Set up virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install Playwright browsers
```bash
playwright install
```

### Running Tests
_Basic Test Execution_
```bash
# Run all tests in headed mode 
pytest
```
```bash
# Run specific test file
pytest tests/test_bookSearch.py
```
```bash
# Run in headless mode
pytest --headless
```

The report is generated everytime the test runs, to access it, you can use the following command:
```bash
allure serve reports
```

### Test Scenario
The automated test performs the following steps:

1. **Navigate** to google.com
2. **Search** for "book {BOOK_NAME}" (e.g., "book Harry Potter", "book Game of thrones")
3. **Click** on the Shopping tab to filter results
4. **Sort** products by price from High to Low
5. **Set** maximum price filter to {AMOUNT} (e.g., 500, 1000)
6. **Verify** that the second listed product with rating has a rating ≥ {RATING} (e.g., 4.5, 3.9)

### Extra considerations: ⚠️ Important ⚠️
During development, I encountered an issue with **Google Captcha** detecting automated scripts and blocking interactions. Here’s what I tried and learned:

- **Fake User Agents**: In past projects, this method worked well to bypass bot detection. However, in this case, it was ineffective.
- **Playwright Stealth**: This library modifies browser properties and behaviors to make automation appear more “human-like.”  
  I experimented with it ([commented in `conftest.py` at line 50](./conftest.py)), and it partially worked:
  - Captcha didn’t appear.
  - But clicking certain buttons (like the **Shopping** tab) became impossible.
- **Unlocker API (Bright Data)**: This paid service worked but had limited free credits for testing.
- **CaptchaSolver**: Another paid alternative; I didn’t proceed due to cost.

When manually solving the captcha, the **entire script runs flawlessly**. While automated captcha-solving solutions exist, they:
- Often become outdated quickly (as captcha systems change frequently).
- Can take significant time to implement.
- Are generally discouraged unless absolutely necessary.

**Environment Setup Note:**  
To match your test results more closely, I configured my tests to:
- Run **from the United States** (geo-location).
- Display results **in English**.

### Assignment Requirements Implemented
* **Data Parametrization**: Test data is externalized using @pytest.mark.parametrize
* **Fixtures**: Custom fixtures for page setup and browser configuration
* **Page Object Model**: Clean separation of test logic and page interactions
* **Allure Reporting**: Comprehensive test reports with steps and attachments
* **Screenshot on Failure**: Automatic screenshot capture when tests fail
* **Headless/Headed Mode**: Configurable browser execution mode
* **Python + Pytest**: Core framework as requested

### Test Results — Allure Report
Last but not least, here’s a screenshot of the **Allure Report** generated after manually solving the Google Captcha. 🙂

<img width="1364" height="675" alt="image" src="https://github.com/user-attachments/assets/67d97876-3db5-468d-a1cd-c2c144c5ff15" />

✅ **Test 1 – Pass**: The second rated book’s score is greater than 3, meeting the expected criteria.

❌ **Test 2 – Fail**: The second rated book’s score is lower than 5, which does not meet the expected criteria.
