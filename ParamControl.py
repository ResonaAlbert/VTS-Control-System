import random
import numpy as np
import FitCurve as FC

# main control data initial
def param_initia():
    parameter = {
        "parameterValues": [
            #{"id": "FaceAngleY", "weight": 1, "value": value*30}
        ]
    }
    data = {
        "faceFound": False,
        "mode": "set",
        "parameterValues": parameter["parameterValues"],
    }
    return data

# Eye Open Part
def EyeOpen_Blick(data, t0 = 0, T = 0.3, y0 = 0, y1 = 1, t = 0, N = 3):
    # awake
    if t < T:
        value = FC.cos_fun01(T0 = t0, T = T, N = N, t = t)
    else:
        value = 1
    data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
    data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value
    
def EyeOpen_NormalMode(data, t0 = 0, T = 1, y0 = 0, y1 = 1, t = 0, N = 2):
    # normal
    if t < T:
        value = FC.cos_fit_full(t0 = t0, T = T, y0 = y0, y1 = y1, t = t, N = N)
    else:
        value = y1
    data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
    data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value    

def EyeOpen_SleepMode(data, t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0, N = 2):
    # Sleep
    if t < T:
        value = FC.cos_fit_full(t0 = t0, T = T, y0 = y0, y1 = y1, t = t, N = N)
    else:
        value = y1
    data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
    data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value   
        
def EyeOpen_ShyMode(data, t0 = 0, T = 0.3, y0 = 0, y1 = 1, t = 0, N = 3):
    # Shy
    if t < T:
        value = FC.cos_fun01(T0 = t0, T = T, N = N, t = t)
    else:
        value = 1
    data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
    data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value

# Eye Ball Part
def EyeBallMotion(param, data, T, y1, y0, t):
    if t < T:
        value = FC.cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value

def EyeBallMotion_ShyMode(param, data, T, y1, y0, t):
    T1 = T*2/3
    T2 = T/3
    if t < T1:
        value = 0
    else:
        if t < T1 + T2:
            value = FC.cos_fit_full(T = T2, y0 = y0, y1 = y1, t = t, N = 2)
        else:
            value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value

# Ball Part
def Body_AwakeMode(param, data, T, y1, y0, t):
    # awake
    if param == "FaceAngleX":
        T = 0.5
        if t < T:
            value = (FC.cos_fun01(T0 = 0, T = T, N = 3, t = t) - 0.5)*20
        else:
            value = 1
    else:
        if t < T:
            value = FC.cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
        else:
            value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 

def Body_NormalMode(param, data, T, y1, y0, t):
    if t < T:
        value = FC.cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 

def Body_ShyMode(param, data, T, y1, y0, t):
    if t < T:
        value = FC.order3curve(T = T, y0 = y0, y1 = y1, t = t)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 

#Mouth
def MouthOpen_ShyMode(param, data, T, y1, y0, t):
    if t < T:
        value = FC.order3curve(T = T, y0 = y0, y1 = y1, t = t)
    elif t < T*2:
            value = y1
    else:
        value = -99
    if value != -99:
        data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 

# consider value
def consider_body_motion(dis = 0, y1 = 0, mean = 30, bis = 10, direction = 1, max = 30, min = 0):
    y1_new = np.random.normal(direction*mean, bis) #random.randint(0, 30)
    return y1_new

def consider_EyeOpen_motion(mean = 0.75, bis = 1):
    EyeOpen1 = np.random.normal(mean, bis)
    return EyeOpen1

def SetParam_Normal_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.15)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.15)
    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_body_motion(dis = 0, y1 = param_list[0][2], mean = 15, bis = 5, direction=random.choice([-1, 1]))
    param_list[1][1] = consider_body_motion(dis = 0, y1 = param_list[1][2], mean = 15, bis = 5, direction=random.choice([-1, 1]))
    param_list[2][1] = consider_body_motion(dis = 0, y1 = param_list[2][2], mean = 15, bis = 5, direction=random.choice([-1, 1]))

    param_list[3][0] = param_list[0][0]/30
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)
    T = 1

    return param_list, T, blick_num

def Normal_Mode(param_list, T_body, blick_num, t):

    FaceAngleX0 = param_list[0][0]
    FaceAngleX1 = param_list[0][1]
    FaceAngleY0 = param_list[1][0]
    FaceAngleY1 = param_list[1][1]
    FaceAngleZ0 = param_list[2][0]
    FaceAngleZ1 = param_list[2][1]
    EyeX0 = param_list[3][0]
    EyeX1 = param_list[3][1]
    EyeY0 = param_list[4][0]
    EyeY1 = param_list[4][1]
    EyeOpen0 = param_list[5][0] 
    EyeOpen1 = param_list[5][1]   
    T_eye = 1
    # Get the value of "start_parameter"
    data = param_initia()
    #control param
    #body
    data, param_list[0][2] = Body_NormalMode("FaceAngleX", data, T_body, FaceAngleX1, FaceAngleX0, t)
    data, param_list[1][2] = Body_NormalMode("FaceAngleY", data, T_body, FaceAngleY1, FaceAngleY0, t)
    data, param_list[2][2] = Body_NormalMode("FaceAngleZ", data, T_body, FaceAngleZ1, FaceAngleZ0, t)
    #Eye ball
    data, param_list[3][2] = EyeBallMotion("EyeRightX", data, T_body, EyeX1, EyeX0, t)
    data, param_list[4][2] = EyeBallMotion("EyeRightY", data, T_body, EyeY1, EyeY0, t)     
    #Eye Open
    data, param_list[5][2] = EyeOpen_NormalMode(data, T = T_eye, y0 = EyeOpen0, y1 = EyeOpen1, t = t, N = blick_num)
    return param_list, data

