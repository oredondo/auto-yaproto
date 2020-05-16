from netaddr import IPNetwork
import ipaddress

class Config(object):

    def __init__(self, data=None):
        nets, routers, gateways, puertos, puertos_mosquitto = self.__get_nets(data)
        self.config = self.__assign_ips(subnets=self.__get_subnets(), nets=nets,
                                        routers=routers, gateways=gateways, puertos=puertos,
                                        puertos_mosquitto=puertos_mosquitto)

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
        puertos_mosquitto = {}
        routers = []
        for item in data.get("elements").get("nodes"):

            if "parent" in item.get("data").keys():
                puertos[item.get("data").get("text")] = item.get("data").get("port")
                puertos_mosquitto[item.get("data").get("text")] = item.get("data").get("port_mosquitto")
                nets.setdefault(item.get("data").get("parent"), []).append(item.get("data").get("text"))
            if item.get("data").get("type") == "rectangle" and item.get("data").get("meta") != "net":
                puertos[item.get("data").get("text")] = item.get("data").get("port")
                puertos_mosquitto[item.get("data").get("text")] = item.get("data").get("port_mosquitto")
                routers.append(item.get("data").get("text"))
        for edge in data.get("elements").get("edges"):
            if edge.get("data").get("source") not in nets.keys() and edge.get("data").get("target") not in routers:
                nets[edge.get("data").get("target")].append(edge.get("data").get("source"))
                gateways[edge.get("data").get("target")] = edge.get("data").get("source")
            elif edge.get("data").get("target") not in nets.keys():
                nets[edge.get("data").get("target") + "_$connectador$_" + edge.get("data").get("source")] = [
                    edge.get("data").get("target"),
                    edge.get("data").get("source")]

        return nets, routers, gateways, puertos, puertos_mosquitto

    def __assign_ips(self, subnets, nets, routers, gateways, puertos, puertos_mosquitto):
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
                        elif cont == 0:
                            red_aux[value]["netmask"] = str(i)
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
                    if aux.get("net") == net:
                        aux["puerto"] = puertos.get(item1)
                        aux["puerto_mosquitto"] = puertos_mosquitto.get(item1)
                        aux["gateway"] = red_aux.get(net).get("gateway")
            for item1 in config.get("routers"):
                for aux in config.get("routers").get(item1):
                    if aux.get("net") == net and net not in gateways.keys():
                        lista = net.split("_$connectador$_")
                        lista.remove(item1)
                        asigno_gateway = False
                        for i in config.get("routers").get(item1):
                            if i.get("gateway") != "":
                                asigno_gateway = True
                        for i in config.get("routers").get(lista[0]):
                            if i.get("net") == net and not asigno_gateway:
                                aux["gateway"] = i.get("ip")
                                aux["puerto"] = puertos.get(item1)
                                aux["puerto_mosquitto"] = puertos_mosquitto.get(item1)
                                asigno_gateway = True

        for item2 in config.get("routers"):
            notienegateway = True
            redes = []
            for valor in config.get("routers").get(item2):
                if valor.get("gateway") != "":
                    notienegateway = False
                if valor.get("net").find("$connectador$") != -1:
                    redes.append(valor.get("net").replace(item2, "").replace("_$connectador$_", ""))
            if len(redes) == len(config.get("routers").get(item2)):
                config.get("routers").get(item2)[0]["gateway"] = config.get("routers").get(item2)[0]["ip"]
                config.get("routers").get(item2)[0]["puerto"] = puertos.get(item2)
                config.get("routers").get(item2)[0]["puerto_mosquitto"] = puertos_mosquitto.get(item2)
                for router in redes:
                    for otra in config.get("routers").get(router):
                        if otra["gateway"] != "":
                            for red in config.get("routers").get(item2):
                                if red["net"].find(router) != -1 and red["net"].find("_$connectador$_") != -1:
                                    otra["gateway"] = red["ip"]
            if notienegateway:
                config.get("routers").get(item2)[0]["gateway"] = config.get("routers").get(item2)[0]["ip"]
                config.get("routers").get(item2)[0]["puerto"] = puertos.get(item2)
                config.get("routers").get(item2)[0]["puerto_mosquitto"] = puertos_mosquitto.get(item2)

        ### Agrego rutas para los nodos que se podrian quedar aislados.
        for item2 in config.get("routers"):
            cont = 0
            for eth in config.get("routers").get(item2):
                if eth.get("gateway") == "" and eth.get("net").find("$connectador$") != -1:
                    agregar = eth.get("net").replace(item2, "").replace("_$connectador$_", "")
                    nets_destino = []
                    ip_gateway = None
                    for v in config.get("routers").get(agregar):
                        if v.get("net") == eth.get("net"):
                            ip_gateway = v.get("ip")
                        if v.get("net").find("$connectador$") == -1:
                            nets_destino.append(red_aux.get(v.get("net")).get("netmask"))
                    if ip_gateway:
                        eth["gateway"] = ip_gateway
                        eth["nets_destino"] = nets_destino
                cont = cont + 1

        return config


    def __get_subnets(self):
        """

        :return:
        """
        ip = IPNetwork('172.24.0.0/19')
        subnets = list(ip.subnet(24))
        return subnets
