import asyncio, pyvts
import time
import threading
import math
import random
import numpy as np
import ParamControl as PC
import ExpressionControl as EC

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


def ControlMode_Switch(status, param_list, T, blick_num, t):
    if status == 0:
        param_list, data = PC.Normal_Mode(param_list, T, blick_num, t)  
    if status == 1:
        param_list, data = PC.Sleep_Mode(param_list, T, blick_num, t) 
    if status == 2:
        param_list, data = PC.Awake_Mode(param_list, T, blick_num, t)  
    if status == 3:
        param_list, data = PC.Shy_Mode(param_list, T, blick_num, t)
    if status == 4:
        param_list, data = PC.hold_Mode(param_list, T, blick_num, t)
    current_status = status
    return param_list, data, current_status

def ParamMode_Switch(status, param_list):
    # Set Param
    if status == 0:
        param_list, T, blick_num = PC.SetParam_Normal_Mode(param_list)
    if status == 1:
        param_list, T, blick_num = PC.SetParam_Sleep_Mode(param_list)
    if status == 2:
        param_list, T, blick_num = PC.SetParam_Awake_Mode(param_list)
    if status == 3:
        param_list, T, blick_num = PC.SetParam_Shy_Mode(param_list)
    if status == 4:
        param_list, T, blick_num = PC.SetParam_hold_Mode(param_list)
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

    param_list = np.zeros((8, 3))  #body 3, eyeball 2, eyeOpen 2, Mouth Open 1

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
            Expression_trigger = threading.Thread(target=lambda: asyncio.run(EC.VTS_module(emotion)))
            Expression_trigger.start()
            #Expression_trigger.join()

        # Set Param
        param_list, T, blick_num = ParamMode_Switch(status, param_list)

        while t <= T:
            if trigger == False:
                param_list, data, current_status = ControlMode_Switch(status, param_list, T, blick_num, t)

            set_paraemter_value = await vts.request(
                vts.vts_request.BaseRequest("InjectParameterDataRequest", data=data)
            )  
            t += 0.015
            time.sleep(0.015)

            if trigger == True:
                # check expression
                # shy mode
                if current_status == 0:
                    if status == 3:
                        expression_trigger_singal = True
                    emotion = 'love'
                
                # reset to normal mode
                if current_status == 4:
                    if status == 0:
                        expression_trigger_singal = True
                    emotion = 'love'

                print('trigger', 'to:', status, 'from:', current_status)
                trigger = False
                break

        # 0 normal 1 sleep 2 awake 3 Shy 4 hold
        if current_status == 2: # awake
            status = 0 # 0 normal 
        if current_status == 3: #3 Shy
            status = 4 # 4 hold
        
async def Trigger_time():
    global status
    global trigger

    time.sleep(10)
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
    time.sleep(10)
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