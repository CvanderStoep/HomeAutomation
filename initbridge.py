from phue import Bridge
import time
import os


def initbridge():
    # global bridge
    from private_info import ip_address_hue_bridge
    # bridge = Bridge(ip_address_hue_bridge)  # connected to Deco mesh
    bridge = Bridge(ip=ip_address_hue_bridge, config_file_path='./.python_hue')  # connected to Deco mesh
    bridge.connect()  # this command is needed only once; press hue bridge button en run bridge.connect() command.
    return bridge


