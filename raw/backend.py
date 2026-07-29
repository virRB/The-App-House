import win32gui
import win32process
import win32api
import os
import time
import pywintypes
import random
import json
import sys

if getattr(sys, "frozen", False):
    HERE = os.path.dirname(sys.executable)
else:
    HERE = os.path.dirname(os.path.abspath(__file__))

GARDEN = os.path.join(HERE, "__garden__")
SAVE = os.path.join(GARDEN, "save.json")

usage = {}
quotes = [
    "() is your most-used app right now.",
    "Looks like () is leading the pack.",
    "() is currently at the top of your activity list.",
    "You seem to have your eye on ().",
    "() is today's frontrunner.",
    "() is in first place so far."
]

def save():
    os.makedirs(GARDEN, exist_ok=True)
    with open(SAVE, "w") as f:
        json.dump(usage, f, indent=4)

def load():
    global usage
    if os.path.exists(SAVE):
        try:
            with open(SAVE, "r") as f:
                usage = json.load(f)
        except json.JSONDecodeError:
            usage = {}

load()

def makeQuote():
    quote = random.choice(quotes)
    return quote.replace("()", getHighest()["app"])


def getApp():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        handle = win32api.OpenProcess(0x0400 | 0x0010, False, pid)
        name = os.path.basename(win32process.GetModuleFileNameEx(handle, 0))
        handle.Close()
        return name

    except pywintypes.error:
        return None
    except Exception:
        return None


app = getApp()

def getHighest():
    highest = {
        "app": "",
        "ms": 0
    }
    for app, ms in usage.items():
        if ms > highest["ms"]:
            highest["app"] = app
            highest["ms"] = ms
    return highest


last = time.perf_counter()
lastApp = getApp()


def start():
    global lastApp, last
    while True:
        now = time.perf_counter()
        dt = (now - last) * 1000
        if lastApp is None:
            time.sleep(0.05)
            continue
        usage.setdefault(lastApp, 0.0)
        usage[lastApp] += dt
        last = now
        lastApp = getApp()
        time.sleep(0.05)