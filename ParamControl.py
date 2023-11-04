import random
import numpy as np
import FitCurve as FC

plugin_info = {
    "plugin_name": "change_status hotkey",
    "developer": "OverHome",
    "authentication_token_path": "./pyvts_token.txt",
    "ip": "127.0.0.1",
}


# main control data initial
def data_head():
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
        value = -99
    if value  != -99:
        data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
        data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value
    
def EyeOpen_NormalMode(data, t0 = 0, T = 1, y0 = 0, y1 = 1, t = 0, N = 2):
    # normal
    if t < T:
        value = FC.cos_fit_full(t0 = t0, T = T, y0 = y0, y1 = y1, t = t, N = N)
    else:
        value = -99
    if value  != -99:
        data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
        data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value    

def EyeOpen_SleepMode(data, t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0, N = 2):
    # Sleep
    if t < T:
        value = FC.cos_fit_full(t0 = t0, T = T, y0 = y0, y1 = y1, t = t, N = N)
    else:
        value = y0
    if value  != -99:
        data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
        data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value   
        
def EyeOpen_ShyMode(data, t0 = 0, T = 0.3, y0 = 0, y1 = 1, t = 0, N = 3):
    # Shy
    if t < T:
        value = FC.cos_fun01(T0 = t0, T = T, N = N, t = t)
    else:
        value = -99
    if value  != -99:
        data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
        data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value

def EyeOpen_CheerupMode(data, t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0, N = 2):
    # Cheerup 4s
    T1 = 0.2
    T2 = 3
    T3 = 3.3
    if t < T1:
        value = FC.order3curve(t0 = 0, T = T1, y0 = 1, y1 = 0, t = t)
    elif t < T2:
        value = 0 
    elif t< T3:
        value = FC.cos_fun01(T0 = T2, T = T3 - T2, N = 2, t = t)
    else:
        value = -99

    if value  != -99:
        data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
        data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value   
        
# Eye Ball Part
def EyeBallMotion(param, data, T = 1, y1 = 0, y0 = 0, t = 0):
    if t < T:
        value = FC.cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value

def EyeBallMotion_ShyMode(param, data, T = 1, y1 = 0, y0 = 0, t = 0):
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
def Body_AwakeMode(param, data, T = 1, y1 = 0, y0 = 0, t = 0):
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

def Body_NormalMode(param, data, T = 1, y1 = 0, y0 = 0, t = 0):
    if t < T:
        value = FC.cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 

def Body_ShyMode(param, data, T = 1, y1 = 0, y0 = 0, t = 0):
    if t < T:
        value = FC.order3curve(T = T, y0 = y0, y1 = y1, t = t)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 

def Body_BeatsMode(param, data, T = 1, y1 = 0, y0 = 0, t = 0, N = 3):
    if t < T:
        value = FC.sin_fit_full(T = T, y0 = y0, y1 = y1, t = t, N = N)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 


#Mouth Open
def MouthOpen_ShyMode(param, data, T = 1, y1 = 0, y0 = 0, t = 0):
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
    EyeOpen1 = np.random.normal(mean, bis)
    return EyeOpen1

def MouthOpen_CheerupMode(param, data, T = 1, y1 = 0, y0 = 0, t = 0):
    # Cheerup 4s
    T1 = 2.8
    T2 = 3
    if t < T1:
        value = FC.order3curve(t0 = 0, T = T1, y0 = 0, y1 = 1, t = t)
    elif t < T2:
            value = FC.cos_fit_half(t0 = T1, T = T2 - T1, y0 = 1, y1 = 0, t = t)
    else:
        value = -99
    if value != -99:
        data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 

#consider value of param
def consider_value(dis = 0, y1 = 0, mean = 30, bis = 10, direction = 1, max = 30, min = 0):
    y1_new = np.random.normal(direction*mean, bis) #random.randint(0, 30)
    return y1_new

