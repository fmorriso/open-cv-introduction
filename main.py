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
    trunk1_X1, trunk1_Y1 = int(width * 2 / 3), height - groundHeight  # (600, 500) in video
    trunk1_X2 = trunk1_X1
    trunk1_height = int(height * 0.30)
    trunk1_Y2 = trunk1_Y1 - trunk1_height
    trunk1_color = (30, 65, 155)  # BGR not RGB
    # trunk line thickness is proportional to screen width
    trunk1_lineThickness = int(width * 0.03)
    cv.line(img, (trunk1_X1, trunk1_Y1), (trunk1_X2, trunk1_Y2), trunk1_color, trunk1_lineThickness)
    # cv.line(img, (600, 500), (600, 420), (30,65,155), 25) # from video

    # leaves on the tree as a simple triangle
    # triangle = np.array([ [500,440], [700,440], [600,75]  ]) # left base, right-base, top from video
    leaves1_Xleft = int(trunk1_X1 * 0.85)
    leaves1_Ybase = int(trunk1_Y1 - (height * 0.10))
    leaves1_baseLeft = [leaves1_Xleft, leaves1_Ybase]  # left base

    leaves1_Xright = int(trunk1_X1 * 1.15)
    leaves1_baseRight = [leaves1_Xright, leaves1_Ybase]

    leaves1_TopX = trunk1_X1
    leaves1_TopY = int(trunk1_Y2 * 0.30)
    leaves1_Top = [leaves1_TopX, leaves1_TopY]

    triangle = np.array([[leaves1_Xleft, leaves1_Ybase], [leaves1_Xright, leaves1_Ybase], [leaves1_TopX, leaves1_TopY]], dtype=np.int32)
    cv.fillPoly(img, [triangle], groundColor)

    # tree #2 over to the right, shorter and thinner than tree #1

    # add caption text
    captionText = "I love Python"
    captionFont = cv.FONT_HERSHEY_SCRIPT_SIMPLEX
    captionX = int(width * 0.20)
    captionY = int(height * 0.84)
    # make font scale somewhat proportional with a little extra for good measure
    fontScale =  max(height, width) / min(height, width) * 1.5
    print(f'fontScale = {fontScale:.2f}')
    textColor = (255, 255, 255) # BGR not RGB
    textThickness = int(height * 0.0025)
    cv.putText(img, captionText, (captionX, captionY), captionFont, fontScale, textColor, textThickness)

    cv.imshow("tree", img)

    cv.waitKey(0)
    cv.destroyAllWindows()
