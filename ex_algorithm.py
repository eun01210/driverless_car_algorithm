from jajuchaUtil import *
#2018년 12월 21일 

def stop(image):
    height, width = image.shape[:2]
    status = "None"
    count = 0
    count2 = 0
    for y in range(100, 150):
        for x in range(120, 300):
            B = image.item(y,x,0)
            G = image.item(y,x,1)
            R = image.item(y,x,2)
            if 90 <= R <= 180 and R-G >= 30 and R-B >= 30: count += 1
            elif R >= 100 and B >= 100 and G >= 100: count2 += 1
            if 60 >= count >= 40 and count2 >= 1500:
                status = "stop"
                break
        if status == "stop":
            break
    print(count, count2)
    count = 0
    count2 = 0
    if status != "stop":
        for y in range(25, 55):
            for x in range(120, 200):
                B = image.item(y,x,0)
                G = image.item(y,x,1)
                R = image.item(y,x,2)
                if 80 <= R <= 180 and R-G >= 30 and R-B >= 30: count += 1
                elif R <= 100 and G <= 100 and B <= 100: count2 += 1
                if count >= 8 and count2 >= 250:
                    status = "stop"
                    count = 0
                    break
            if status == "stop":
                break
    print(count, count2)
    return status
 
def autoDrive_algorithm(original_img, canny_img, points, LiDAR, prevComm, status, light):
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
    H6LD = points['H6LD']
    H6RD = points['H6RD']
 
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
    la[5] = H6LD
    ra[0] = H1RD
    ra[1] = H2RD
    ra[2] = H3RD
    ra[3] = H4RD
    ra[4] = H5RD
    ra[5] = H6RD
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
 
    if stop(original_img) == "stop":
        command = "S0150E"
 
    elif V3D > 195 or V4D > 185 or V5D > 195:
        if prevComm == 'S1110E' or prevComm == 'S1190E' or prevComm == 'S1130E' or prevComm == 'S1170E':
            if prevComm == 'S1110E' or prevComm == 'S1130E':
                if V3D > 175: command = 'S1110E'
                else: command = 'S1130E'
            else: 
                if V5D > 175: command = 'S1190E'
                else: command = 'S1170E'
        else:
            temp = 0
            for i in ea:
                if i == 0: temp += 1
            if temp <= 3:
                temp = 0
                for i in la:
                    if i == 0: temp += 1
                if temp >= 4: command = 'S1110E'
                else:
                    temp = 0
                    for i in ra:
                        if i == 320: temp += 1
                    if temp >= 4: command = 'S1190E'
            else:
                if abs((160-H3LD)-(H3RD-160)) > 10:
                    if (160-H3LD)-(H3RD-160) > 0: command = 'S1140E'
                    else: command = 'S1160E'
                else:
                    command = 'S1150E'
    else: 
        if temp < 175:
            if abs((160-H3LD)-(H3RD-160)) > 10:
                if (160-H3LD)-(H3RD-160) > 0: command = 'S1140E'
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
 
