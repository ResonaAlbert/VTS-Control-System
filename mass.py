#from requests import get
#
#url = "http://93.55.228.194:8123/api/states/sensor.esphome_web_dcdf28_hx711_value"
##url = "http://93.55.228.194:8123/api/states/switch.sonoff_1000245744"
#
#headers = {
#    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlNzE1OWYxNzAwNTk0ZDIxODU4OTI5YmQ3NjExZWFmOCIsImlhdCI6MTY5ODUyOTYxNCwiZXhwIjoyMDEzODg5NjE0fQ.e0veWiZvcRAF821ZBroQxLksnoCDBNeMA4Ps7hGrCiE",
#    "content-type": "application/json",
#}
#
#response = get(url, headers=headers)
#print(response.text)

import requests

def get_sensor_value():
    """获取 Home Assistant 中 sensor.esphome_web_dcdf28_hx711_value 的数值。"""

    url = "http://93.55.228.194:8123/api/states/sensor.esphome_web_dcdf28_hx711_value"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlNzE1OWYxNzAwNTk0ZDIxODU4OTI5YmQ3NjExZWFmOCIsImlhdCI6MTY5ODUyOTYxNCwiZXhwIjoyMDEzODg5NjE0fQ.e0veWiZvcRAF821ZBroQxLksnoCDBNeMA4Ps7hGrCiE",
        "content-type": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["state"]
    else:
        raise ValueError(f"获取 Home Assistant 状态失败，状态码：{response.status_code}")


if __name__ == "__main__":
    value = get_sensor_value()
    print(value)
