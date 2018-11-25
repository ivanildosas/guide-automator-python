import pyttsx3
from selenium import webdriver
from IPython.display import display
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
import pygame
import io

wd = webdriver.Chrome()
# wd.maximize_window()
try:
    engine = pyttsx3.init()
except:
    engine = None
    print("Could not load TTS engine")
keyboardSound = 'keyboard_sound.mp3'

def __element_exists_by_css_selector(selector):
    wd.implicitly_wait(0)
    elems = wd.find_elements_by_css_selector(selector)
    wd.implicitly_wait(3)
    return len(elems) > 0

def create_fake_mouse():
    if __element_exists_by_css_selector('#maccursor'):
        print("Fake cursor was already added")
        return

    myString = """
        var s=window.document.createElement('img');
        s.src = 'https://github.com/octalmage/mousecontrol/raw/gh-pages/mac-cursor.png';
        s.id = 'maccursor';
        s.style = `cursor: none;
        width: 20px;
        height: 25px;
        background-size: contain;
        background-image: url("mac-cursor.png");
        background-repeat: no-repeat;
        background-position: top left;
        position: absolute;
        top: 0;
        left: 0;
        z-index: 10000;`;
        window.document.body.appendChild(s);
        s.onload = arguments[0];
        """
    wd.execute_async_script(myString)

def __get_element_bounds(element):
    bounds = wd.execute_script("return arguments[0].getBoundingClientRect();", element)
    return {
        "x": bounds['left'],
        "y": bounds['top'],
        "width": bounds['width'],
        "height": bounds['height']
    }

def __get_element_center_position(element):
    bounds = __get_element_bounds(element)
    return {
        "x": bounds["x"] + bounds["width"] / 2,
        "y": bounds["y"] + bounds["height"] / 2
    }

def move_fake_mouse(selector, duration=700):
    create_fake_mouse()
    element = wd.find_element_by_css_selector(selector)
    bounds = __get_element_center_position(element)
    script = """
        function createTweenFunction(x1, y1, x2, y2, totalTime) {
          let x = x1, y = y1;
          let t0 = Date.now();

          return function () {
            let t = Date.now();
            let alpha = Math.min(1, (t - t0) / totalTime);
            x = x1 + (x2 - x1) * alpha;
            y = y1 + (y2 - y1) * alpha;
            return {x: x, y: y, done: alpha >= 1};
          };
        }

        function animate(elem, x2, y2, duration, callback) {
          const delay = 16;
          let bounds = elem.getBoundingClientRect();
          let x1 = bounds.left, y1 = bounds.top;
          let f = createTweenFunction(x1, y1, x2, y2, duration);
          let interval = setInterval(function () {
            let pos = f();
            $(elem).css('left', pos.x).css('top', pos.y);
            if (pos.done) {
              clearInterval(interval);
              if (callback != undefined) {
                callback();
              }
            }
          }, delay);
        }

        elem = document.getElementById('maccursor');
        // $(elem).css('left', 0).css('top', 0);
        let duration = %d;
        animate(elem, %d, %d, duration, arguments[0]);
    """ % (duration, bounds["x"], bounds["y"])
    wd.execute_async_script(script)


# Move mouse to element
def click(selector):
    move_fake_mouse(selector)
    elem = wd.find_element_by_css_selector(selector)

    touch = ActionChains(wd)
    touch.click_and_hold(elem)
    touch.perform()
    time.sleep(0.5)
    touch.click(elem)
    touch.perform()
    
# Speak some text
def speak(text):
    if engine is not None:
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
        time.sleep(0.05)
    pygame.mixer.stop()
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

def close():
    wd.quit()
