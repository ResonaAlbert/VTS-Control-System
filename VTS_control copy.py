import asyncio, pyvts
import time
import threading
import math
import random
import numpy as np

hotkeyname_list = [ 'OO眼.exp3.json', 'Scene1.exp3.json', '压扁.exp3.json', '堵嘴.exp3.json', '屑.exp3.json', 
                    '恐怕.exp3.json', '星星眼.exp3.json', '汗.exp3.json', '爱心眼.exp3.json', '生气皱眉.exp3.json', 
                    '箭头眼.exp3.json', '累.exp3.json', '脸红.exp3.json', '脸青.exp3.json', '脸黑.exp3.json', 
                    '话筒.exp3.json', '鼓嘴.exp3.json', '@@眼.exp3.json', '上下摇摆10.motion3.json', '快速眨眼5.motion3.json', 
                    '惊讶55.motion3.json']
hotkey_list = ['83a2d987f7064642b7a9d3640274333b', '06826505889b40678302597311c79911', '12ca15e78fe7421483691b167fe7482d', 
               'b1cd02db9cfa4b04bddb1ee48c326dae', '47a8088c7b6a415b8158c2f42b0485e2', 'edb893b80c294871b6635ae0b42d44e6', 
               '0a7bf45151324c6d82ccdda5f34e4115', 'bee0edc6cf65491f9cc2e2bcd768ee2b', '7b849ad686b94e328a4c3748e19be7c6', 
               'bf102f7962dc47cd81de8c8366d39147', 'edfc753b78024779ad5bca0bf7f73f8e', 'e379e9d6b94d4ffe98d1e89dd7673843', 
               'a18ce5e4d0a144ac9b4a0805241048c8', '70f8c48382634faba50555b76940cd72', 'd2894537a77a43238df478324cd55a55', 
               'c292a2b25b424c48bf177e64db22cdc7', 'b6157183d1d94b1eaecfa8dd28522abe', '8ee59d635dd041ccb2335280cf7fff9d', 
               'e217ac7c24b540ebb72fdfe11d42479c', 'da76c120eb0745a9a2621a8c0ea4fde7', 'cf9269def5be447ea9b6c44a2ef34ef8']
plugin_info = {
    "plugin_name": "trigger hotkey",
    "developer": "OverHome",
    "authentication_token_path": "./pyvts_token.txt",
}

global blick
# 0 normal 1 sleep 2 awake 3 Shy 4 hold
global status
global trigger
global expression_trigger_singal



#fit curve function
def order3curve(t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0):
    t = t - t0
    y = y1 + (y1 - y0) * (t - T) ** 3 / T ** 3
    return y

def cos_fit_half(t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0):
    t = t - t0
    y = (y0 + y1)/2 + ((y0 - y1)/2) * math.cos( math.pi * (t - t0) / T )
    return y

def cos_fit_full(t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0, N = 1):
    t = t - t0
    y = (y0 + y1)/2 + ((y0 - y1)/2) * math.cos( 2 * N * math.pi * (t - t0) / T )
    return y

def cos_fun01(T0 = 0, T = 2, N = 5, t = 0):
    value = math.cos( 2 * N * math.pi * (t - T0) / T ) + 0.5
    return value

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

def EyeOpen_Blick(data, t0 = 0, T = 0.3, y0 = 0, y1 = 1, t = 0, N = 3):
    # awake
    if t < T:
        value = cos_fun01(T0 = t0, T = T, N = N, t = t)
    else:
        value = 1
    data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
    data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value
    
def EyeOpen_NormalMode(data, t0 = 0, T = 1, y0 = 0, y1 = 1, t = 0, N = 2):
    # normal
    if t < T:
        value = cos_fit_full(t0 = t0, T = T, y0 = y0, y1 = y1, t = t, N = N)
    else:
        value = y1
    data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
    data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value    
        
def EyeOpen_ShyMode(data, t0 = 0, T = 0.3, y0 = 0, y1 = 1, t = 0, N = 3):
    # awake
    if t < T:
        value = cos_fun01(T0 = t0, T = T, N = N, t = t)
    else:
        value = 1
    data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
    data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value


def Body_AwakeMode(param, data, T, y1, y0, t):
    # awake
    if param == "FaceAngleX":
        T = 0.5
        if t < T:
            value = (cos_fun01(T0 = 0, T = T, N = 3, t = t) - 0.5)*15
        else:
            value = 1
    else:
        if t < T:
            value = cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
        else:
            value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 

def Body_NormalMode(param, data, T, y1, y0, t):
    if t < T:
        value = cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 

def Body_ShyMode(param, data, T, y1, y0, t):
    if t < T:
        value = cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value 