# control part
def SetParam_Normal_Mode(param_list):

    # consider param
    param_list[5][0] = consider_value(mean = 0.75, bis = 0.15)
    param_list[5][1] = consider_value(mean = 0.75, bis = 0.15)
    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_value(dis = 0, y1 = param_list[0][2], mean = 15, bis = 5, direction=random.choice([-1, 1]))
    param_list[1][1] = consider_value(dis = 0, y1 = param_list[1][2], mean = 15, bis = 5, direction=random.choice([-1, 1]))
    param_list[2][1] = consider_value(dis = 0, y1 = param_list[2][2], mean = 15, bis = 5, direction=random.choice([-1, 1]))

    param_list[3][0] = param_list[0][0]/30
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)

    #time list
    T_total = 0.6
    T_body = 0.6
    T_EyeOpen = 0.6
    T_EyeBall = 0.6
    T_MouthOpen = 0.6
    T_list = np.array([T_total, T_body, T_EyeOpen, T_EyeBall, T_MouthOpen])

    return param_list, T_list, blick_num

def Normal_Mode(param_list, T, blick_num, t):

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
    #time
    T_body = T[1]   
    T_EyeOpen = T[2]   
    T_EyeBall = T[3]   
    # Get the value of "start_parameter"
    data = data_head()
    #control param
    #body
    data, param_list[0][2] = Body_NormalMode("FaceAngleX", data, T = T_body, y1 = FaceAngleX1, y0 = FaceAngleX0, t = t)
    data, param_list[1][2] = Body_NormalMode("FaceAngleY", data, T = T_body, y1 = FaceAngleY1, y0 = FaceAngleY0, t = t)
    data, param_list[2][2] = Body_NormalMode("FaceAngleZ", data, T = T_body, y1 = FaceAngleZ1, y0 = FaceAngleZ0, t = t)
    #Eye ball
    data, param_list[3][2] = EyeBallMotion("EyeRightX", data, T = T_EyeBall, y1 = EyeX1, y0 = EyeX0, t = t)
    data, param_list[4][2] = EyeBallMotion("EyeRightY", data, T = T_EyeBall, y1 = EyeY1, y0 = EyeY0, t = t)     
    #Eye Open
    data, param_list[5][2] = EyeOpen_NormalMode(data, T = T_EyeOpen, y0 = EyeOpen0, y1 = EyeOpen1, t = t, N = blick_num)
    return param_list, data

def SetParam_Sleep_Mode(param_list):

    # consider param
    param_list[5][0] = consider_value(mean = 0, bis = 0.15)
    param_list[5][1] = consider_value(mean = 0, bis = 0.15)
    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_value(dis = 0, y1 = param_list[0][2], mean = 0, bis = 3, direction=1*np.sign(param_list[0][0]))
    param_list[1][1] = consider_value(dis = 0, y1 = param_list[1][2], mean = 0, bis = 3, direction=1*np.sign(param_list[1][0]))
    param_list[2][1] = consider_value(dis = 0, y1 = param_list[2][2], mean = 20, bis = 5, direction=1*np.sign(param_list[2][0]))

    param_list[3][0] = param_list[0][0]/30
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)

    #time list
    T_total = 1
    T_body = 1
    T_EyeOpen = 1
    T_EyeBall = 1
    T_MouthOpen = 1
    T_list = np.array([T_total, T_body, T_EyeOpen, T_EyeBall, T_MouthOpen])

    return param_list, T_list, blick_num

def Sleep_Mode(param_list, T, blick_num, t):

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
    T_body = T[1]      
    T_EyeOpen = T[2]   
    T_EyeBall = T[3]   
    # Get the value of "start_parameter"
    data = data_head()
    #control param
    #body
    data, param_list[0][2] = Body_NormalMode("FaceAngleX", data, T = T_body, y1 = FaceAngleX1, y0 = FaceAngleX0, t = t)
    data, param_list[1][2] = Body_NormalMode("FaceAngleY", data, T = T_body, y1 = FaceAngleY1, y0 = FaceAngleY0, t = t)
    data, param_list[2][2] = Body_NormalMode("FaceAngleZ", data, T = T_body, y1 = FaceAngleZ1, y0 = FaceAngleZ0, t = t)
    #Eye ball
    data, param_list[3][2] = EyeBallMotion("EyeRightX", data, T = T_EyeBall, y1 = EyeX1, y0 = EyeX0, t = t)
    data, param_list[4][2] = EyeBallMotion("EyeRightY", data, T = T_EyeBall, y1 = EyeY1, y0 = EyeY0, t = t)   
    #Eye Open
    data, param_list[5][2] = EyeOpen_SleepMode(data, t0 = 0, T = T_EyeOpen, y0 = EyeOpen0, y1 = EyeOpen1, t = t, N = blick_num)
    return param_list, data

