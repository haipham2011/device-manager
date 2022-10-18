from models.device import Device
import json


class DeviceConf(object):
    def __init__(self, file_path) -> None:
        super().__init__()
        self.__file_path = file_path

    def get_all_conf(self):
        with open(self.__file_path, encoding='utf-8') as f:
            return json.load(f)

    def get_system_overview(self):
        device_conf = self.get_all_conf()
        system_overview = {
            "version": device_conf["version"],
            "company": device_conf["company"],
            "location": device_conf["location"],
            "system": device_conf["system"],
            "devices": [{"id": device["id"], "code": device["code"], "name": device["name"]} for device in device_conf["devices"]]
        }

        return system_overview

    def upsert_device(self, new_device: Device):
        device_conf = self.get_all_conf()
        indice = [index for (index, item) in enumerate(
            device_conf["devices"]) if item["id"] == new_device.id]
        if len(indice) == 1:
            device_conf["devices"][indice[0]] = json.loads(new_device.json())

        else:
            device_conf["devices"].append(json.loads(new_device.json()))

        with open(self.__file_path, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(device_conf, indent=4))

        return self.get_devices()

    def get_device_with_id(self, id):
        device_conf = self.get_all_conf()
        for device in device_conf["devices"]:
            if device["id"] == id:
                return device

        return None

    def get_devices(self):
        device_conf = self.get_all_conf()

        return device_conf["devices"]

    def delete_device(self, id):
        device_conf = self.get_all_conf()
        device_conf["devices"] = [
            device for device in device_conf["devices"] if device["id"] != id]

        with open(self.__file_path, "w") as outfile:
            outfile.write(json.dumps(device_conf))
        
        return self.get_devices()