def EyeBallMotion(param, data, T, y1, y0, t):
    if t < T:
        value = cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value

def EyeBallMotion_ShyMode(param, data, T, y1, y0, t):
    T1 = T/3
    T2 = T/6
    if t < T1:
        value = 0
    else:
        if t < T1 + T2:
            value = cos_fit_full(T = T2, y0 = y0, y1 = y1, t = t, N = 2)
        else:
            value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value

# consider value
def consider_body_motion(dis = 0, y1 = 0, mean = 30, bis = 10, direction = 1, max = 30, min = 0):
    y1_new = np.random.normal(direction*mean, bis) #random.randint(0, 30)
    return y1_new

def consider_EyeOpen_motion(mean = 0.75, bis = 1):
    global status
    if status == 1:
        EyeOpen1 = np.random.normal(0, 0.05)
    else:
        # nomral    
        EyeOpen1 = np.random.normal(mean, bis)
    return EyeOpen1

def SetParam_Normal_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][0] = param_list[6][0]
    param_list[5][1] = param_list[6][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_body_motion(dis = 0, y1 = param_list[0][2], mean = 10, bis = 5)
    param_list[1][1] = consider_body_motion(dis = 0, y1 = param_list[1][2], mean = 10, bis = 5)
    param_list[2][1] = consider_body_motion(dis = 0, y1 = param_list[2][2], mean = 15, bis = 5)

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
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][0] = param_list[6][0]
    param_list[5][1] = param_list[6][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_body_motion(dis = 0, y1 = param_list[0][2], mean = 0, bis = 3)
    param_list[1][1] = consider_body_motion(dis = 0, y1 = param_list[1][2], mean = 0, bis = 3)
    param_list[2][1] = consider_body_motion(dis = 0, y1 = param_list[2][2], mean = 15, bis = 5)

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
    data, param_list[5][2] = EyeOpen_NormalMode(data, T_eye, EyeOpen1, EyeOpen0, t, blick_num)
    return param_list, data

def SetParam_Awake_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)

    param_list[5][0] = param_list[6][0]
    param_list[5][1] = param_list[6][1]

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
    data, param_list[5][2] = EyeOpen_Blick(data, t0 = 0, T = 0.3, y0 = 0, y1 = 1, t = 0, N = 3)
    return param_list, data

def SetParam_Shy_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)

    param_list[5][0] = param_list[6][0]
    param_list[5][1] = param_list[6][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_body_motion(y1 = param_list[0][2], mean = 15, bis = 10)
    param_list[1][1] = consider_body_motion(y1 = param_list[1][2], mean = 0, bis = 10)
    param_list[2][1] = consider_body_motion(y1 = param_list[2][2], mean = 5, bis = 10)

    param_list[3][0] = param_list[0][0]/30
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)
    T = 5

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
    T_eye = 1
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
    data, param_list[5][2] = EyeOpen_ShyMode(data, t0 = 0, T = 0.3, y0 = 0, y1 = 1, t = 0, N = 3)
    return param_list, data

def SetParam_hold_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)

    param_list[5][0] = param_list[6][0]
    param_list[5][1] = param_list[6][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    param_list[0][1] = consider_body_motion(y1 = param_list[0][2], mean = param_list[0][2], bis = 5)
    param_list[1][1] = consider_body_motion(y1 = param_list[1][2], mean = param_list[0][2], bis = 5)
    param_list[2][1] = consider_body_motion(y1 = param_list[2][2], mean = param_list[0][2], bis = 5)

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


def VTS_motion_MODE(mode):
    # mode: happy / fear / anger / disgust / normal / love / sad  
    if mode == 'happy':
        motion = 18
        expression = [6, 10] # 星星眼 箭头眼
    elif mode == 'fear':
        motion = -1
        expression = [5] # 恐怕
    elif mode == 'anger':
        motion = -1
        expression = [16]  # 鼓嘴
    elif mode == 'disgust':
        motion = -1
        expression = [14] # 脸黑
    elif mode == 'normal':
        motion = 18     # 上下摇摆10
        expression = -1 
    elif mode == 'love':
        motion = 18     # 上下摇摆10
        expression = [12, 8] #爱心眼 脸红
    elif mode == 'sad':
        motion = -1
        expression = [11] #累
    elif mode == 'shy':
        motion = 20 # 惊讶55
        expression = [8, 12] #爱心眼 脸红       
    elif mode == 'mad':
        motion = 18 # 惊讶55
        expression = [9, 12] #生气皱眉 脸红     
    else:
        motion = 18 # 上下摇摆10
        expression = -1 
    return expression
# Vtube Studio Function Module
async def VTS_module(emotion, status= True):

    myvts = pyvts.vts(plugin_info=plugin_info)
    await myvts.connect()
    #await myvts.request_authenticate_token()  # get token
    await myvts.read_token() 
    await myvts.request_authenticate()  # use token

    expression_list = VTS_motion_MODE(emotion)

    #expression mode
    if expression_list != -1:
        for i in range(len(expression_list)):
            send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[expression_list[i]])
            await myvts.request(send_hotkey_request)
            time.sleep(0.01)

    await myvts.close()

