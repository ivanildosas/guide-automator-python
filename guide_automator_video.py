from pymouse import PyMouse
from pykeyboard import PyKeyboard
import pyttsx3
from selenium import webdriver
from IPython.display import display
from selenium.webdriver.support.wait import WebDriverWait
import requests
import time
import pygame
import io

wd = webdriver.Chrome()
wd.maximize_window()
mouse = PyMouse()
keyboard = PyKeyboard()
engine = pyttsx3.init()
keyboardSound = 'keyboard_sound.mp3'


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
    element = wd.find_element_by_css_selector(selector);
    words = list(string)
    playKeyboardSound()
    for word in words:
        element.send_keys(word)
        time.sleep(0.1)
    pygame.mixer.stop()
    print('aa')
# Play keyboard sound
def playKeyboardSound():
    # Avoid sound lag
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.mixer.music.load(keyboardSound)
    pygame.mixer.music.play()

# Stop keyboard sound
def stopKeyboardSound():
    pygame.mixer.stop()
