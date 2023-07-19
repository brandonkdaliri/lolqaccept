from util import *
from os import path
import time


APPLICATION = "League of Legends"

baseline = open_image(path.join("images", "matchfound.png"))
print("Begin polling...")
while True:
    sc = get_screenshot(APPLICATION)
    ssim = similarity(baseline, sc)
    print(ssim)

    if ssim >= 0.70:
        print("Queue pop detected, clicking")
        click_app(APPLICATION, 800, 700)
        break

    time.sleep(1)

print("Done")
