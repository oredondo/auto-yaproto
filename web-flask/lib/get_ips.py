from lib.config import Config
import json


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
