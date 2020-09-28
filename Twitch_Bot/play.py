import pynput.keyboard as kb
import pynput.mouse as ms
import pyautogui as pag
import pydirectinput as p
import time

keyboard = kb.Controller()
mouse = ms.Controller()


def chat():
    p.press("l")
    time.sleep(2)
    p.press("o")
    time.sleep(2)
    p.press("k")


def press_key(btn):

    p.press(btn)


def say_ingame(text):

    p.press("y")
    for x in text:
        p.press(x)
    p.press("enter")