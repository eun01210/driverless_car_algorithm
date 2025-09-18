from jajuchaUtil import *
#2018년 12월 21일 
################################ set cascade ################################
trafficlight_cascade = cv2.CascadeClassifier('haar.xml')
#############################################################################
 
 
def autoDrive_algorithm(original_img, canny_img, points, LIDAR, prevComm, status, light):
    height, width = canny_img.shape[:2]
    debug = True
    # debug = False
    command = prevComm
 
    H1LD = points['H1LD']
    H1RD = points['H1RD']
    H2LD = points['H2LD']
    H2RD = points['H2RD']
    H3LD = points['H3LD']
    H3RD = points['H3RD']
    H4LD = points['H4LD']
    H4RD = points['H4RD']
    H5LD = points['H5LD']
    H5RD = points['H5RD']
 
    V1D = points['V1D']
    V2D = points['V2D']
    V3D = points['V3D']
    V4D = points['V4D']
    V5D = points['V5D']
    V6D = points['V6D']
    V7D = points['V7D']

    la = [0, 0, 0, 0, 0, 0]
    ra = [0, 0, 0, 0, 0, 0]
    ea = [0, 0, 0, 0, 0, 0, 0]
    la[0] = H1LD
    la[1] = H2LD
    la[2] = H3LD
    la[3] = H4LD
    la[4] = H5LD
    ra[0] = H1RD
    ra[1] = H2RD
    ra[2] = H3RD
    ra[3] = H4RD
    ra[4] = H5RD
    ea[0] = V1D
    ea[1] = V2D
    ea[2] = V3D
    ea[3] = V4D
    ea[4] = V5D
    ea[5] = V6D
    ea[6] = V7D
    
    temp = 300

    for i in ea: 
        if i < temp: temp = i

    if V3D > 177 or V4D > 167 or V5D > 177:
        if prevComm == 'S1110E' or prevComm == 'S1190E' or prevComm == 'S1130E' or prevComm == 'S1170E':
            if prevComm == 'S1110E' or prevComm == 'S1130E':
                if V3D > 155: command = 'S1110E'
                else: command = 'S1130E'
            else: 
                if V5D > 155: command = 'S1190E'
                else: command = 'S1170E'
        else:
            temp = 0
            for i in ea:
                if i == 0: temp += 1
            if temp <= 3:
                temp = 0
                for i in la:
                    if i == 0: temp += 1
                if temp >= 3: command = 'S1110E'
                else:
                    temp = 0
                    for i in ra:
                        if i == 320: temp += 1
                    if temp >= 3: command = 'S1190E'
            else:
                if abs((160-H1LD)-(H1RD-160)) > 10:
                    if (160-H1LD)-(H1RD-160) > 0: command = 'S1140E'
                    else: command = 'S1160E'
                else:
                    command = 'S1150E'
    else: 
        if temp < 155:
            if abs((160-H1LD)-(H1RD-160)) > 10:
                if (160-H1LD)-(H1RD-160) > 0: command = 'S1140E'
                else: command = 'S1160E'
            else:
                command = 'S1150E'
        else:
            temp1 = 0
            for i in ra:
                if i == 320: temp1 += 1
            temp2 = 0
            for i in la:
                if i == 0: temp2 += 1
            if temp1 > temp2: command = 'S1190E'
            elif temp1 < temp2: command = 'S1110E'

    return command, status, light
