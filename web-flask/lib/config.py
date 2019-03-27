from netaddr import IPNetwork


class Config(object):

    def __init__(self, data=None):
        nets, routers = self.__get_nets(data)
        self.config = self.__assign_ips(subnets=self.__get_subnets(), nets=nets, routers=routers)

    def get(self):
        return self.config

    def __get_nets(self, data):
        """
        Parsea el dicionario de la red para generar un dict con los nodos y sus redes.
        :param data:
        :return:
        """
        nets = {}
        routers = []
        i = 0
        for item in data.get("elements").get("nodes"):
            if "parent" in item.get("data").keys():
                nets.setdefault(item.get("data").get("text"), []).append(item.get("data").get("parent"))
            if item.get("data").get("type") == "rectangle" and item.get("data").get("meta") != "net":
                routers.append(item.get("data").get("text"))
                nets.setdefault(item.get("data").get("text"), [])

        for item in data.get("elements").get("edges"):
            if item.get("data").get("source") in routers and not item.get("data").get("target") in routers:
                if nets[item.get("data").get("target")][0] not in nets[item.get("data").get("source")]:
                    nets[item.get("data").get("source")].append(nets[item.get("data").get("target")][0])

            if item.get("data").get("target") in routers and not item.get("data").get("source") in routers:
                if nets[item.get("data").get("source")][0] not in nets[item.get("data").get("target")]:
                    nets[item.get("data").get("target")].append(nets[item.get("data").get("source")][0])

            if item.get("data").get("target") in routers and item.get("data").get("source") in routers:
                i = i + 1
                nets.setdefault(item.get("data").get("source"), []).append("private" + str(i))
                nets.setdefault(item.get("data").get("target"), []).append("private" + str(i))
        return nets, routers


    def __assign_ips(self, subnets, nets, routers):
        """

        :param subnets:
        :param nets:
        :param routers:
        :return:
        """
        config = {"nodes": {},
                  "routers": {}}
        red_aux = {}

        # genera diccionario con las redes y sus ips
        for value in nets:
            for item in nets[value]:
                if item in red_aux.keys():
                    pass
                else:
                    try:
                        red_aux[item] = []
                        for i in subnets.pop(0):
                            red_aux[item].append("%s" % i)
                    except BaseException:
                        pass  # TODO: Generar buenas excepciones

        # genera dicionario de configuracion con nodos y routers con sus ips
        for value in nets:
            if value in routers:
                for item in nets[value]:
                    if value in config["routers"].keys():
                        config["routers"][value].append(red_aux[item].pop(1))
                    else:
                        config["routers"][value] = [red_aux[item].pop(1)]
            else:
                for item in nets[value]:
                    if value in config["nodes"].keys():
                        config["nodes"][value].append(red_aux[item].pop(-3))
                    else:
                        config["nodes"][value] = [red_aux[item].pop(-3)]
        return config


    def __get_subnets(self):
        """

        :return:
        """
        ip = IPNetwork('172.24.0.0/19')
        subnets = list(ip.subnet(23))
        return subnets

