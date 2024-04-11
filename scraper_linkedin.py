# Import các thư viện cần thiết
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
from time import sleep
from selenium.common.exceptions import TimeoutException

print('- Finish importing packages')

# Khởi tạo trình duyệt Chrome và truy cập trang đăng nhập LinkedIn
driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')

try:
    # Đợi cho trường email và mật khẩu xuất hiện và nhập thông tin
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'session_password'))
    )
except TimeoutException:
    print("Email or password field not found within the specified timeout period.")
    driver.quit()

# Đọc thông tin đăng nhập từ tệp văn bản
try:
    with open('linkedin_hoang.txt', 'r') as credential:
        lines = credential.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
except FileNotFoundError:
    print("Error: The file 'linkedin_login.txt' was not found.")
    driver.quit()

# Nhập thông tin đăng nhập và nhấp vào nút Đăng nhập
email_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

print('- Finish Task 1: Login to Linkedin')

# Đợi cho ô tìm kiếm xuất hiện và nhập truy vấn tìm kiếm
try:
    search_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))
    )
except TimeoutException:
    print("Search field not found within the specified timeout period.")
    driver.quit()

search_query = input('What profile do you want to scrape? ')
search_field.send_keys(search_query)
search_field.send_keys(Keys.RETURN)

print('- Finish Task 2: Search for profiles')

# Hàm để lấy danh sách URL từ một trang
def get_profile_urls():
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    profiles = page_source.find_all('a', class_='app-aware-link')
    all_profile_urls = []
    for profile in profiles:
        profile_url = profile.get('href')
        if profile_url not in all_profile_urls:
            all_profile_urls.append(profile_url)
    return all_profile_urls

# Lặp qua nhiều trang và lấy danh sách URL của các hồ sơ
num_pages = int(input('How many pages do you want to scrape? '))
all_profile_urls = []
for _ in range(num_pages):
    all_profile_urls.extend(get_profile_urls())
    sleep(2)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(3)
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'artdeco-pagination__button--next'))
        )
        next_button.click()
    except TimeoutException:
        print("Next button not found within the specified timeout period.")
        break
    sleep(2)

print('- Finish Task 3: Scrape the URLs')

# Hàm để lấy dữ liệu từ một hồ sơ LinkedIn và ghi vào tệp CSV
def scrape_profile_data(profile_url):
    driver.get(profile_url)
    print('- Accessing profile: ', profile_url)
    sleep(3)
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    info_div = page_source.find('div', class_='flex-1 mr5')
    try:
        name = info_div.find('li', class_='inline t-24 t-black t-normal break-words').get_text().strip()
        location = info_div.find('li', class_='t-16 t-black t-normal inline-block').get_text().strip()
        title = info_div.find('h2', class_='mt1 t-18 t-black t-normal break-words').get_text().strip()
        return {'Name': name, 'Location': location, 'Job Title': title, 'URL': profile_url}
    except AttributeError:
        print("Error: Profile data not found.")
        return None

# Lặp qua danh sách URL và ghi dữ liệu vào tệp CSV
with open('output.csv', 'w', newline='') as file_output:
    headers = ['Name', 'Job Title', 'Location', 'URL']
    writer = csv.DictWriter(file_output, fieldnames=headers)
    writer.writeheader()
    for profile_url in all_profile_urls:
        profile_data = scrape_profile_data(profile_url)
        if profile_data:
            writer.writerow(profile_data)

print('Mission Completed!')