def SetParam_Awake_Mode(param_list):

    # consider param
    param_list[5][0] = consider_value(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_value(mean = 0.75, bis = 0.3)

    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_value(y1 = param_list[0][2], mean = 0, bis = 10)
    param_list[1][1] = consider_value(y1 = param_list[1][2], mean = 0, bis = 10)
    param_list[2][1] = consider_value(y1 = param_list[2][2], mean = 30, bis = 10)

    param_list[3][0] = param_list[0][0]/30
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)

    #time list
    T_total = 1
    T_body = 1
    T_EyeOpen = 0.3
    T_EyeBall = 1
    T_MouthOpen = 1
    T_list = np.array([T_total, T_body, T_EyeOpen, T_EyeBall, T_MouthOpen])

    return param_list, T_list, blick_num

def Awake_Mode(param_list, T, blick_num, t):

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
    # Time                
    T_body = T[1]      
    T_EyeOpen = T[2]
    T_EyeBall = T[3]
    T_MouthOpen = T[4]
    # Get the value of "start_parameter"
    data = data_head()
    #control param
    #body
    data, param_list[0][2] = Body_AwakeMode("FaceAngleX", data, T = T_body, y1 = FaceAngleX1, y0 = FaceAngleX0, t = t)
    data, param_list[1][2] = Body_AwakeMode("FaceAngleY", data, T = T_body, y1 = FaceAngleY1, y0 = FaceAngleY0, t = t)
    data, param_list[2][2] = Body_AwakeMode("FaceAngleZ", data, T = T_body, y1 = FaceAngleZ1, y0 = FaceAngleZ0, t = t)
    #Eye ball
    data, param_list[3][2] = EyeBallMotion("EyeRightX", data, T = T_EyeBall, y1 = EyeX1, y0 = EyeX0, t = t)
    data, param_list[4][2] = EyeBallMotion("EyeRightY", data, T = T_EyeBall, y1 = EyeY1, y0 = EyeY0, t = t)
    #Eye Open
    data, param_list[5][2] = EyeOpen_Blick(data, t0 = 0, T = T_EyeOpen, y0 = 0, y1 = 1, t = t, N = 3)
    return param_list, data

def SetParam_Shy_Mode(param_list):

    # consider param
    param_list[5][0] = consider_value(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_value(mean = 0.75, bis = 0.3)

    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    direction  = random.choice([-1, 1])
    param_list[0][1] = consider_value(y1 = param_list[0][2], mean = 25, bis = 5, direction = direction)
    param_list[1][1] = consider_value(y1 = param_list[1][2], mean = 0, bis = 5, direction = random.choice([-1, 1]))
    param_list[2][1] = consider_value(y1 = param_list[2][2], mean = -10, bis = 3, direction = direction)

    param_list[3][0] = -param_list[0][0]/20
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)
    #time list
    T_total = 2
    T_body = 1
    T_EyeOpen = 0.5
    T_EyeBall = 1
    T_MouthOpen = 1
    T_list = np.array([T_total, T_body, T_EyeOpen, T_EyeBall, T_MouthOpen])

    return param_list, T_list, blick_num

