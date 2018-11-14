from pymouse import PyMouse
from pykeyboard import PyKeyboard
from guide_automator_function import *
# Move mouse to element
def clickOnElement(x, y):
    mouse = PyMouse()
    mouse.move(x, y)
    mouse.click(x, y, 1)


