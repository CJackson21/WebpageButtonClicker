# cjackson21@georgefox.edu
# 10/25/2023 automator for my office job

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
import time as t
from datetime import datetime


def automator(user, password, red, green, blue, desired_value):
    try:
        driver = webdriver.Chrome()
        url = 'https://buildertrend.net/Leads/LeadActivityCalendar.aspx'
        background_color = f"rgb({red}, {green}, {blue})"
        complete = 'btnMarkComplete'
        item_ids = []

        driver.get(url)

        # use WebDriverWait to wait for the login page to load completely
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))

        # finds username and password id's for input
        username_input = driver.find_element(By.ID, 'username')
        password_input = driver.find_element(By.ID, 'password')

        # sends username and password keys into field
        username_input.send_keys(user)
        password_input.send_keys(password)

        password_input.send_keys(Keys.RETURN)

        # Use WebDriverWait to wait for the "leadOpportunities" element to become visible
        activity_calendar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ctl00_ctl00_BaseMain_MainContentHolder_tc1_BTTab3_LinkButton1")))
        driver.execute_script("arguments[0].click();", activity_calendar)

        # continue loop until the specified date similar to format below. the day must always be 1 and the starting date must be lower than 
        # the desired value variable
        while desired_value != '7/1/2023':
            dropdown = Select(driver.find_element(By.ID, 'lstMasterCalendarDate'))
            dropdown.select_by_value(desired_value)
            t.sleep(2)

            # Use WebDriverWait to wait for elements with the specified background color to become present
            items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'[style*="background-color: {background_color}"]')))

            # Iterate through the elements and get their IDs
            for item in items:
                item_ids.append(item.get_attribute("id"))

            item_positions = [(item_id, driver.find_element(By.ID, item_id).location['y']) for item_id in item_ids]
            item_positions.sort(key=lambda x: x[1])

            sorted_item_ids = [item[0] for item in item_positions]

            for id in sorted_item_ids:
                try:
                    element = driver.find_element(By.ID, id)

                    # bunch of checks to make sure the elements can be found and clicked 
                    if element.is_displayed():
                        try:
                            element.click()
                            t.sleep(2)
                            complete_btn = driver.find_element(By.ID, complete)
                            if complete_btn.is_displayed():
                                try:
                                    mark_complete = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, complete)))        
                                    mark_complete.click()
                                    t.sleep(2)
                                except StaleElementReferenceException:
                                    print(f"Element with ID {id} became stale while waiting for mark complete")
                            else:
                                print(f"Complete button not visible for element with ID {id}")
                        except ElementClickInterceptedException:
                            print(f"Element with ID {id} is not clickable due to an intercepting element")
                    else:
                        print(f"Element with ID {id} is not visible")
                except NoSuchElementException:
                    print(f"Element with ID {id} does not exist")

            # get the date to increment to find new id to change pages
            parsed_date = datetime.strptime(desired_value, "%m/%d/%Y")
            day = parsed_date.day
            month = parsed_date.month
            year = parsed_date.year
            if month < 12:
                month += 1
            else:
                month = 1
                year += 1
            desired_value = f"{month}/{day}/{year}"

            # clear both lists so there is no clutter or errors popping up
            item_ids.clear()
            sorted_item_ids.clear()
    except Exception as e:
        print(f"An error occurred: {str(e)}")


    # Close the browser after you are done
    driver.quit()
    
# Close the browser after you are done
driver.quit()