def Shy_Mode(param_list, T, blick_num, t):

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
    # Time                
    T_body = T[1]      
    T_EyeOpen = T[2]   
    T_EyeBall = T[3]
    T_MouthOpen = T[4]
    # Get the value of "start_parameter"
    data = data_head()
    #control param
    #Body
    data, param_list[0][2] = Body_ShyMode("FaceAngleX", data, T = T_body, y1 = FaceAngleX1, y0 = FaceAngleX0, t = t)
    data, param_list[1][2] = Body_ShyMode("FaceAngleY", data, T = T_body, y1 = FaceAngleY1, y0 = FaceAngleY0, t = t)
    data, param_list[2][2] = Body_ShyMode("FaceAngleZ", data, T = T_body, y1 = FaceAngleZ1, y0 = FaceAngleZ0, t = t)
    #Eye Ball
    data, param_list[3][2] = EyeBallMotion_ShyMode("EyeRightX", data, T = T_EyeBall, y1 = EyeX1, y0 = EyeX0, t = t)
    data, param_list[4][2] = EyeBallMotion_ShyMode("EyeRightY", data, T = T_EyeBall, y1 = EyeY1, y0 = EyeY0, t = t)
    #Eye Open
    data, param_list[5][2] = EyeOpen_ShyMode(data, t0 = 0, T = T_EyeOpen, y0 = EyeOpen0, y1 = EyeOpen1, t = t, N = 4)
    #Mouth Open
    data, param_list[7][2] = MouthOpen_ShyMode("MouthOpen", data, T = T_MouthOpen, y0 = 0, y1 = 1, t = t)
    return param_list, data

