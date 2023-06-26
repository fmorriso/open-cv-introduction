import sys
import pyautogui
#
import cv2 as cv
import numpy as np


@staticmethod
def get_python_version() -> str:
    return f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'

@staticmethod
def scaleBackground(screenPct: float) -> tuple[int, int]:
    # find out the width and height of the device we are running on
    device_width, device_height = pyautogui.size()

    # scale width and height based on what percentage of device size user wants to use, rounded to
    # the nearest multiple of 100
    scaledWidth: int = int((device_width * screenPct // 100) * 100)
    scaledHeight: int = int((device_height * screenPct // 100) * 100)

    return scaledWidth, scaledHeight


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f'Python version {get_python_version()}')

    # scale the size of the background based on device size
    width, height = scaleBackground(0.80)
    print(f'scaled: width={width}, height={height}')

    # background
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # sky
    x1, y1 = 0, 0
    # allow for future ground by reserving a percentage of the total height
    groundHeight: int = int(height * 0.15 * 10 / 10)
    x2, y2 = width, height - groundHeight
    print(f'ground height={groundHeight}, y2={y2}')
    skyColor = (255, 255, 85) # BGR, not RGB
    skyLineThickness = -1 # fill without a border
    cv.rectangle(img, (x1, y1), (x2, y2), skyColor, skyLineThickness)

    # ground
    x1, y1 = 0, height - groundHeight
    x2, y2 = width, height
    groundColor = (75, 180, 70)
    groundThickness = -1
    cv.rectangle(img, (x1, y1), (x2, y2), groundColor, groundThickness)

    # sun
    xCenter = int(width / 5) # indent from left side via a proportion instead of a fixed amount
    yCenter = int((height - groundHeight) / 3) # indent from the top by a proportion instead of a fixed amount
    # radius of sun is a percentage of the height (because height is usually smaller than width on my laptop computer
    sunRadius = int(height * 0.12 * 10 / 10)
    sunColor  = (0, 255, 255) # BGR not RGB
    sunThickness = -1
    cv.circle(img, (xCenter, yCenter), sunRadius, sunColor, sunThickness)

    cv.imshow("tree", img)

    cv.waitKey(0)
    cv.destroyAllWindows()
