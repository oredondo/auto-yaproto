from netaddr import IPNetwork


class Config(object):

    def __init__(self, data=None):
        nets, routers, gateways, puertos = self.__get_nets(data)
        self.config = self.__assign_ips(subnets=self.__get_subnets(), nets=nets,
                                        routers=routers, gateways=gateways, puertos=puertos)

    def get(self):
        return self.config

    def __get_nets(self, data):
        """
        Parsea el dicionario de la red para generar un dict con los nodos y sus redes.
        :param data:
        :return:
        """
        nets = {}
        gateways = {}
        puertos = {}
        routers = []
        for item in data.get("elements").get("nodes"):

            if "parent" in item.get("data").keys():
                puertos[item.get("data").get("text")] = item.get("data").get("port")
                nets.setdefault(item.get("data").get("parent"), []).append(item.get("data").get("text"))
            if item.get("data").get("type") == "rectangle" and item.get("data").get("meta") != "net":
                puertos[item.get("data").get("text")] = item.get("data").get("port")
                routers.append(item.get("data").get("text"))
        for edge in data.get("elements").get("edges"):
            if edge.get("data").get("source") not in nets.keys() and edge.get("data").get("target") not in routers:
                nets[edge.get("data").get("target")].append(edge.get("data").get("source"))
                gateways[edge.get("data").get("target")] = edge.get("data").get("source")
            elif edge.get("data").get("target") not in nets.keys():
                nets[edge.get("data").get("target") + "_$router$_" + edge.get("data").get("source")] = [
                    edge.get("data").get("target"),
                    edge.get("data").get("source")]

        return nets, routers, gateways, puertos

    def __assign_ips(self, subnets, nets, routers, gateways, puertos):
        """

        :param subnets:
        :param nets:
        :param routers:
        :return:
        """
        config = {"nodes": {},
                  "routers": {}}
        red_aux = {}
        allips = []
        # genera diccionario con las redes y sus ips
        for value in nets:
            for item in nets[value]:
                if value in red_aux.keys():
                    pass
                else:
                    red_aux[value] = {}
                    red_aux[value]["ips"] = []
                    subnets.pop(0)
                    cont = 0
                    for i in subnets.pop(0):
                        if cont > 2:
                            red_aux[value]["ips"].append("%s" % i)
                        elif cont == 2:
                            red_aux[value]["gateway"] = str(i)
                        cont = cont + 1

        # genera dicionario de configuracion con nodos y routers con sus ips

        for value in nets:
            for item in nets[value]:
                if item in routers:
                    if gateways.get(value) == item:
                        ip = red_aux[value]["gateway"]
                        if item in config["routers"].keys():
                            config["routers"][item].append({"ip": ip,
                                                            "net": value,
                                                            "gateway": ""})
                        else:
                            config["routers"][item] = [{"ip": ip,
                                                        "net": value,
                                                        "gateway": ""}]

                    elif item in config["routers"].keys():
                        config["routers"][item].append({"ip": red_aux[value]["ips"].pop(-3),
                                                        "net": value,
                                                        "gateway": ""})
                    else:
                        config["routers"][item] = [{"ip": red_aux[value]["ips"].pop(-3),
                                                    "net": value,
                                                    "gateway": ""}]
                else:
                    if item in config["nodes"].keys():
                        config["nodes"][item].append({"ip": red_aux[value]["ips"].pop(-3),
                                                      "net": value,
                                                      "gateway": ""})
                    else:
                        config["nodes"][item] = [{"ip": red_aux[value]["ips"].pop(-3),
                                                  "net": value,
                                                  "gateway": ""}]

        for net in red_aux:
            for item1 in config.get("nodes"):
                for aux in config.get("nodes").get(item1):
                    if aux.get("ip") not in allips:
                        allips.append(aux.get("ip"))
                    if aux.get("net") == net:
                        aux["puerto"] = puertos.get(item1)
                        aux["gateway"] = red_aux.get(net).get("gateway")

            for item1 in config.get("routers"):
                for aux in config.get("routers").get(item1):
                    if aux.get("ip") not in allips:
                        allips.append(aux.get("ip"))
                    if aux.get("net") == net and net not in gateways.keys():
                        lista = net.split("_$router$_")
                        lista.remove(item1)
                        for i in config.get("routers").get(lista[0]):
                            if i.get("net") == net:
                                aux["gateway"] = i.get("ip")
                                aux["puerto"] = puertos.get(item1)

        for item2 in config.get("routers"):
            notienegateway = True
            for valor in config.get("routers").get(item2):
                if valor.get("gateway") != "":
                    notienegateway = False
            if notienegateway:
                config.get("routers").get(item2)[0]["gateway"] = config.get("routers").get(item2)[0]["ip"]
                config.get("routers").get(item2)[0]["puerto"] = puertos.get(item2)
        config["ips"] = allips
        return config


    def __get_subnets(self):
        """

        :return:
        """
        ip = IPNetwork('172.24.0.0/20')
        subnets = list(ip.subnet(24))
        return subnets