def SetParam_Hold_Mode(param_list):

    # consider param
    param_list[5][0] = consider_value(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_value(mean = 0.75, bis = 0.3)

    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_value(y1 = param_list[0][2], mean = param_list[0][0], bis = 5)
    param_list[1][1] = consider_value(y1 = param_list[1][2], mean = param_list[1][0], bis = 5)
    param_list[2][1] = consider_value(y1 = param_list[2][2], mean = param_list[2][0], bis = 5)

    param_list[3][0] = 0
    param_list[3][1] = 0
    param_list[4][0] = 0
    param_list[4][1] = 0

    blick_num = random.randint(0, 2)
    #time list
    T_total = 2
    T_body = 2
    T_EyeOpen = 2
    T_EyeBall = 2
    T_MouthOpen = 2
    T_list = np.array([T_total, T_body, T_EyeOpen, T_EyeBall, T_MouthOpen])

    return param_list, T_list, blick_num

def Hold_Mode(param_list, T, blick_num, t):

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
    # Time                
    T_body = T[1]      
    T_EyeOpen = T[2]   
    T_EyeBall = T[3]   
    # Get the value of "start_parameter"
    data = data_head()
    #control param
    #body
    data, param_list[0][2] = Body_NormalMode("FaceAngleX", data, T = T_body, y1 = FaceAngleX1, y0 = FaceAngleX0, t = t)
    data, param_list[1][2] = Body_NormalMode("FaceAngleY", data, T = T_body, y1 = FaceAngleY1, y0 = FaceAngleY0, t = t)
    data, param_list[2][2] = Body_NormalMode("FaceAngleZ", data, T = T_body, y1 = FaceAngleZ1, y0 = FaceAngleZ0, t = t)
    #Eye ball
    data, param_list[3][2] = EyeBallMotion("EyeRightX", data, T = T_EyeBall, y1 = EyeX1, y0 = EyeX0, t = t)
    data, param_list[4][2] = EyeBallMotion("EyeRightY", data, T = T_EyeBall, y1 = EyeY1, y0 = EyeY0, t = t)
    #Eye Open
    data, param_list[5][2] = EyeOpen_NormalMode(data, T = T_EyeOpen, y0 = EyeOpen0, y1 = EyeOpen1, t = t, N = blick_num)
    return param_list, data

def SetParam_Cheerup_Mode(param_list):

    # consider param
    param_list[5][0] = consider_value(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_value(mean = 0.75, bis = 0.3)

    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    direction  = random.choice([-1, 1])
    param_list[0][1] = consider_value(y1 = param_list[0][2], mean = 5, bis = 5, direction = direction)
    param_list[1][1] = consider_value(y1 = param_list[1][2], mean = 15, bis = 5, direction = 1)
    param_list[2][1] = consider_value(y1 = param_list[2][2], mean = 15, bis = 3, direction = direction)

    param_list[3][0] = param_list[0][0]/20
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)
    #time list
    T_total = 4
    T_body = 2
    T_EyeOpen = 4
    T_EyeBall = 1
    T_MouthOpen = 4
    T_list = np.array([T_total, T_body, T_EyeOpen, T_EyeBall, T_MouthOpen])

    return param_list, T_list, blick_num

def Cheerup_Mode(param_list, T, blick_num, t):

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
    # Time                
    T_body = T[1]      
    T_EyeOpen = T[2]   
    T_EyeBall = T[3]
    T_MouthOpen = T[4]
    # Get the value of "start_parameter"
    data = data_head()
    #control param
    #Body
    data, param_list[0][2] = Body_NormalMode("FaceAngleX", data, T = T_body, y1 = FaceAngleX1, y0 = FaceAngleX0, t = t)
    data, param_list[1][2] = Body_NormalMode("FaceAngleY", data, T = T_body, y1 = FaceAngleY1, y0 = FaceAngleY0, t = t)
    data, param_list[2][2] = Body_NormalMode("FaceAngleZ", data, T = T_body, y1 = FaceAngleZ1, y0 = FaceAngleZ0, t = t)
    #Eye Ball
    data, param_list[3][2] = EyeBallMotion("EyeRightX", data, T = T_EyeBall, y1 = EyeX1, y0 = EyeX0, t = t)
    data, param_list[4][2] = EyeBallMotion("EyeRightY", data, T = T_EyeBall, y1 = EyeY1, y0 = EyeY0, t = t)
    #Eye Open
    data, param_list[5][2] = EyeOpen_CheerupMode(data, t0 = 0, T = T_EyeOpen, y0 = EyeOpen0, y1 = EyeOpen1, t = t, N = 4)
    #Mouth Open
    data, param_list[7][2] = MouthOpen_CheerupMode("MouthOpen", data, T = T_MouthOpen, y0 = 0, y1 = 1, t = t)
    return param_list, data


def SetParam_Beats_Mode(param_list):

    # consider param
    param_list[5][0] = consider_value(mean = 0.0, bis = 0.01)
    param_list[5][1] = consider_value(mean = 0.0, bis = 0.01)

    param_list[6][0] = param_list[5][0]
    param_list[6][1] = param_list[5][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    direction  = random.choice([-1, 1])
    param_list[0][1] = consider_value(y1 = param_list[0][2], mean = 10, bis = 5, direction = direction)
    param_list[1][1] = consider_value(y1 = param_list[1][2], mean = 15, bis = 5, direction = random.choice([-1, 1]))
    param_list[2][1] = consider_value(y1 = param_list[2][2], mean = 5, bis = 5, direction = direction)

    param_list[3][0] = param_list[0][0]/20
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)
    #time list
    T_total = 2
    T_body = T_total
    T_EyeOpen = T_total
    T_EyeBall = T_total
    T_MouthOpen = T_total
    T_list = np.array([T_total, T_body, T_EyeOpen, T_EyeBall, T_MouthOpen])

    return param_list, T_list, blick_num

def Beats_Mode(param_list, T, blick_num, t):

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
    # Time                
    T_body = T[1]      
    T_EyeOpen = T[2]   
    T_EyeBall = T[3]
    T_MouthOpen = T[4]
    # Get the value of "start_parameter"
    data = data_head()
    #control param
    #Body
    data, param_list[0][2] = Body_BeatsMode("FaceAngleX", data, T = T_body, y1 = FaceAngleX1, y0 = FaceAngleX0, t = t, N = 0.5)
    data, param_list[1][2] = Body_BeatsMode("FaceAngleY", data, T = T_body, y1 = FaceAngleY1, y0 = FaceAngleY0, t = t, N = 1)
    data, param_list[2][2] = Body_NormalMode("FaceAngleZ", data, T = T_body, y1 = FaceAngleZ1, y0 = FaceAngleZ0, t = t)
    #Eye Ball
    data, param_list[3][2] = EyeBallMotion("EyeRightX", data, T = T_EyeBall, y1 = EyeX1, y0 = EyeX0, t = t)
    data, param_list[4][2] = EyeBallMotion("EyeRightY", data, T = T_EyeBall, y1 = EyeY1, y0 = EyeY0, t = t)
    #Eye Open
    data, param_list[5][2] = EyeOpen_NormalMode(data, t0 = 0, T = T_EyeOpen, y0 = EyeOpen0, y1 = EyeOpen1, t = t, N = 4)
    return param_list, data
