import cv2
import numpy as np
 
############################## Server Address ##############################
# server_address = ('169.254.194.104', 45713)
server_address = ('169.254.153.83', 45713)
#############################################################################
 
############################# Camera Parameter ##############################
mtx = np.array([[168.1683,   0.,         166.4460],
 [  0.,         167.7907, 115.1241],
 [  0.,           0.,           1.        ]])
dist = np.array([[-0.2870, 0.0631, 0 ,0, 0]])
#############################################################################
 
############################# Wheel Alignment ###############################
WHEELALIGN = 0
#############################################################################
 
ONLEFT = 0
ONSTRAIGHT = 1
ONRIGHT = 2
ONSCORNER = 3
 
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
 
def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)
 
def ROI(image):
 
    height, width = image.shape[:2]
 
    polygons = np.array([
        [(0, height), (width, height), (int(width), int((height/16)*9)), (0, int(height/16)*9)] #(0, height), (width, height), (int((width/7)*3.2), int((height/5)*3)), (int(width/3), int(height/5)*3)
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
        
    return masked_image
 
def draw_crossLines(image):
    height, width = image.shape[:2]
    # draw horizontal lines
 
    image = cv2.line(image, (0, int(height/16)*10), (width , int(height/16)*10), (180, 180, 180), 1) # 150
    image = cv2.line(image, (0, int(height/16)*11), (width , int(height/16)*11), (180, 180, 180), 1) # 165
    image = cv2.line(image, (0, int(height/16)*12), (width , int(height/16)*12), (180, 180, 180), 1) # 180
    image = cv2.line(image, (0, int(height/16)*13), (width , int(height/16)*13), (180, 180, 180), 1) # 195
    image = cv2.line(image, (0, int(height/16)*14), (width , int(height/16)*14), (180, 180, 180), 1) # 210
    image = cv2.line(image, (0, int(height/16)*15), (width , int(height/16)*15), (180, 180, 180), 1) # 225
    image = cv2.putText(image, '150', (0,150), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '165', (0,165), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '180', (0,180), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '195', (0,195), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '210', (0,210), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '225', (0,225), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
 
    # draw vertical lines
    image = cv2.line(image, (int(width/8)*1, 0), (int(width/8)*1, int(height)), (180, 180, 180), 1) # 40
    image = cv2.line(image, (int(width/8)*2, 0), (int(width/8)*2, int(height)), (180, 180, 180), 1) # 80
    image = cv2.line(image, (int(width/8)*3, 0), (int(width/8)*3, int(height)), (180, 180, 180), 1) # 120
    image = cv2.line(image, (int(width/8)*4, 0), (int(width/8)*4, int(height)), (180, 180, 180), 1) # 160
    image = cv2.line(image, (int(width/8)*5, 0), (int(width/8)*5, int(height)), (180, 180, 180), 1) # 200
    image = cv2.line(image, (int(width/8)*6, 0), (int(width/8)*6, int(height)), (180, 180, 180), 1) # 240
    image = cv2.line(image, (int(width/8)*7, 0), (int(width/8)*7, int(height)), (180, 180, 180), 1) # 280
    image = cv2.putText(image, '40', (40,10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '80', (80,10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '120', (120,10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '160', (160,10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '200', (200,10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '240', (240,10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
    image = cv2.putText(image, '280', (280,10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 0))
 
    return image
 
def getVerticalDistance(image, v):
    
    height, width = image.shape[:2]
    VD = 0
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # find vertical distance from bottom
 
    for y in range(height-1, 0, -1):
        yx = image.item(y,v,2)  #[0,0,255]
        if yx >= 10:
            VD = y
            break
    return VD
        
def getHorizontalDistance(image, h):
 
    height, width = image.shape[:2]
    center = int(width/2)
    HLD = 0
    HRD = width
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 
    # find Horizontal Left Distance from center line
    for x in range(center, 0, -1):
        yx = image.item(h,x,2)
        if yx >= 10:
            HLD = x
            break
 
    # find Horizontal Right Distance from center line
    for x in range(center+1, width):
        yx = image.item(h,x,2)
        if yx >= 10:
            HRD = x
            break
 
    return HLD, HRD
 
def getContactPoints(image):
 
    height, width = image.shape[:2]
    # get vertical lengths
    V1D = getVerticalDistance(image, int(width/8)*1)
    V2D = getVerticalDistance(image, int(width/8)*2)
    V3D = getVerticalDistance(image, int(width/8)*3)
    V4D = getVerticalDistance(image, int(width/8)*4)
    V5D = getVerticalDistance(image, int(width/8)*5)
    V6D = getVerticalDistance(image, int(width/8)*6)
    V7D = getVerticalDistance(image, int(width/8)*7)
 
    # get horizontal lenghts
 
    H1LD, H1RD = getHorizontalDistance(image, int(height/16)*10) #
    H2LD, H2RD = getHorizontalDistance(image, int(height/16)*11) # 
    H3LD, H3RD = getHorizontalDistance(image, int(height/16)*12) #
    H4LD, H4RD = getHorizontalDistance(image, int(height/16)*13) # 
    H5LD, H5RD = getHorizontalDistance(image, int(height/16)*14) # 
    H6LD, H6RD = getHorizontalDistance(image, int(height/16)*15) # 
 
    return {'V1D':V1D, 'V2D':V2D, 'V3D':V3D, 'V4D':V4D, 'V5D':V5D, 'V6D':V6D, 'V7D':V7D, \
    'H1LD':H1LD, 'H1RD':H1RD, 'H2LD':H2LD, 'H2RD':H2RD, 'H3LD':H3LD, 'H3RD':H3RD, 'H4LD':H4LD, 'H4RD':H4RD, 'H5LD':H5LD, 'H5RD':H5RD, 'H6LD':H6LD, 'H6RD':H6RD}
 
def drawContactPoints(image, points):    
 
    height, width = image.shape[:2]
    # draw vertical points
 
    image = cv2.circle(image, (points['H1LD'], int(height/16)*10), 3, (255, 0, 0), -1)
    image = cv2.circle(image, (points['H1RD']-1, int(height/16)*10), 3, (0, 0, 255), -1)
    image = cv2.circle(image, (points['H2LD'], int(height/16)*11), 3, (255, 0, 0), -1)
    image = cv2.circle(image, (points['H2RD']-1, int(height/16)*11), 3, (0, 0, 255), -1)
    image = cv2.circle(image, (points['H3LD'], int(height/16)*12), 3, (255, 0, 0), -1)
    image = cv2.circle(image, (points['H3RD']-1, int(height/16)*12), 3, (0, 0, 255), -1)
    image = cv2.circle(image, (points['H4LD'], int(height/16)*13), 3, (255, 0, 0), -1)
    image = cv2.circle(image, (points['H4RD']-1, int(height/16)*13), 3, (0, 0, 255), -1)
    image = cv2.circle(image, (points['H5LD'], int(height/16)*14), 3, (255, 0, 0), -1)
    image = cv2.circle(image, (points['H5RD']-1, int(height/16)*14), 3, (0, 0, 255), -1)
    image = cv2.circle(image, (points['H6LD'], int(height/16)*15), 3, (255, 0, 0), -1)
    image = cv2.circle(image, (points['H6RD']-1, int(height/16)*15), 3, (0, 0, 255), -1)
    image = cv2.putText(image, '%d' % points['H1LD'], (points['H1LD'], 150), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (255, 255, 0))
    image = cv2.putText(image, '%d' % points['H2LD'], (points['H2LD'], 165), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (255, 255, 0))
    image = cv2.putText(image, '%d' % points['H3LD'], (points['H3LD'], 180), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (255, 255, 0))
    image = cv2.putText(image, '%d' % points['H4LD'], (points['H4LD'], 195), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (255, 255, 0))
    image = cv2.putText(image, '%d' % points['H5LD'], (points['H5LD'], 210), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (255, 255, 0))
    image = cv2.putText(image, '%d' % points['H6LD'], (points['H6LD'], 225), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (255, 255, 0))
    image = cv2.putText(image, '%d' % points['H1RD'], (points['H1RD'], 150), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 0, 255))
    image = cv2.putText(image, '%d' % points['H2RD'], (points['H2RD'], 165), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 0, 255))
    image = cv2.putText(image, '%d' % points['H3RD'], (points['H3RD'], 180), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 0, 255))
    image = cv2.putText(image, '%d' % points['H4RD'], (points['H4RD'], 195), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 0, 255))
    image = cv2.putText(image, '%d' % points['H5RD'], (points['H5RD'], 210), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 0, 255))
    image = cv2.putText(image, '%d' % points['H6RD'], (points['H6RD'], 225), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 0, 255))
 
    # draw horizontal points
    image = cv2.circle(image, (int(width/8)*1, points['V1D']), 3, (0, 255, 255), -1)
    image = cv2.circle(image, (int(width/8)*2, points['V2D']), 3, (0, 255, 255), -1)
    image = cv2.circle(image, (int(width/8)*3, points['V3D']), 3, (0, 255, 255), -1)
    image = cv2.circle(image, (int(width/8)*4, points['V4D']), 3, (0, 255, 255), -1)
    image = cv2.circle(image, (int(width/8)*5, points['V5D']), 3, (0, 255, 255), -1)
    image = cv2.circle(image, (int(width/8)*6, points['V6D']), 3, (0, 255, 255), -1)
    image = cv2.circle(image, (int(width/8)*7, points['V7D']), 3, (0, 255, 255), -1)
    image = cv2.putText(image, '%d' % points['V1D'], (40, points['V1D'] - 10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 255))
    image = cv2.putText(image, '%d' % points['V2D'], (80, points['V2D'] - 10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 255))
    image = cv2.putText(image, '%d' % points['V3D'], (120, points['V3D'] - 10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 255))
    image = cv2.putText(image, '%d' % points['V4D'], (160, points['V4D'] - 10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 255))
    image = cv2.putText(image, '%d' % points['V5D'], (200, points['V5D'] - 10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 255))
    image = cv2.putText(image, '%d' % points['V6D'], (240, points['V6D'] - 10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 255))
    image = cv2.putText(image, '%d' % points['V7D'], (280, points['V7D'] - 10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, .3, (0, 255, 255))
 
    return image
 
# functions for the algorithm
def getLean(line):
    if line[0]-line[2] == 0:
        return 10000
    return (line[1]-line[3])/(line[0]-line[2])
 
def getIntercept(line):
    x = line[0]
    y = line[1]
    a = getLean(line)
    b = y-(a*x)
    return (120-b)/a
 
def draw_lines(img, lines, color=[0, 0, 255], thickness=2):
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
 
def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap): 
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
 
    return line_img, lines
    
def weighted_img(img, initial_img, alpha=1, beta=1., gamma=0.):
    return cv2.addWeighted(initial_img, alpha, img, beta, gamma)
 
def getAlignedWheelAngle(command, alignAlgle):
    steeringAngle = int(command[2:5]) + alignAlgle
    return command[:2] + str(steeringAngle) + 'E'
 
def getLane(lines):
    leftLanes = []
    rightLanes = []
    endLanes = []
    rightLane = []
    leftLane = []
    
    for line in lines.tolist():
        line = line[0]
        a = getLean(line)
        if a == 10000:
            pass
        elif a < -0.2 and line[2] < 200: # left lane
            leftLanes.append(line)
        elif a < 0.2: # end lane
            endLanes.append(line)
        elif line[0] > 120:
            rightLanes.append(line)
 
    for right in rightLanes:
        if len(rightLane) == 0:
            rightLane = right
        if getIntercept(right) < getIntercept(rightLane):
            rightLane = right
    for left in leftLanes:
        if len(leftLane) == 0:
            leftLane = left
        if getIntercept(left) > getIntercept(leftLane):
            leftLane = left
        
    return leftLane, rightLane, endLanes
 
def getMidPositionOfX(lines, width):
    sum = 0
    for line in lines:
        sum += (line[0] + line[2])/2
    sum /= len(lines)
    if sum < width/2:
        return False # means left
    else: return True # means right
 
def getCenterPoint(leftLane, rightLane):
    left_a = getLean(leftLane)
    left_b = leftLane[3] - left_a*leftLane[2]
    right_a = getLean(rightLane)
    right_b = rightLane[1] - right_a*rightLane[0]
 
    left_x = (30-left_b)/left_a
    right_x = (30-right_b)/right_a
 
    return left_x, right_x
 
 
 
 

