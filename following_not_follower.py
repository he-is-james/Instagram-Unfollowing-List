import os
from dotenv import load_dotenv
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver

load_dotenv()

#Enter the credentials of the Instagram account
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

browser = webdriver.Chrome(executable_path=os.getenv('PATH_CHROMEDRIVER')) #Change the path
browser.implicitly_wait(5)

def login_account(username, password, browser):
    """
    Logs into a user's Instagram account and opens to the new updates feed page
    """
    browser.get('https://www.instagram.com')
    sleep(2)

    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")
    username_input.send_keys("", username)
    password_input.send_keys("", password)

    login_button = browser.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()
    tempy = browser.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
    tempy.click()
    sleep(2)
    #Uncomment the lines below if a second pop-up appears
    tempy2 = browser.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
    tempy2.click()
    sleep(2)

def get_unfollowers(browser):
    """
    Opens the profile, obtains the follower and following list
    Returns the names of the users who are in the following list, but not in the follower list
    """
    to_profile = browser.find_element(By.XPATH, "//a[contains(@href, '/{}')]".format(username))
    to_profile.click()
    sleep(3)
    to_following = browser.find_element(By.XPATH, "//a[contains(@href, '/following')]")
    to_following.click()
    # Pass in the element div containing all of the user div
    following_list = get_names(browser, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div')
    write_file('following.txt', following_list)
    print('Following list written')
    to_followers = browser.find_element(By.XPATH, "//a[contains(@href, '/followers')]")
    to_followers.click()
    # Pass in the element div containing all of the user div
    followers_list = get_names(browser, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div')
    write_file('followers.txt', followers_list)
    print('Followers list written')
    # Get the users who are in the following list but not in the followers list
    not_following_back = [user for user in following_list if user not in followers_list]
    write_file('not_following.txt', not_following_back)
    print('Not following you back list is written')

def get_names(browser, path):
    """
    Scrolls through the following/follower list to load all the usernames
    Returns a list of all the people in their respective list
    """
    sleep(2)
    scroll_box = browser.find_element(By.CLASS_NAME, "_aano")
    # Infinite scrolling until all the names have been found
    p_height, height = 0, 1
    while p_height != height:
        p_height = height
        sleep(2)
        height = browser.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll_box)
    # Gets the list of all the divs with the user handles
    total_list = scroll_box.find_element(By.XPATH, path)
    total_list = total_list.get_attribute('innerHTML')
    total_list = total_list.strip()
    # Wait to actually get the innerHTML string
    sleep(10)
    # Clean up the string to only get an array of user handles
    names = clean_names(total_list)
    close_dub = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button')
    close_dub.click()
    return names

def clean_names(listString):
    """
    Cleans the the divs to get the child div with the user handle name
    """
    names = []
    i = 0
    while (i < len(listString)):
        i = listString.find(' _ab8y  _ab94 _ab97 _ab9f _ab9k _ab9p _abcm') # 45 characters after 
        if i == -1:
            break
        # Add 45 to the index because the user handle begins there
        i += 45
        listString = listString[i:]
        # Get all characters before the end of the div tag
        name = ''
        for j in range(30):
            if listString[j] == '<':
                break
            name += listString[j]
        names.append(name)
    return names
    
def write_file(fileName, namesList):
    with open(fileName, 'w') as f:
        for name in namesList:
            f.write(name)
            f.write('\n')

login_account(username, password, browser)
get_unfollowers(browser)
sleep(5)
browser.close()