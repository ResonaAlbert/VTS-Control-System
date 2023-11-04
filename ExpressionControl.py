import pyvts
import time
import json
import threading
import asyncio

plugin_info = {
    "plugin_name": "trigger hotkey",
    "developer": "OverHome",
    "authentication_token_path": "./pyvts_token.txt",
}

hotkeyname_list = [ 'OO眼.exp3.json', 'Scene1.exp3.json', '压扁.exp3.json', '堵嘴.exp3.json', '屑.exp3.json', 
                     '恐怕.exp3.json', '星星眼.exp3.json', '汗.exp3.json', '爱心眼.exp3.json', '生气皱眉.exp3.json', 
                     '箭头眼.exp3.json', '累.exp3.json', '脸红.exp3.json', '脸青.exp3.json', '脸黑.exp3.json', 
                     '话筒.exp3.json', '鼓嘴.exp3.json', '@@眼.exp3.json']
hotkey_list = ['83a2d987f7064642b7a9d3640274333b', '06826505889b40678302597311c79911', '12ca15e78fe7421483691b167fe7482d', 
                'b1cd02db9cfa4b04bddb1ee48c326dae', '47a8088c7b6a415b8158c2f42b0485e2', 'edb893b80c294871b6635ae0b42d44e6', 
                '0a7bf45151324c6d82ccdda5f34e4115', 'bee0edc6cf65491f9cc2e2bcd768ee2b', '7b849ad686b94e328a4c3748e19be7c6', 
                'bf102f7962dc47cd81de8c8366d39147', 'edfc753b78024779ad5bca0bf7f73f8e', 'e379e9d6b94d4ffe98d1e89dd7673843', 
                'a18ce5e4d0a144ac9b4a0805241048c8', '70f8c48382634faba50555b76940cd72', 'd2894537a77a43238df478324cd55a55', 
                'c292a2b25b424c48bf177e64db22cdc7', 'b6157183d1d94b1eaecfa8dd28522abe', '8ee59d635dd041ccb2335280cf7fff9d', 
                'e217ac7c24b540ebb72fdfe11d42479c', 'da76c120eb0745a9a2621a8c0ea4fde7', 'cf9269def5be447ea9b6c44a2ef34ef8']

def VTS_motion_MODE(mode):
    # mode: happy / fear / anger / disgust / normal / love / sad  
    if mode == 'happy':
        expression = [6, 10] # 星星眼 箭头眼
    elif mode == 'fear':
        expression = [5] # 恐怕
    elif mode == 'anger':
        expression = [16]  # 鼓嘴
    elif mode == 'disgust':
        expression = [14] # 脸黑
    elif mode == 'normal':
        expression = -1 
    elif mode == 'love':
        expression = [12, 8] #爱心眼 脸红
    elif mode == 'sad':
        expression = [11] #累
    elif mode == 'shy':
        expression = [8, 12] #爱心眼 脸红       
    elif mode == 'mad':
        expression = [9, 12] #生气皱眉 脸红     
    else:
        expression = -1 
    return expression

# Vtube Studio Function Module
async def VTS_module(emotion = 0, hotkeyID_list = hotkey_list, status= True):

    myvts = pyvts.vts(plugin_info=plugin_info, IP = "localhost")
    await myvts.connect()
    #await myvts.request_authenticate_token()  # get token
    await myvts.read_token() 
    await myvts.request_authenticate()  # use token

    expression_list = VTS_motion_MODE(emotion)

    #expression mode
    if expression_list != -1:
        for i in range(len(expression_list)):
            send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkeyID_list[expression_list[i]])
            await myvts.request(send_hotkey_request)

    await myvts.close()
