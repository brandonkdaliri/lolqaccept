import win32gui
import win32ui
import mouse
from ctypes import windll
from PIL import Image
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim


def open_image(filename):
    if not filename:
        return

    return Image.open(filename)


def get_screenshot(app):
    hwnd = win32gui.FindWindow(None, app)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)
    windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    image = Image.frombuffer(
        "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1
    )
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return image


def crop(image):
    # Hardcoded coords for q accept
    return image.crop((468, 120, 1132, 795))


def similarity(a, b):
    if a.size == (1600, 900):
        a = crop(a)
    if b.size == (1600, 900):
        b = crop(b)

    a = cv2.cvtColor(np.array(a), cv2.COLOR_RGB2GRAY)
    b = cv2.cvtColor(np.array(b), cv2.COLOR_RGB2GRAY)

    score, _ = ssim(a, b, full=True)
    return score


def click_app(app, x, y):
    hwnd = win32gui.FindWindow(None, app)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

    cur_x, cur_y = mouse.get_position()
    abs_x, abs_y = left + x, top + y

    # Assume app in foreground
    mouse.move(abs_x, abs_y)
    mouse.click()
    mouse.move(cur_x, cur_y)
