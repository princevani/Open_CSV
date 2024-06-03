from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from datetime import datetime
import time

# Set up Edge options to spoof the User-Agent and disable images
edge_options = Options()
edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
edge_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize the WebDriver
driver = webdriver.Edge(options=edge_options)

def fetch_data_for_year(year):
    # Open the website
    driver.get("https://www.nseindia.com/reports-indices-historical-index-data")

    # Wait until the 'Index' dropdown is clickable
    index_dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "hpReportIndexTypeSearchInput"))
    )

    # Select 'Nifty Bank' from the dropdown menu
    select = Select(index_dropdown)
    select.select_by_value("NIFTY BANK")

    # Wait for the period options to be visible
    custom_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-val='Custom']"))
    )
    custom_option.click()

    # Wait for the date pickers to be enabled
    start_date_picker = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "startDate"))
    )
    end_date_picker = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "endDate"))
    )

    # Input the date range using JavaScript
    start_date = f"01-01-{year}"
    end_date = f"31-12-{year}"

    driver.execute_script(f"document.getElementById('startDate').value = '{start_date}'")
    driver.execute_script(f"document.getElementById('endDate').value = '{end_date}'")

    # Ensure date fields are set correctly by clicking outside the date picker
    driver.execute_script("document.getElementById('startDate').dispatchEvent(new Event('change'))")
    driver.execute_script("document.getElementById('endDate').dispatchEvent(new Event('change'))")

    # Click the 'Go' button
    go_button = driver.find_element(By.CSS_SELECTOR, "button.filterbtn.hpreport-getdata-btn")
    go_button.click()

    # Wait for the data to load
    time.sleep(10)

    # Download the data
    download_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "CFanncEquity-download"))
    )
    download_link.click()

    # Wait for the download to complete
    time.sleep(5)

# Loop through the years and fetch data
current_year = datetime.now().year
for year in range(2015, 2016):
    fetch_data_for_year(year)

# Close the WebDriver
driver.quit()