def SetParam_Sleep_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0, bis = 0.15)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0, bis = 0.15)
    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_body_motion(dis = 0, y1 = param_list[0][2], mean = 0, bis = 3, direction=1*np.sign(param_list[0][0]))
    param_list[1][1] = consider_body_motion(dis = 0, y1 = param_list[1][2], mean = 0, bis = 3, direction=1*np.sign(param_list[1][0]))
    param_list[2][1] = consider_body_motion(dis = 0, y1 = param_list[2][2], mean = 20, bis = 5, direction=1*np.sign(param_list[2][0]))

    param_list[3][0] = param_list[0][0]/30
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)
    T = 1

    return param_list, T, blick_num   

def Sleep_Mode(param_list, T_body, blick_num, t):

    FaceAngleX0 = param_list[0][0]
    FaceAngleX1 = param_list[0][1]
    FaceAngleY0 = param_list[1][0]
    FaceAngleY1 = param_list[1][1]
    FaceAngleZ0 = param_list[2][0]
    FaceAngleZ1 = param_list[2][1]
    EyeX0 = param_list[3][0]
    EyeX1 = param_list[3][1]
    EyeY0 = param_list[4][0]
    EyeY1 = param_list[4][1]
    EyeOpen0 = param_list[5][0] 
    EyeOpen1 = param_list[5][1]                 
    T_eye = 1
    # Get the value of "start_parameter"
    data = param_initia()
    #control param
    #body
    data, param_list[0][2] = Body_NormalMode("FaceAngleX", data, T_body, FaceAngleX1, FaceAngleX0, t)
    data, param_list[1][2] = Body_NormalMode("FaceAngleY", data, T_body, FaceAngleY1, FaceAngleY0, t)
    data, param_list[2][2] = Body_NormalMode("FaceAngleZ", data, T_body, FaceAngleZ1, FaceAngleZ0, t)
    #Eye ball
    data, param_list[3][2] = EyeBallMotion("EyeRightX", data, T_body, EyeX1, EyeX0, t)
    data, param_list[4][2] = EyeBallMotion("EyeRightY", data, T_body, EyeY1, EyeY0, t)     
    #Eye Open
    data, param_list[5][2] = EyeOpen_SleepMode(data, t0 = 0, T = T_eye, y0 = EyeOpen0, y1 = EyeOpen1, t = t, N = blick_num)
    return param_list, data

def SetParam_Awake_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)

    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_body_motion(y1 = param_list[0][2], mean = 0, bis = 10)
    param_list[1][1] = consider_body_motion(y1 = param_list[1][2], mean = 0, bis = 10)
    param_list[2][1] = consider_body_motion(y1 = param_list[2][2], mean = 30, bis = 10)

    param_list[3][0] = param_list[0][0]/30
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)
    T = 1

    return param_list, T, blick_num   

def Awake_Mode(param_list, T_body, blick_num, t):

    FaceAngleX0 = param_list[0][0]
    FaceAngleX1 = param_list[0][1]
    FaceAngleY0 = param_list[1][0]
    FaceAngleY1 = param_list[1][1]
    FaceAngleZ0 = param_list[2][0]
    FaceAngleZ1 = param_list[2][1]
    EyeX0 = param_list[3][0]
    EyeX1 = param_list[3][1]
    EyeY0 = param_list[4][0]
    EyeY1 = param_list[4][1]
    EyeOpen0 = param_list[5][0] 
    EyeOpen1 = param_list[5][1]                    
    T_eye = 1
    # Get the value of "start_parameter"
    data = param_initia()
    #control param
    #body
    data, param_list[0][2] = Body_AwakeMode("FaceAngleX", data, T_body, FaceAngleX1, FaceAngleX0, t)
    data, param_list[1][2] = Body_AwakeMode("FaceAngleY", data, T_body, FaceAngleY1, FaceAngleY0, t)
    data, param_list[2][2] = Body_AwakeMode("FaceAngleZ", data, T_body, FaceAngleZ1, FaceAngleZ0, t)
    #Eye ball
    data, param_list[3][2] = EyeBallMotion("EyeRightX", data, T_body, EyeX1, EyeX0, t)
    data, param_list[4][2] = EyeBallMotion("EyeRightY", data, T_body, EyeY1, EyeY0, t)     
    #Eye Open
    data, param_list[5][2] = EyeOpen_Blick(data, t0 = 0, T = 0.3, y0 = 0, y1 = 1, t = t, N = 3)
    return param_list, data

