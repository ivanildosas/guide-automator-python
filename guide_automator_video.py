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
def clickOnElement(x, y):
    mouse.move(x, y)
    mouse.click(x, y, 1)

# Speak some text
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
# Get method. Access websites using the url by parameter
def get(url):
    wd.get(url);

