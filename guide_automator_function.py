from selenium import webdriver
from IPython.display import display
from selenium.webdriver.support.wait import WebDriverWait
import requests
import time
import io
from PIL import Image

wd = webdriver.Chrome()
listOfSelectors = []


# Get method. Access websites using the url by parameter
def get(url):
    wd.get(url);

# Fill in method. Insert text inside elements, using the element CSS selector
def fillIn(selector, text):
    elem = wd.find_element_by_css_selector(selector)
    elem.send_keys(text)

## Click on element of screen, using the element CSS selector
def click(selector):
    elem = wd.find_element_by_css_selector(selector)
    elem.click()

## Submit a element, using the element CSS selector
def submit(selector):
    elem = wd.find_element_by_css_selector(selector)
    elem.submit()

## Take screenshot of entire screen and display it
def takeScreenshot():
    sleep(3)
    display(Image.open(io.BytesIO(wd.get_screenshot_as_png())))
    removeAllHighlights()

## Take Screenshot of a specified element of the page and display it
def takeScreenshotOf(selector):

    element = wd.find_element_by_css_selector(selector)
    ratio = wd.execute_script("return window.devicePixelRatio;")
    bounds = wd.execute_script("return arguments[0].getBoundingClientRect();", element)
    img = wd.get_screenshot_as_png()
    pilimg = Image.open(io.BytesIO(img))
    region = pilimg.crop((bounds['left'] * ratio, bounds['top'] * ratio, bounds['right'] * ratio, bounds['bottom'] * ratio,))
    display(region)
    removeAllHighlights()


# Highlight a element with a red border, using the element CSS selector
def highlight(selector):
    element = wd.find_element_by_css_selector(selector)
    wd.execute_script('arguments[0].setAttribute("style", "outline: 3px solid red")', element)
    listOfSelectors.append(selector)

# Remove the highlight of a element, using the element CSS selector
def removeHighlight(selector):
    element = wd.find_element_by_css_selector(selector)
    wd.execute_script('arguments[0].setAttribute("style", "outline: 0px solid red")', element)

# Remove all the highlights
def removeAllHighlights():
    for selector in listOfSelectors:
        removeHighlight(selector)

def sleep(sleepTime):
    time.sleep(sleepTime);