from pymouse import PyMouse
from pykeyboard import PyKeyboard
import pyttsx3
from selenium import webdriver
from IPython.display import display
from selenium.webdriver.support.wait import WebDriverWait
import requests
import time
import io

wd = webdriver.Chrome()
wd.maximize_window()
mouse = PyMouse()
keyboard = PyKeyboard()
engine = pyttsx3.init()


# Move mouse to element
def click(selector):
    elem = wd.find_element_by_css_selector(selector)
    mouse.move(elem.location['x'], elem.location['y'])
    mouse.click(elem.location['x'], elem.location['y'], 1)

# Speak some text
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
# Get method. Access websites using the url by parameter
def get(url):
    wd.get(url);

# Simulates slow typing on an element defined by a selector
def slowTip(selector, string):
    element = wd.find_element_by_css_selector(selector).click();
    words = list(string)
    for word in words:
        keyboard.tap_key(word)
        time.sleep(0.5) 


