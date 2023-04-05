import sys
import time
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

region = sys.argv[1]
hwid = sys.argv[2]

def closedb():
    cursor.close()
    connection.close()

if region == 'eu':
    dbip = 'IP address'
elif region == 'us':
    dbip = 'IP address'
else:
    print('Incorrect region.')
    sys.exit()

# Database connection configuration
config = {
    'user': 'username',
    'password': 'password',
    'host': dbip,
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

query = f"SELECT kvm_url, kvm_user, kvm_password FROM hardware_systems WHERE id = {hwid};"
cursor.execute(query)
result = cursor.fetchone()

kvm_url, kvm_user, kvm_password = result

closedb()

# Print the values
print("kvm_url:", kvm_url)
print("kvm_user:", kvm_user)
print("kvm_password:", kvm_password)

chromedriver_path = '/usr/bin/chromedriver'
browser = webdriver.Chrome(chromedriver_path)
browser.get(f'http://{kvm_url}')
actions = ActionChains(browser)

time.sleep(1)

actions = ActionChains(browser)

actions.send_keys(Keys.TAB * 4)
actions.send_keys(Keys.ENTER)
actions.perform()

time.sleep(.5)

actions.reset_actions()
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.ENTER)
actions.perform()

time.sleep(5)

actions.reset_actions()
actions.send_keys(kvm_user)
actions.send_keys(Keys.TAB)
actions.send_keys(kvm_password)
actions.send_keys(Keys.ENTER)
actions.perform()

try:
    while True:
        browser.title 
        time.sleep(1)
except WebDriverException:
    print("Browser closed")
