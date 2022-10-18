import json

from fastapi import FastAPI
from modules import config
from models.device import Device

API_VERSION = 1
API_PREFIX = f"api/dm/v{API_VERSION}"

app = FastAPI()
device_config = config.DeviceConf("./public/device_conf.json")

@app.get(f"/{API_PREFIX}/overview")
def get_overview():
    return device_config.get_system_overview()

@app.get(f"/{API_PREFIX}/devices")
def get_devices():
    return device_config.get_devices()

@app.get(f"/{API_PREFIX}/" + "devices/{item_id}")
def get_device(item_id: int):
    return device_config.get_device_with_id(item_id)

@app.post(f"/{API_PREFIX}/" + "devices")
async def upsert_device(device: Device):
    return device_config.upsert_device(device)

@app.delete(f"/{API_PREFIX}/" + "devices/{item_id}")
def delete_device(item_id: int):
    return device_config.delete_device(item_id)