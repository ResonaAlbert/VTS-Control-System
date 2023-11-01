import sys

sys.path.insert(0, "../pyvts")

import asyncio
import pyvts
import time 


async def main():
    # init vts object
    plugin_info = {
        "plugin_name": "start pyvts",
        "developer": "Genteki",
        "authentication_token_path": "./token.txt",
    }
    vts = pyvts.vts(plugin_info=plugin_info)

    # Connect
    await vts.connect()

    # Authenticate
    await vts.request_authenticate_token()  # get token
    await vts.request_authenticate()  # use token

    # Custom new parameter named "start_parameter"
    new_parameter_name = "start_parameter"
    recv_new_parameter = await vts.request(
        vts.vts_request.requestCustomParameter(new_parameter_name)
    )  # request custum parameter
    print("received msg after adding the parameter:")
    print(recv_new_parameter["data"])  # print response message

    # Get the value of "start_parameter"
    new_paraemter_value = await vts.request(
        vts.vts_request.requestParameterValue(new_parameter_name)
    )  # request to get value
    print("new parameter value info:")
    print(new_paraemter_value["data"])  # show

    # Delete that parameter
    await asyncio.sleep(3)  # sleep 10 seconds
    return_msg = await vts.request(
        vts.vts_request.requestDeleteCustomParameter(new_parameter_name)
    )  # delete the parameter
    print(return_msg)

    i = 0
    while i <= 100:
        # Get the value of "start_parameter"
        set_paraemter_value = await vts.request(
            vts.vts_request.requestSetParameterValue("FaceAngleX", 80)
        )  # request to get value
        print("new parameter value info:")
        print(set_paraemter_value["data"])  # show
        time.sleep(0.8)

if __name__ == "__main__":
    asyncio.run(main())
