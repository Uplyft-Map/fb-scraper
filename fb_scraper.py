from selenium.webdriver import Chrome
from collections import defaultdict, deque
from tqdm import tqdm
import time
import csv
import pickle

# Important constants
CONFESSION_URLS = 'school_confessions.csv'
NUM_SCROLLS = 50
SCROLL_DELAY = 0.5

# Load school dictionaries
SCHOOL_DICT = defaultdict(list)
with open(CONFESSION_URLS, 'r') as csvfile:
    rea = csv.DictReader(csvfile)
    for row in rea:
        SCHOOL_DICT[row['School Name']].append(row['URL'])

all_confessions = defaultdict(list)

# Open Chrome window
driver = Chrome()

# Loop for eaech school
for school in tqdm(SCHOOL_DICT):
    # Get school URL
    school_urls = SCHOOL_DICT[school]

    for school_url in school_urls:
        school_url = school_url.replace('www', 'mobile')
        driver.get(school_url)

        time.sleep(1)

        # Load more posts
        heights = deque(maxlen=10)
        heights.append(driver.execute_script("return document.body.scrollHeight"))

        for i in range(NUM_SCROLLS):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_DELAY)

            heights.append(driver.execute_script("return document.body.scrollHeight"))

            if len(heights) == 10 and all(i == heights[0] for i in heights):
                break

        # Close popup to clear viewport
        popup_close = driver.find_element_by_id("popup_xout")
        try:
            popup_close.click()
        except:
            print("No popup exists")

        # Expand all posts
        more_buttons = driver.find_elements_by_partial_link_text("More")
        for button in more_buttons:
            try:
                button.click()
            except:
                print("Tried to click something rip")

        # Get posts
        posts = driver.find_elements_by_class_name("story_body_container")
        post_texts = ["\n".join(thing.text for thing in post.find_elements_by_tag_name('p')) for post in posts]

        all_confessions[school].extend(post_texts)

# Save confessions
with open('school_confessions.pickle', 'wb') as f:
    pickle.dump(all_confessions, f)

driver.close()
