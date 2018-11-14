from pymouse import PyMouse
from pykeyboard import PyKeyboard
import pyttsx


# Move mouse to element
def clickOnElement(x, y):
    mouse = PyMouse()
    mouse.move(x, y)
    mouse.click(x, y, 1)

# Speak some text
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    

