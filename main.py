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
    # use a percentage of total image height for the ground height
    ground_level: int = int(height * 0.15 * 10 / 10)

    # background
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # sky
    x1, y1 = 0, 0
    x2, y2 = width, height - ground_level
    sky_color = (255, 255, 85)  # BGR, not RGB
    sky_line_thickness = -1  # fill without a border
    cv.rectangle(img, (x1, y1), (x2, y2), sky_color, sky_line_thickness)

    # ground
    x2, y2 = width, height - ground_level
    print(f'ground height={ground_level}, y2={y2}')
    x1, y1 = 0, height - ground_level
    x2, y2 = width, height
    groundColor = (75, 180, 70)
    groundThickness = -1
    cv.rectangle(img, (x1, y1), (x2, y2), groundColor, groundThickness)

    # sun
    xCenter = int(width / 8)  # indent from left side via a proportion instead of a fixed amount
    yCenter = int((height - ground_level) / 4)  # indent from the top by a proportion instead of a fixed amount
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
    trunk1_X1, trunk1_Y1 = int(width * 60 / 100), height - ground_level  # (600, 500) in video
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

    tree1_triangle = np.array([[leaves1_Xleft, leaves1_Ybase], [leaves1_Xright, leaves1_Ybase], [leaves1_TopX, leaves1_TopY]], dtype=np.int32)
    cv.fillPoly(img, [tree1_triangle], groundColor)

    # tree #2 over to the right, shorter and thinner than tree #1

    trunk2_X1 = int(width * 3 / 4)  # (600, 500) in video
    trunk2_Y1 = int(height - ground_level) # this should be on the ground instead of up in the air
    print(f'trunk1_Y1 = {trunk1_Y1}, trunk2_Y1 = {trunk2_Y1}')
    trunk2_X2 = trunk2_X1
    trunk2_height = int(height * 0.20)
    trunk2_Y2 = trunk2_Y1 - trunk2_height
    print(f'trunk1(x2, y2) = ({trunk1_X2},{trunk1_Y2}), trunk2(x2,y2) = ({trunk2_X2},{trunk2_Y2})')
    trunk2_color = (30, 65, 155)  # BGR not RGB
    # trunk line thickness is proportional to screen width
    trunk2_lineThickness = int(width * 0.015)
    cv.line(img, (trunk2_X1, trunk2_Y1), (trunk2_X2, trunk2_Y2), trunk2_color, trunk2_lineThickness)
    print(f'trunk1 thickness = {trunk1_lineThickness}, trunk2 thickness = {trunk2_lineThickness}')

    # tree #2 leaves

    leaves2_Xleft = int(trunk2_X1 * 0.90)
    leaves2_Ybase = int(trunk2_Y1 - (height * 0.15))
    leaves2_baseLeft = [leaves2_Xleft, leaves2_Ybase]  # left base

    leaves2_Xright = int(trunk2_X1 * 1.10)
    leaves2_baseRight = [leaves2_Xright, leaves1_Ybase]

    leaves2_TopX = trunk2_X1
    leaves2_TopY = int(trunk2_Y2 * 0.5) # TODO: make top of leaves shorter
    leaves2_Top = [leaves2_TopX, leaves2_TopY]
    print(f'leaves1_top(x,y)=({leaves1_TopX},{leaves1_TopY}), leaves2_top(x,y)=({leaves2_TopX},{leaves2_TopY})')

    leaves2_color = (75, 140, 70) # BGR not RGB

    tree2_triangle = np.array( [[leaves2_Xleft, leaves2_Ybase], [leaves2_Xright, leaves2_Ybase], [leaves2_TopX, leaves2_TopY]], dtype=np.int32)
    cv.fillPoly(img, [tree2_triangle], leaves2_color)

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

    cv.imwrite("tree.jpg", img)
    cv.imshow("tree", img)

    cv.waitKey(0)
    cv.destroyAllWindows()
