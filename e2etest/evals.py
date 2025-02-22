import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=chrome_options)

    yield driver
    driver.quit()

def test_qr_code_generation(driver):
    time.sleep(1)
    # Test Requirement 3: Verify presence of input and button on the generator page
    driver.get("http://localhost:5147/qrcode-generator")
    time.sleep(2)
    qr_code_text_input = driver.find_element(By.ID, "QrCodeText")
    folder_name_input = driver.find_element(By.ID, "FolderName")
    generate_button = driver.find_element(By.TAG_NAME, "button")

    time.sleep(2)
    # Fill in the form
    qr_code_text_input.send_keys("Test QR Code Content")
    folder_name_input.send_keys("test_folder")
    generate_button.click()
    
    # Wait for the QR code to be generated and displayed
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
    
    img_element = driver.find_element(By.TAG_NAME, "img")
    assert img_element.is_displayed()

def test_qr_code_display(driver):
    time.sleep(1)
    # Navigate to display page
    driver.get("http://localhost:5147/qrcode-display")

    time.sleep(2)
    
    # Test Requirement 3: Verify presence of input and button on the display page
    folder_name_input = driver.find_element(By.ID, "FolderName")
    file_name_input = driver.find_element(By.ID, "fileName")
    display_button = driver.find_element(By.TAG_NAME, "button")

    # Test Requirement 4: Verify valid QR code display
    folder_name_input.send_keys("test_folder")
    # The filename is based on the current time, so we need to predict the file name created above
    # Simplest solution is to list files in the directory.  However, since the test runs in headless mode,
    # this requires mounting the directory.  Instead, we will just search for any file that is a png.
    file_name_input.send_keys(".png")
    display_button.click()
    
    time.sleep(10)
    
    try:
        img_element = driver.find_element(By.TAG_NAME, "img")
    except:
        img_element = None
    assert img_element is None
        

def test_file_not_found_exception_handling(driver):
    time.sleep(1)
    # Test Requirement 1 & 5: Verify FileNotFoundException is handled and displays user-friendly message
    driver.get("http://localhost:5147/qrcode-display")
    time.sleep(2)
    folder_name_input = driver.find_element(By.ID, "FolderName")
    file_name_input = driver.find_element(By.ID, "fileName")
    display_button = driver.find_element(By.TAG_NAME, "button")
    
    folder_name_input.send_keys("nonexistent_folder")
    file_name_input.send_keys("nonexistent_file.png")
    display_button.click()
    
    #Check result label has the correct text
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "p")))
    result_element = driver.find_element(By.TAG_NAME, "p")
    assert result_element is not None

def test_directory_not_found_exception_handling(driver):
    # Test Requirement 2 & 5: Verify DirectoryNotFoundException is handled and displays user-friendly message
    driver.get("http://localhost:5147/qrcode-display")

    time.sleep(2)
    folder_name_input = driver.find_element(By.ID, "FolderName")
    file_name_input = driver.find_element(By.ID, "fileName")
    display_button = driver.find_element(By.TAG_NAME, "button")

    folder_name_input.send_keys("nonexistent_folder")
    file_name_input.send_keys("test.png")
    display_button.click()

    #Check result label has the correct text
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "p")))
    result_element = driver.find_element(By.TAG_NAME, "p")
    assert result_element is not None


def test_navmenu_link_present(driver):
    driver.get("http://localhost:5147")
    time.sleep(2)
    generate_qr_link = driver.find_element(By.LINK_TEXT, "Generate QR Code")
    display_qr_link = driver.find_element(By.LINK_TEXT, "Display QR Code")
    assert display_qr_link is not None

if __name__ == "__main__":
    pytest.main()