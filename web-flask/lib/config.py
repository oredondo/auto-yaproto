from netaddr import IPNetwork

class Config(object):

    def __init__(self, data=None):
        self.__parse(data)
        self.__get_nets(data)

    def __parse(self, data):
        pass

    def __get_nets(self, data):
        nets = {}
        routers = []
        i = 0
        for item in data.get("elements").get("nodes"):
            if "parent" in item.get("data").keys():
                nets.setdefault(item.get("data").get("parent"), []).append(item.get("data").get("text"))
            if item.get("data").get("type") == "rectangle" and item.get("data").get("meta") != "net":
                routers.append(item.get("data").get("text"))

        for item in data.get("elements").get("edges"):
            if item.get("data").get("source") in routers and not item.get("data").get("target") in routers:
                for key, value in nets.items():
                    if item.get("data").get("target") in value and not item.get("data").get("source") in value:
                        nets[key].append(item.get("data").get("source"))

            if item.get("data").get("target") in routers and not item.get("data").get("source") in routers:
                for key, value in nets.items():
                    if item.get("data").get("source") in value and not item.get("data").get("target") in value:
                        nets[key].append(item.get("data").get("target"))

            if item.get("data").get("target") in routers and item.get("data").get("source") in routers:
                i = i + 1
                nets.setdefault("private" + str(i), []).append(item.get("data").get("source"))
                nets.setdefault("private" + str(i), []).append(item.get("data").get("target"))
        return nets, routers

    def __get_routers(self):
        pass

    def __get_subnets(self):
        ip = IPNetwork('172.24.0.0/16')
        subnets = list(ip.subnet(23))
        for ip in subnets:
            print(subnets)
            print('%s' % ip)
            break
        #128
        # subnets
        # [IPNetwork('172.24.0.0/23'), IPNetwork('172.24.2.0/23'), IPNetwork('172.24.4.0/23'), ...,
        # IPNetwork('172.24.250.0/23'), IPNetwork('172.24.252.0/23'), IPNetwork('172.24.254.0/23')]
