import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.bt.com/")
driver.maximize_window()


'''Using the XPATH "//a[@class='call' and text()='Accept all cookies']" for "Accept all cookies" button locator, 
its is detected in DOM element but not via selenium.
Throws error as :
File "C:\Users\ankita.ghosh\PycharmProjects\BTGroup\PageObject\HomePage.py", line 14, in <module>
    alert_popup = driver.find_element(By.XPATH, "//a[@class='call' and text()='Accept all cookies']")
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ankita.ghosh\PycharmProjects\BTGroup\venv\Lib\site-packages\selenium\webdriver\remote\webdriver.py", line 738, in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hence, while runnig the code I have manually accepted the "Accept all cookies" button so that other TC's can be executed.
Below is the idea how we can click the element.
'''
# 1.Close accept Cookie pop-up if it appears
try:
    # Wait for the element to be clickable (max 10 seconds)
    accept_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='call' and text()='Accept all cookies']"))
    )

    # Click the "Accept all cookies" button
    accept_cookies_button.click()
except Exception:
    pass


# 2. Hover to Mobile menu
hover_mobile_element = driver.find_element(By.XPATH, "(//span[contains(text(),'Mobile')])[1]")
action_chains = ActionChains(driver)
# Perform the hover action
action_chains.move_to_element(hover_mobile_element).perform()

# 3.From mobile menu, select Mobile phones
try:
    element_to_click = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(@href,'/products/mobile/phones/')]")) and
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/products/mobile/phones/')]"))
    )

    # Click the element
    element_to_click.click()
except Exception as e:
    print(f"Error clicking Mobile phones: {str(e)}")


# 5. Verify the number of banners
banners = driver.find_elements(By.XPATH, "//div[contains(@class, 'flexpay-card_card_wrapper__Antym')]")
assert len(banners) >= 3, "Number of banners is less than 3"
print("number of banners are not less than: ", len(banners))


# 6. Scroll down and click View SIM only deals
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
view_sim_deals = driver.find_element(By.XPATH, "//a[text()='View SIM only deals']")
view_sim_deals.click()


# 7. Validate the title for new page.
expected_title = "SIM Only Deals | Compare SIMO Plans & Contracts | BT Mobile"
print(driver.title)
assert expected_title in driver.title, f"Expected title '{expected_title}' not found"

# 8. Validate the promotion text
plans = driver.find_element(By.XPATH, "(//div[contains(text(),'250GB')])[3]")
data_plan = plans.text
print(data_plan)
expected_text = '250GB'
assert plans.text == expected_text, f"Expected promotion text not found: {expected_text}"


driver.close()