def ControlMode_Switch(status, param_list, T, blick_num, t):
    if status == 0:
        param_list, data = Normal_Mode(param_list, T, blick_num, t)  
        current_status = 0
    if status == 1:
        param_list, data = Sleep_Mode(param_list, T, blick_num, t) 
        current_status = 3                      
    if status == 2:
        param_list, data = Awake_Mode(param_list, T, blick_num, t)  
        current_status = 2
    if status == 3:
        param_list, data = Shy_Mode(param_list, T, blick_num, t)
        current_status = 3 
    if status == 4:
        param_list, data = hold_Mode(param_list, T, blick_num, t)
        current_status = 4 
    return param_list, data, current_status

def ParamMode_Switch(status, param_list):
    # Set Param
    if status == 0:
        param_list, T, blick_num = SetParam_Normal_Mode(param_list)
    if status == 1:
        param_list, T, blick_num = SetParam_Sleep_Mode(param_list)
    if status == 2:
        param_list, T, blick_num = SetParam_Awake_Mode(param_list)
    if status == 3:
        param_list, T, blick_num = SetParam_Shy_Mode(param_list)
    if status == 4:
        param_list, T, blick_num = SetParam_hold_Mode(param_list)
    print( 'X:',param_list[0][1], 'Y:',param_list[1][1], 'Z:',param_list[2][1], 'Eye:',param_list[5][1])
    return param_list, T, blick_num 


# main control function
async def send_info():
    global status
    global trigger
    global blick
    global T
    global expression_trigger_singal

    status = 0
    trigger = False
    blick = False
    expression_trigger_singal = False
    blick_num = 0

    param_list = np.zeros((7, 3))  #body 3, eyeball 2, eyeOpen 2, 

    # init vts object
    vts = pyvts.vts(plugin_info=plugin_info)

    # Connect
    await vts.connect()
    await vts.read_token()
    await vts.request_authenticate()  # use token

    T = 2
    T_body = 2

    while True:

        print('status:', status)
        t = 0

        # trigger expression
        if expression_trigger_singal == True:
            expression_trigger_singal = False
            Expression_trigger = threading.Thread(target=lambda: asyncio.run(VTS_module(emotion)))
            Expression_trigger.start()
        # Set Param
            param_list, T, blick_num = ParamMode_Switch(status, param_list)
        while t <= T:
            if status == 0:
                param_list, data = Normal_Mode(param_list, T, blick_num, t)  
                current_status = 0
            if status == 1:
                param_list, data = Sleep_Mode(param_list, T, blick_num, t) 
                current_status = 3                      
            if status == 2:
                param_list, data = Awake_Mode(param_list, T, blick_num, t)  
                current_status = 2
            if status == 3:
                param_list, data = Shy_Mode(param_list, T, blick_num, t)
                current_status = 3 
            if status == 4:
                param_list, data = hold_Mode(param_list, T, blick_num, t)
                current_status = 4 
            set_paraemter_value = await vts.request(
                vts.vts_request.BaseRequest("InjectParameterDataRequest", data=data)
            )  
            t += 0.015
            time.sleep(0.015)

            if trigger == True:
                trigger = False
                if current_status == 0:
                    if status == 3:
                        expression_trigger_singal = True
                        emotion = 'love'
                if status == 3  | status == 4:
                    if current_status == 0:
                        expression_trigger_singal = True
                        emotion = 'love'
                print('trigger', 'to:', status, 'from:', current_status)
                break

        if current_status == 2:
            status = 0
        if current_status == 3:
            status = 4
        
async def Trigger_time():
    global status
    global trigger

    time.sleep(5)
    print("sleep start")
    status = 1
    trigger = True
    time.sleep(10)
    print("sleep end")
    status = 2
    trigger = True
    time.sleep(10)
    print("love start")
    status = 3
    trigger = True
    time.sleep(20)
    print("love end")
    status = 0
    trigger = True



if __name__ == "__main__":

    sleep = threading.Thread(target=lambda: asyncio.run(Trigger_time()))
    controlMotionY = threading.Thread(target=lambda: asyncio.run(send_info()))
    controlMotionY.start()    
    sleep.start()    
    sleep.join()

    controlMotionY.join()