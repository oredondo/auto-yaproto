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

    def __assign_ips(self, subnets, nets, routers):
        """

        :param subnets:
        :param nets:
        :param routers:
        :return:
        """
        config = {"nodes": {},
                  "routers": {},
                  "gateways": {}}
        red_aux = {}

        # genera diccionario con las redes y sus ips
        for value in nets:
            for item in nets[value]:
                if value in red_aux.keys():
                    pass
                else:
                    try:
                        red_aux[value] = []
                        for i in subnets.pop(0):
                            red_aux[value].append("%s" % i)
                    except BaseException:
                        pass  # TODO: Generar buenas excepciones

        # genera dicionario de configuracion con nodos y routers con sus ips
        for value in nets:
            for item in nets[value]:
                if item in routers:
                    if item in config["routers"].keys():
                        config["routers"][item].append(red_aux[value].pop(1))
                    else:
                        config["routers"][item] = [red_aux[value].pop(1)]
                        # gates = []
                        # for i in nets[value]:
                        #     if i != item:
                        #         gates.append(i)
                        # config["gateways"][config["routers"][item][0]] = gates
                else:
                    if item in config["nodes"].keys():
                        config["nodes"][item].append(red_aux[value].pop(-3))
                    else:
                        config["nodes"][item] = [red_aux[value].pop(-3)]
        self.__gateways(nets, config)
        return config

    def __gateways(self, nets, config):
        """{'nodes': {'nodo1': ['172.24.0.253'], 'nodo2': ['172.24.0.252']},
         'routers': {'router': ['172.24.0.1', '172.24.1.1', '172.24.2.1'], 'router2': ['172.24.1.2'],
                     'router3': ['172.24.2.2']}, 'gateways': {}}

        {'net1': ['nodo1', 'nodo2', 'router'], 'private1': ['router', 'router2'], 'private2': ['router', 'router3']}
        """
        for nodo in config.get("nodes"):
            print(nodo)
            for net in nets:
                print(net)

    def __get_subnets(self):
        """

        :return:
        """
        ip = IPNetwork('172.24.0.0/20')
        subnets = list(ip.subnet(24))
        return subnets
