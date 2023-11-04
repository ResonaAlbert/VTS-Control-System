import asyncio, pyvts
import time
import threading
import numpy as np
import ParamControl as PC
import ExpressionControl as EC
import json
from flask import Flask, request

plugin_info = {
    "plugin_name": "trigger hotkey",
    "developer": "OverHome",
    "authentication_token_path": "./pyvts_token.txt",
}


global status  # 0 normal 1 sleep 2 awake 3 Shy 4 hold 5 CheerUp 6 beats
global change_status

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
        param_list, T, blick_num = PC.SetParam_Hold_Mode(param_list)
    if status == 5:
        param_list, T, blick_num = PC.SetParam_Cheerup_Mode(param_list)
    if status == 6:
        param_list, T, blick_num = PC.SetParam_Beats_Mode(param_list)
    print( 'X:',param_list[0][1], 'Y:',param_list[1][1], 'Z:',param_list[2][1], 'Eye:',param_list[5][1])
    return param_list, T, blick_num 

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
        param_list, data = PC.Hold_Mode(param_list, T, blick_num, t)
    if status == 5:
        param_list, data = PC.Cheerup_Mode(param_list, T, blick_num, t)
    if status == 6:
        param_list, data = PC.Beats_Mode(param_list, T, blick_num, t)
    current_status = status
    return param_list, data, current_status

def check_expression(current_status, status):
    # check expression
    # shy mode
    if current_status == 0:
        if status == 3:
            emotion = 'love'
            emotion_trigger = True
            return emotion, emotion_trigger
    if current_status == 4:
        if status == 0:
            emotion = 'love' 
            emotion_trigger = True
            return emotion, emotion_trigger
    if current_status == 3:
        if status == 0:
            emotion = 'love' 
            emotion_trigger = True
            return emotion, emotion_trigger
    else:
        emotion = ""
        emotion_trigger = False      
        return emotion, emotion_trigger

def change_status_onetime(current_status, status):
    # 0 normal 1 sleep 2 awake 3 Shy 4 hold
    # after 2 awake change back to normal mode
    if current_status == 2: 
        status = 0 # 0 normal
        return current_status, status
     #after 3 Shy change to hold mode to wait
    if current_status == 3:
        status = 4 # 4 hold    \
        return current_status, status
     #after 5 CheerUp change back to Normal Mode
    if current_status == 5:
        status = 0 # 0 Normal 
        return current_status, status   
    return current_status, status

def read_hotkey_list():
    # 读取热键列表
    with open("./hotkey_list.json", "r") as f:
        data = json.load(f)

    hotkeyName_list = data["hotkeyName_list"]
    hotkeyID_list = data["hotkeyID_list"]
    name_list = data["name_list"]

    return hotkeyName_list, hotkeyID_list, name_list

# main control function
async def ControlSystem_main():

    hotkeyName_list, hotkeyID_list, name_list = read_hotkey_list()
    
    global status
    global change_status
    global current_status
    status = 0
    change_status = False
    emotion = False
    emotion_trigger = False
    param_list = np.zeros((8, 3))  #body 3, eyeball 2, eyeOpen 2, Mouth Open 1

    # init vts object
    vts = pyvts.vts(plugin_info=plugin_info, IP = "localhost")

    # Connect
    await vts.connect()
    #await vts.request_authenticate_token()  # get token
    #await vts.write_token() # write token
    await vts.read_token()
    await vts.request_authenticate()  # use token

    while True:

        print('status:', status)
        t = 0

        # change_status expression
        if emotion_trigger == True:
            print('emotion:', emotion)
            Expression_change_status = threading.Thread(target=lambda: asyncio.run(EC.VTS_module(emotion = emotion)))
            Expression_change_status.start()
            emotion_trigger = False

        # Set Param
        param_list, T_list, blick_num = ParamMode_Switch(status, param_list)

        while t <= T_list[0]:

            if change_status == False:
                param_list, data, current_status = ControlMode_Switch(status, param_list, T_list, blick_num, t)
                #print(data)
                set_paraemter_value = await vts.request(vts.vts_request.BaseRequest("InjectParameterDataRequest", data=data))  
            else:
                # check expression
                emotion, emotion_trigger  = check_expression(current_status, status)
                print('change_status', 'from:', current_status, 'to:', status)
                change_status = False
                break

            Update_Hetz = 60
            update_time  = 1/Update_Hetz
            t += update_time
            time.sleep(update_time)

        # 0 normal 1 sleep 2 awake 3 Shy 4 hold
        current_status, status = change_status_onetime(current_status, status)
        
async def change_status_time():
    global status
    global change_status

    time.sleep(10)
    print("sleep start")
    status = 6
    change_status = True
    if True:
        time.sleep(20)
        print("sleep end")
        status = 2
        change_status = True
        time.sleep(5)
        print("love start")
        status = 3
        change_status = True
        time.sleep(5)
        print("love end")
        status = 0
        time.sleep(5)
        print("CheerUp start")
        status = 5
        time.sleep(5)
        print("Beats start")
        status = 6
        change_status = True

# 定义flask_thread函数，用于启动flask服务
app = Flask(__name__)
def flask_thread():
    app.run(host='0.0.0.0', port=6666)
# 定义/receive_text路由，使用POST方法，用于接收文本
@app.route('/receive_text', methods=['POST'])
def receive_text():
    # 定义全局变量question_list
    global status
    global current_status
    # 获取请求中的json数据
    data = request.get_json()
    # 从json数据中获取文本
    status = data.get('status')
    # 打印获取的文本
    # 定义返回信息
    reply = {"status": current_status}
    # 将返回信息转换为json格式
    reply_json = json.dumps(reply)


if __name__ == "__main__":
    if False:
        #Client part
        flask_server_thread = threading.Thread(target=flask_thread)
        flask_server_thread.daemon = True

    ModeChange = threading.Thread(target=lambda: asyncio.run(change_status_time()))
    controlMotion = threading.Thread(target=lambda: asyncio.run(ControlSystem_main()))
    controlMotion.start()    
    ModeChange.start()    
    ModeChange.join()
    controlMotion.join()