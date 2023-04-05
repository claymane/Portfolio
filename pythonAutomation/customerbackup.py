import sys, time
import mysql.connector
import pyinputplus as pyip
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


customer_id = sys.argv[1]
# target_id = sys.argv[2]

email = 'username@company.com'
password = 'password'

def closedb():
    cursor.close()
    connection.close()

config = {
    'user': 'username',
    'password': 'password',
    'host': 'url',
    'database': 'database',
}

# Establish a connection to the database
connection = mysql.connector.connect(**config)
cursor = connection.cursor()

# Check if the connection is successful
if connection.is_connected():
    print("Successfully connected to the database!")
else:
    print("Failed to connect to the database.")
    closedb()
    sys.exit()

query1 = f"SELECT hardware_system_id, service_id, created, modified, deleted FROM server_gameservers WHERE customer_id = '{customer_id}' AND deleted IS NOT NULL;"
cursor.execute(query1)
result_set1 = cursor.fetchall()

formatted_result_set = []
for row1 in result_set1:
    hw_id = row1[0]
    query2 = f"SELECT name FROM hardware_categories WHERE id = {hw_id}"
    cursor.execute(query2)
    row2 = cursor.fetchone()
    formatted_result_set.append((f"service_id: {row1[1]}", f"category: {row2[0]}\n", f"created: {row1[2].strftime('%Y-%m-%d %H:%M:%S')}", f"modified: {row1[3].strftime('%Y-%m-%d %H:%M:%S')}", f"deleted: {row1[4].strftime('%Y-%m-%d %H:%M:%S')}\n"))

for row in formatted_result_set:
    print(*row)
    
closedb()

restoreService = pyip.inputNum('Service ID to restore: ')

s = Service('/usr/bin/chromedriver')
browser = WebDriver(service=s)
browser.get('URL')
actions = ActionChains(browser)

time.sleep(2)

actions.send_keys(email)
actions.send_keys(Keys.TAB)
actions.send_keys(password)
actions.send_keys(Keys.ENTER)
actions.perform()

time.sleep(5)

element = browser.find_element(By.CSS_SELECTOR, "body > main > div > div > div > main > main > div.mdc-data-table > div.mdc-data-table__table-container > table > tbody > tr:nth-child(2) > td:nth-child(1) > a")
element.click()

time.sleep(2)

element = browser.find_element(By.CSS_SELECTOR, "body > main > div > div > div > main > main > div.mdc-data-table > div.mdc-data-table__table-container > table > tbody > tr:nth-child(3) > td:nth-child(2) > a > b")
element.click()

time.sleep(2)

element = browser.find_element(By.CSS_SELECTOR, "body > main > div > div > div > main > main > div.content-search.svelte-1e63z9e > input")
element.click()

actions.reset_actions()
actions.send_keys(restoreService)
actions.send_keys(Keys.ENTER)
actions.perform()

try:
    while True:
        browser.title
        time.sleep(1)
except WebDriverException:
    print("Browser closed")
                           
