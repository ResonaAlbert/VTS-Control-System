import asyncio, pyvts
import time
import threading
import math

plugin_info = {
    "plugin_name": "trigger hotkey",
    "developer": "OverHome",
    "authentication_token_path": "./pyvts_token.txt",
}

def curve(t, t0, T, y0, y1):
    t = t - t0
    y = y1 + (y1 - y0) * (t - T) ^ 3 / (T ^ 3)
    return y

async def main():
    myvts = pyvts.vts(plugin_info=plugin_info)
    await myvts.connect()
    #await myvts.request_authenticate_token()  # get token
    #await myvts.write_token() # write token
    await myvts.read_token()
    await myvts.request_authenticate()  # use token

    response_data = await myvts.request(myvts.vts_request.requestHotKeyList())
    hotkey_list = []
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkey_list.append(hotkey["name"])
    print(hotkey_list)  # ['My Animation 1', 'My Animation 2', ...]

    send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[0])
    await myvts.request(send_hotkey_request)  # send request to play 'My Animation 1'
    await myvts.close()

async def motion(num):
    myvts = pyvts.vts(plugin_info=plugin_info)
    await myvts.connect()
    #await myvts.request_authenticate_token()  # get token
    #await myvts.write_token() # write token
    await myvts.read_token()
    await myvts.request_authenticate()  # use token

    response_data = await myvts.request(myvts.vts_request.requestHotKeyList())
    hotkeyName_list = []
    hotkeyID_list = []
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkeyName_list.append(hotkey["file"])
    #print(hotkeyName_list)
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkeyID_list.append(hotkey["hotkeyID"])
    print(hotkeyName_list)
    print(hotkeyID_list)
    #print(hotkeyName_list[num])
    send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkeyID_list[num])
    await myvts.request(send_hotkey_request)  # send request to play 'My Animation 1'
    await myvts.close()

async def control(param):
    # init vts object
    vts = pyvts.vts(plugin_info=plugin_info)
    # Connect
    await vts.connect()
    await vts.read_token()
    await vts.request_authenticate()  # use token

    i = 0
    while i <= 10000:
        value = math.sin(i/10)
        value = math.sin(i/5)
        # Get the value of "start_parameter"
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

        #data["parameterValues"].append({ "id": "FaceAngleZ", "weight": 1, "value": value*30 })
        data["parameterValues"].append({ "id": "EyeRightX", "weight": 1, "value": value })
        #data["parameterValues"].append({ "id": "EyeRightY", "weight": 1, "value": value })
        data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
        data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })

        set_paraemter_value = await vts.request(
            vts.vts_request.BaseRequest("InjectParameterDataRequest", data=data)
        )  # request to get value
        #print("new parameter value info:")
        #print(set_paraemter_value["data"])  # show
        i += 1
        time.sleep(0.01)


if __name__ == "__main__":
    motion1 = threading.Thread(target=lambda: asyncio.run(motion(18)))
    motion1.start() 
    #motion2 = threading.Thread(target=lambda: asyncio.run(motion(19)))
    #motion2.start()
    motion1.join() 
    #motion2.join()
    #controlMotionY = threading.Thread(target=lambda: asyncio.run(control("FaceAngleY")))
    #controlMotionY.start()      
    #controlMotionY.join()  
