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


    cv.imshow("tree", img)

    cv.waitKey(0)
    cv.destroyAllWindows()
