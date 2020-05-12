from lib.config import Config
import json
from pathlib import Path
import os


class GetIps(object):

    def __init__(self, data=None):
        self.data = json.loads(data)

    def get(self):
        conf = Config(data=self.data).get()
        output = {}
        all_ip = []
        for item in conf.get("nodes"):
            output[item] = []
            for ip in conf.get("nodes").get(item):
                output[item].append(ip.get("ip"))
                all_ip.append(ip.get("ip"))
        for item in conf.get("routers"):
            output[item] = []
            for ip in conf.get("routers").get(item):
                output[item].append(ip.get("ip"))
                all_ip.append(ip.get("ip"))
        output["all_ips"] = all_ip
        return output


class LoadSave(object):

    def __init__(self, data=None):
        self.dir = "{}/dirsave".format(Path(os.path.dirname(os.path.abspath(__file__))))
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        if data:
            self.data = json.loads(data)
            self.name = self.data.get("name")
            del self.data["name"]

    def save(self):
        if os.path.isfile('{}/{}.json'.format(self.dir, self.name)):
            os.remove('{}/{}.json'.format(self.dir, self.name))
        with open('{}/{}.json'.format(self.dir, self.name), 'w') as outfile:
            json.dump(self.data, outfile)
        return True

    def list_json(self):
        return {"files": [obj.name.replace(".json", "") for obj in Path(self.dir).iterdir() if obj.is_file()]}

    def load(self):
        with open('{}/{}.json'.format(self.dir, self.name)) as json_file:
            return json.load(json_file)


class Puertos(object):

    def __init__(self, data):
        self.ports = []
        for item in data.get("elements").get("nodes"):
            if item.get("data").get("color") == "grey":
                self.ports.append(item.get("data").get("port"))
                self.ports.append(item.get("data").get("port_mosquitto"))
        self.ports.sort()
    def get(self):
        result = self.ports[-1] + 1
        self.ports.append(result)
        self.ports.sort()
        return result