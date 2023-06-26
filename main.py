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
    groundHeight: int = int(height * 0.10 * 10 / 10)
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

    cv.imshow("tree", img)

    cv.waitKey(0)
    cv.destroyAllWindows()
