import asyncio, pyvts
import threading
import json

plugin_info = {
    "plugin_name": "trigger hotkey",
    "developer": "OverHome",
    "authentication_token_path": "./pyvts_token.txt",
}

def get_hotkey_list(hotkeyName_list, hotkeyID_list, name_list):
    # 保存热键列表
    with open("hotkey_list.json", "w") as f:
        json.dump({"hotkeyName_list": hotkeyName_list, "hotkeyID_list": hotkeyID_list, "name_list": name_list}, f)

def read_hotkey_list():
    # 读取热键列表
    with open("hotkey_list.json", "r") as f:
        data = json.load(f)

    hotkeyName_list = data["hotkeyName_list"]
    hotkeyID_list = data["hotkeyID_list"]
    name_list = data["name_list"]

    return hotkeyName_list, hotkeyID_list, name_list

async def main():
    # request authenticate token
    myvts = pyvts.vts(plugin_info=plugin_info)
    await myvts.connect()
    #await myvts.request_authenticate_token()  # get token
    #await myvts.write_token() # write token
    await myvts.read_token()
    await myvts.request_authenticate()  # use token

    #request HotKeyList
    response_data = await myvts.request(myvts.vts_request.requestHotKeyList())
    hotkeyName_list = []
    hotkeyID_list = []
    name_list = []
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkeyName_list.append(hotkey["file"])
    for hotkey in response_data["data"]["availableHotkeys"]:
        name_list.append(hotkey["name"])
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkeyID_list.append(hotkey["hotkeyID"])
    
    # save json
    get_hotkey_list(hotkeyName_list, hotkeyID_list, name_list)
    
    print(hotkeyName_list)
    print(hotkeyID_list)
    print(name_list)
    await myvts.close()


if __name__ == "__main__":
    motion1 = threading.Thread(target=lambda: asyncio.run(main()))
    motion1.start() 
    motion1.join() 