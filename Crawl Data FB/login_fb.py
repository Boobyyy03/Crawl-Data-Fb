from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Initialize Chrome WebDriver
browser = webdriver.Chrome()

# Navigate to Facebook login page
browser.get("http://facebook.com/login")

try:
    # Wait for email and password fields to be present
    email_field = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    password_field = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'pass'))
    )

    # Read login credentials from a text file
    try:
        with open('fblogin.txt', 'r') as credential:
            lines = credential.readlines()
            username = lines[0].strip()
            password = lines[1].strip()
    except FileNotFoundError:
        print("Error: The file 'fblogin.txt' was not found.")
        browser.quit()
        exit()

    # Input login credentials and submit
    email_field.send_keys(username)
    password_field.send_keys(password)
    password_field.submit()
    print('- Task 1: Logged in to Facebook')
    time.sleep(5)
    
    #open Link post
    browser.get(r"LINK Post DATA")
    time.sleep(5)
    # Crawl posts and save to file
    try:
        with open('posts.txt', 'w', encoding='utf-8') as file:
            posts = browser.find_elements_by_xpath('//div[@data-pagelet="FeedUnit_0"]')
            for post in posts:
                try:
                    post_content = post.find_element_by_xpath('.//div[@data-testid="post_message"]').text
                    file.write(post_content + '\n')
                except NoSuchElementException:
                    print("Post content not found")
    except NoSuchElementException:
        print("No posts found")

except TimeoutException:
    print("Email or password field not found within the specified timeout period.")
    browser.quit()
