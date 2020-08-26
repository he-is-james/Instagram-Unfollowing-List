from time import sleep
from selenium import webdriver

#Enter the credentials of the Instagram account
username = ""
password = ""

browser = webdriver.Chrome('C:\webdriver\chromedriver.exe') #Change the path
browser.implicitly_wait(5)

def login_account(username, password, browser):
    """
    Logs into a user's Instagram account and opens to the new updates feed page
    """
    browser.get('https://www.instagram.com')
    sleep(2)

    username_input = browser.find_element_by_name("username")
    password_input = browser.find_element_by_name("password")
    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = browser.find_element_by_xpath('//button[@type="submit"]')
    login_button.click()
    tempy = browser.find_element_by_xpath("//button[contains(text(), 'Not Now')]")
    tempy.click()
    sleep(2)
    #Uncomment the lines below if a second pop-up appears
    #tempy2 = browser.find_element_by_xpath("//button[contains(text(), 'Not Now')]")
    #tempy2.click()
    #sleep(2)

def get_unfollowers(browser):
    """
    Opens the profile, obtains the follower and following list
    Returns the names of the users who are in the following list, but not in the follower list
    """
    to_profile = browser.find_element_by_xpath("//a[contains(@href, '/{}')]".format(username))
    to_profile.click()
    sleep(3)
    to_following = browser.find_element_by_xpath("//a[contains(@href, '/following')]")
    to_following.click()
    following_list = get_name(browser)
    to_followers = browser.find_element_by_xpath("//a[contains(@href, '/followers')]")
    to_followers.click()
    followers_list = get_name(browser)
    not_following_back = [user for user in following_list if user not in followers_list]
    
    print(not_following_back) #prints a list with every name separated by a comma
    #Below prints a much longer list but in a vertical format
    #print('\n'.join([str(i) for i in not_following_back]))

def get_name(browser):
    """
    Scrolls through the following/follower list to load all the usernames
    Returns a list of all the people in their respective list
    """
    sleep(2)
    scroll_box = browser.find_element_by_class_name('isgrP')
    p_height, height = 0, 1
    while p_height != height:
        p_height = height
        sleep(2)
        height = browser.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll_box)
    total_list = scroll_box.find_elements_by_tag_name('li')
    names = [name.text for name in total_list if name.text != '']
    close_dub = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")
    close_dub.click()
    return names

login_account(username, password, browser)
get_unfollowers(browser)
sleep(5)
browser.close()
