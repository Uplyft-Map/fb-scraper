from selenium.webdriver import ChromeOptions, Chrome
import time
import pickle

SCRAPE_URL = "https://mobile.facebook.com/confessatcarnegiemellon/"
NUM_SCROLLS = 50
SCROLL_DELAY = 0.5

options = ChromeOptions()
options.add_argument('headless')

driver = Chrome(options=options)
driver.get(SCRAPE_URL)

for i in range(NUM_SCROLLS):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_DELAY)

popup_close = driver.find_element_by_id("popup_xout")
popup_close.click()

more_buttons = driver.find_elements_by_partial_link_text("More")
for button in more_buttons:
    try:
        button.click()
    except:
        print("Tried to click something rip")

posts = driver.find_elements_by_class_name("story_body_container")
post_texts = ["\n".join(thing.text for thing in post.find_elements_by_tag_name('p')) for post in posts]

with open('cmu_confessions.pickle', 'wb') as f:
    pickle.dump(post_texts, f)

driver.close()
