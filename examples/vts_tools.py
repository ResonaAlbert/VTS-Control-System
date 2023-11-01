import sys
import threading
sys.path.insert(0, "../pyvts")

import asyncio
import pyvts
import time 

plugin_info = {
    "plugin_name": "trigger hotkey",
    "developer": "OverHome",
    "authentication_token_path": "./pyvts_token.txt",
}

async def Hotkeyrequire(myvts):
    response_data = await myvts.request(myvts.vts_request.requestHotKeyList())
    hotkey_list = []
    hotkeyname_list = []
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkey_list.append(hotkey["hotkeyID"])
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkeyname_list.append(hotkey["file"])
    #print(hotkeyname_list)  # ['My Animation 1', 'My Animation 2', ...]
    #for i in range(len(hotkeyname_list)):
    #    print(f"{i}:{hotkeyname_list[i]}")

    return hotkey_list, hotkeyname_list

async def send_hotkey_request(myvts, hotkey_id):
    send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_id)
    await myvts.request(send_hotkey_request)

async def set_parameter_value(myvts, parameter_name, parameter_value):
    
    set_parameter_value = myvts.vts_request.requestSetParameterValue(
        parameter_name, parameter_value
    )
    await myvts.request(set_parameter_value)



async def VTS_threading():

    End_VTS = True
    
    myvts = pyvts.vts(plugin_info=plugin_info)
    await myvts.connect()
    await myvts.request_authenticate_token()  # get token
    await myvts.request_authenticate()  # use token

    hotkey_list, hotkeyname_list = await Hotkeyrequire(myvts)
    print(hotkey_list)
    print(hotkeyname_list)
    i = 1
    
    await send_hotkey_request(myvts, hotkey_list[i])
    time.sleep(15)
    await set_parameter_value(myvts, "FaceAngleX", 0)
    time.sleep(5)
    await set_parameter_value(myvts, "FaceAngleY", 20)
    if End_VTS ==True:
        await myvts.close()


if __name__ == "__main__":

    asyncio_thread = threading.Thread(target=lambda: asyncio.run(VTS_threading()))
    asyncio_thread.daemon = True
    asyncio_thread.start()
    #End_VTS = True
    #asyncio_thread.join()
