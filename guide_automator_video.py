from guide_automator_constants import rippleCss
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
# wd.maximize_window
wd.fullscreen_window()
try:
    engine = pyttsx3.init()
except:
    engine = None
    print("Could not load TTS engine")

last_mouse_pos = (0, 0, )
pygame.init()
keyboardSound = pygame.mixer.Sound('keyboard_sound.wav')
clickSound = pygame.mixer.Sound('click_sound.wav') # http://soundbible.com/893-Button-Click.html

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
        pointer-events: none;
        width: 20px;
        height: 25px;
        background-size: contain;
        background-image: url("mac-cursor.png");
        background-repeat: no-repeat;
        background-position: top left;
        position: absolute;
        top: {0}px;
        left: {1}px;
        z-index: 10000;`;
        window.document.body.appendChild(s);
        s.onload = arguments[0];
        """.format(last_mouse_pos[0], last_mouse_pos[1])
    print(last_mouse_pos)
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
            elem.style.left = pos.x + 'px';
            elem.style.top = pos.y + 'px';
            if (pos.done) {
              clearInterval(interval);
              if (callback != undefined) {
                callback();
              }
            }
          }, delay);
        }

        elem = document.getElementById('maccursor');
        let duration = %d;
        animate(elem, %d, %d, duration, arguments[0]);
    """ % (duration, bounds["x"], bounds["y"])
    wd.execute_async_script(script)

    global last_mouse_pos
    last_mouse_pos = (bounds["x"], bounds["y"], )

# Move mouse to element
def click(selector):
    move_fake_mouse(selector)
    element = wd.find_element_by_css_selector(selector)
    pos = __get_element_center_position(element)

    
    clickSound.play()
    touch = ActionChains(wd)
    touch.click_and_hold(element).perform()
    ripple(pos['x'], pos['y'])
    time.sleep(0.28)
    touch.release(element).perform()
    sleep(0.2)

# Based on https://hacks.mozilla.org/2012/04/click-highlights-with-css-transitions/
def ripple(x, y):
    if not __element_exists_by_css_selector('#lookatmeiamhere'):
        myString = """
            var s=window.document.createElement('style');
            s.type = 'text/css';
            s.innerHTML = `{0}`;
            window.document.head.appendChild(s);
            s.onload = arguments[0];
        """
        myString = myString.format(rippleCss)
        wd.execute_async_script(myString)

        script = """
            var plot = document.createElement('div'),
                pressed = false;
            plot.id = 'lookatmeiamhere';
            document.body.appendChild(plot);
            var offset = plot.offsetWidth / 2;
            return offset
        """
        wd.execute_script(script)

    script = """
      var plot = document.getElementById('lookatmeiamhere'),
        offset = plot.offsetWidth / 2;
      document.body.classList.add('down');
      plot.style.left = %d - offset + 'px';
      plot.style.top = %d - offset + 'px';
      console.log('left:', plot.style.left, 'top:', plot.style.top)

      setTimeout(function () {
          document.body.classList.remove('down');
      }, 300);
    """ % (x, y)
    wd.execute_script(script)
    
# Speak some text
def speak(text):
    if engine is not None:
        engine.say(text)
        engine.runAndWait()
    
# Get method. Access websites using the url by parameter
def get(url):
    wd.get(url);

# Simulates typing on an element defined by a selector
def fillIn(selector, string):
    element = wd.find_element_by_css_selector(selector);
    seconds_between_keystrokes = 0.05
    words = list(string)
    keyboardSound.play(loops = -1)
    for word in words:
        element.send_keys(word)
        time.sleep(0.05)
    keyboardSound.stop()

def close():
    wd.quit()

def sleep(sleepTime):
    time.sleep(sleepTime);