def SetParam_Shy_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)

    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    direction  = random.choice([-1, 1])
    param_list[0][1] = consider_body_motion(y1 = param_list[0][2], mean = 25, bis = 5, direction = direction)
    param_list[1][1] = consider_body_motion(y1 = param_list[1][2], mean = 0, bis = 5, direction = random.choice([-1, 1]))
    param_list[2][1] = consider_body_motion(y1 = param_list[2][2], mean = -10, bis = 3, direction = direction)

    param_list[3][0] = -param_list[0][0]/20
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)
    T = 2

    return param_list, T, blick_num   

def Shy_Mode(param_list, T_body, blick_num, t):

    FaceAngleX0 = param_list[0][0]
    FaceAngleX1 = param_list[0][1]
    FaceAngleY0 = param_list[1][0]
    FaceAngleY1 = param_list[1][1]
    FaceAngleZ0 = param_list[2][0]
    FaceAngleZ1 = param_list[2][1]
    EyeX0 = param_list[3][0]
    EyeX1 = param_list[3][1]
    EyeY0 = param_list[4][0]
    EyeY1 = param_list[4][1]
    EyeOpen0 = param_list[5][0] 
    EyeOpen1 = param_list[5][1]       
    T_eye = 0.5
    # Get the value of "start_parameter"
    data = param_initia()
    #control param
    #body
    data, param_list[0][2] = Body_ShyMode("FaceAngleX", data, T_body, FaceAngleX1, FaceAngleX0, t)
    data, param_list[1][2] = Body_ShyMode("FaceAngleY", data, T_body, FaceAngleY1, FaceAngleY0, t)
    data, param_list[2][2] = Body_ShyMode("FaceAngleZ", data, T_body, FaceAngleZ1, FaceAngleZ0, t)
    #Eye ball
    data, param_list[3][2] = EyeBallMotion_ShyMode("EyeRightX", data, T_body, EyeX1, EyeX0, t)
    data, param_list[4][2] = EyeBallMotion_ShyMode("EyeRightY", data, T_body, EyeY1, EyeY0, t)     
    #Eye Open
    data, param_list[5][2] = EyeOpen_ShyMode(data, t0 = 0, T = T_eye, y0 = EyeOpen0, y1 = EyeOpen1, t = t, N = 4)
    #Mouth Open
    data, param_list[7][2] = MouthOpen_ShyMode("MouthOpen", data, 1, 0, 1, t)
    return param_list, data

def SetParam_hold_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)

    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_body_motion(y1 = param_list[0][2], mean = param_list[0][0], bis = 5)
    param_list[1][1] = consider_body_motion(y1 = param_list[1][2], mean = param_list[1][0], bis = 5)
    param_list[2][1] = consider_body_motion(y1 = param_list[2][2], mean = param_list[2][0], bis = 5)

    param_list[3][0] = 0
    param_list[3][1] = 0
    param_list[4][0] = 0
    param_list[4][1] = 0

    blick_num = random.randint(0, 2)
    T = 2

    return param_list, T, blick_num   

def hold_Mode(param_list, T_body, blick_num, t):

    FaceAngleX0 = param_list[0][0]
    FaceAngleX1 = param_list[0][1]
    FaceAngleY0 = param_list[1][0]
    FaceAngleY1 = param_list[1][1]
    FaceAngleZ0 = param_list[2][0]
    FaceAngleZ1 = param_list[2][1]
    EyeX0 = param_list[3][0]
    EyeX1 = param_list[3][1]
    EyeY0 = param_list[4][0]
    EyeY1 = param_list[4][1]
    EyeOpen0 = param_list[5][0] 
    EyeOpen1 = param_list[5][1]       
    T_eye = 1
    # Get the value of "start_parameter"
    data = param_initia()
    #control param
    #body
    data, param_list[0][2] = Body_NormalMode("FaceAngleX", data, T_body, FaceAngleX1, FaceAngleX0, t)
    data, param_list[1][2] = Body_NormalMode("FaceAngleY", data, T_body, FaceAngleY1, FaceAngleY0, t)
    data, param_list[2][2] = Body_NormalMode("FaceAngleZ", data, T_body, FaceAngleZ1, FaceAngleZ0, t)
    #Eye ball
    data, param_list[3][2] = EyeBallMotion("EyeRightX", data, T_body, EyeX1, EyeX0, t)
    data, param_list[4][2] = EyeBallMotion("EyeRightY", data, T_body, EyeY1, EyeY0, t)     
    #Eye Open
    data, param_list[5][2] = EyeOpen_NormalMode(data, T = T_eye, y0 = EyeOpen0, y1 = EyeOpen1, t = t, N = blick_num)
    return param_list, data
