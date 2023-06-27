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
    skyColor = (255, 255, 85)  # BGR, not RGB
    skyLineThickness = -1  # fill without a border
    cv.rectangle(img, (x1, y1), (x2, y2), skyColor, skyLineThickness)

    # ground
    x1, y1 = 0, height - groundHeight
    x2, y2 = width, height
    groundColor = (75, 180, 70)
    groundThickness = -1
    cv.rectangle(img, (x1, y1), (x2, y2), groundColor, groundThickness)

    # sun
    xCenter = int(width / 8)  # indent from left side via a proportion instead of a fixed amount
    yCenter = int((height - groundHeight) / 4)  # indent from the top by a proportion instead of a fixed amount
    # radius of sun is a percentage of the height (because height is usually smaller than width on my laptop computer
    sunRadius = int(height * 0.08 * 10 / 10)
    sunColor = (0, 255, 255)  # BGR not RGB
    sunThickness = -1
    cv.circle(img, (xCenter, yCenter), sunRadius, sunColor, sunThickness)
    # sun halo
    sunHaloRadius = int(sunRadius * 1.10)  # increase radius by 10 percent
    sunHaloColor = (220, 255, 255)
    sunHaloThickness = 10
    cv.circle(img, (xCenter, yCenter), sunHaloRadius, sunHaloColor, sunHaloThickness)

    # tree trunk
    trunkX1, trunkY1 = int(width * 2 / 3), height - groundHeight  # (600, 500) in video
    trunkX2 = trunkX1
    trunkHeight = int(height * 0.30)
    trunkY2 = trunkY1 - trunkHeight
    trunkColor = (30, 65, 155)  # BGR not RGB
    # trunk line thickness is proportional to screen width
    trunkLineThickness = int(width * 0.03)
    cv.line(img, (trunkX1, trunkY1), (trunkX2, trunkY2), trunkColor, trunkLineThickness)
    # cv.line(img, (600, 500), (600, 420), (30,65,155), 25) # from video

    # leafs
    # triangle = np.array([ [500,440], [700,440], [600,75]  ]) # left base, right-base, top from video
    leafXleft = int(trunkX1 * 0.85)
    leafYbase = int(trunkY1 - (height * 0.10))
    baseLeft = [leafXleft, leafYbase]  # left base

    leafXright = int(trunkX1 * 1.15)
    baseRight = [leafXright, leafYbase]

    leafTopX = trunkX1
    leafTopY = int(trunkY2 * 0.30)
    leafTop = [leafTopX, leafTopY]

    triangle = np.array([[leafXleft, leafYbase], [leafXright, leafYbase], [leafTopX, leafTopY]], dtype=np.int32)
    cv.fillPoly(img, [triangle], groundColor)

    cv.imshow("tree", img)

    cv.waitKey(0)
    cv.destroyAllWindows()
