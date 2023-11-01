import asyncio, pyvts
import time
plugin_info = {
    "plugin_name": "trigger hotkey",
    "developer": "OverHome",
    "authentication_token_path": "./pyvts_token.txt",
}


async def main():
    myvts = pyvts.vts(plugin_info=plugin_info)
    await myvts.connect()
    await myvts.request_authenticate_token()  # get token
    await myvts.write_token()
    await myvts.read_token()
    await myvts.request_authenticate()  # use token

    response_data = await myvts.request(myvts.vts_request.requestHotKeyList())
    hotkey_list = []
    hotkey_name = []
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkey_list.append(hotkey["hotkeyID"])
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkey_name.append(hotkey["file"])
    #print(hotkey_list)  # ['My Animation 1', 'My Animation 2', ...]
    print(hotkey_name)
    #print(hotkey_name)
    send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[0])
    await myvts.request(send_hotkey_request)  # send request to play 'My Animation 1'

    await myvts.close()


if __name__ == "__main__":
    
    #while True:
    asyncio.run(main())
        #time.sleep(20)
