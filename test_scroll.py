import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://en.wikipedia.org/wiki/History")
time.sleep(2)


previous_frame = 0
for frame in frames:
    if previous_frame < frame:
        driver.execute_script("window.scrollBy(0, 50, { behavior: 'smooth'});")
    previous_frame = frame
    time.sleep(.03)