from selenium import webdriver
from IPython.display import display
from selenium.webdriver.support.wait import WebDriverWait
import requests
import time
import io
from PIL import Image

wd = webdriver.Chrome()


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
    display(Image.open(io.BytesIO(wd.get_screenshot_as_png())))

## Take Screenshot of a specified element of the page and display it
def takeScreenshotOf(selector):

    element = wd.find_element_by_css_selector(selector)
    ratio = wd.execute_script("return window.devicePixelRatio;")
    bounds = wd.execute_script("return arguments[0].getBoundingClientRect();", element)
    img = wd.get_screenshot_as_png()
    pilimg = Image.open(io.BytesIO(img))
    region = pilimg.crop((bounds['left'] * ratio, bounds['top'] * ratio, bounds['right'] * ratio, bounds['bottom'] * ratio,))
    display(region)

# TODO Highlight
#def highlight(element):
