import random


class Style(object):
    def __init__(self):
        self.style = [{
            "selector": 'node',
            "style": {
                'width': 60,
                'height': 60,
                "shape": 'data(type)',
                'content': 'data(text)',
                'text-valign': 'center',
                'color': 'white',
                'text-outline-width': 2,
                'text-outline-color': '#222',
                'text-valign': 'top',
                'background-color': "data(color)"
            }
        },
            {
                "selector": 'edge',
                "style": {
                    'width': 5,
                    'line-color': 'data(color)',
                    'target-arrow-color': '#9dbaea'
                }
            },

            {
                "selector": ':selected',
                "style": {
                    'background-color': 'yellow',
                    'line-color': 'yellow',
                    'target-arrow-color': 'black',
                    'source-arrow-color': 'black',
                }
            },
            {
                "selector": 'edge:selected',
                "style": {
                    'width': 10
                }
            }
        ]

    def get(self):
        return self.style


class Elements(object):

    def __init__(self):
        self.element = {
            "nodes": [{
                "data": {
                    "id": "router",
                    "text": 'router',
                    "parent": "netRouter",
                    "type": 'rectangle',
                    "color": "grey"
                }
            }, {
                "data": {
                    "id": 'nodo1',
                    "text": 'nodo1',
                    "parent": 'net1',
                    "type": "ellipse",
                    "color": "grey"
                }
            }, {
                "data": {
                    "id": 'nodo2',
                    "parent": 'net0',
                    "text": 'nodo2',
                    "type": "ellipse",
                    "color": "grey"
                }
            }, {
                "data": {
                    "id": 'nodo3',
                    "parent": 'net0',
                    "text": 'nodo3',
                    "type": "ellipse",
                    "color": "grey"
                }
            },
                {
                    "data": {
                        "id": 'net0',
                        "text": 'net0',
                        "meta": "net",
                        "type": "rectangle",
                        "color": "#D7D7D7"
                    }
                },
                {
                    "data": {
                        "id": 'net1',
                        "text": 'net1',
                        "meta": "net",
                        "type": "rectangle",
                        "color": "#D7D7D7"
                    }
                },
                {
                    "data": {
                        "id": 'netRouter',
                        "text": 'netRouter',
                        "meta": "net",
                        "type": "rectangle",
                        "color": "#D7D7D7"
                    }
                }
            ],  # nodes
            "edges": [{
                "data": {
                    "color": '#000',
                    "source": 'router',
                    "target": 'net1',
                    "id": "elerouternet1"
                }
            }, {
                "data": {
                    "color": '#000',
                    "source": 'router',
                    "target": 'net0',
                    "id": "elerouternet0"
                }
            }]  ## edges
        }

    def get(self):
        return self.element


class Node(object):
    def __init__(self):
        pass

    def get(self):
        pass

    def put(self, data):
        name = data.get("name")
        net = data.get("net")
        output = []
        parent = None
        id = None

        for item in data.get("elements").get("nodes"):
            if item.get("data").get("text") == name:
                return []
            if item.get("data").get("text") == net:
                net = item.get("data").get("id")
            if item.get("data").get("type") == "ellipse":
                id = item.get("data").get("id")
            if item.get("data").get("name") == net:
                parent = item.get("data").get("id")

        if parent is None:
            output.append({"group": 'nodes', "data": {"id": net, "text": net, "meta": "net",
                                                      "type": "rectangle", "color": "#D7D7D7"}})

        output.append({"group": 'nodes', "data": {"id": str(name), "text": str(name),
                                                  "type": "ellipse", "color": "grey", "parent": net},
                       "position": {"x": random.random() * 200, "y": random.random() * 200}})

        return output

    def delete(self, data):
        name = data.get("name")
        id = None
        ok = True
        net = None
        result = []
        for item in data.get("elements").get("nodes"):
            if item.get("data").get("text") == name and item.get("data").get("type") == "ellipse":
                id = item.get("data").get("id")
                result.append(id)
                net = item.get("data").get("parent")

        for other in data.get("elements").get("nodes"):
            if net == other.get("data").get("parent") and id != other.get("data").get("id"):
                ok = False
        if ok:
            result.append(net)
        return result


class Edge(object):
    def __init__(self):
        pass

    def put(self, data):
        net_edge = data.get("net_edge")
        router = data.get("router")
        rut = False
        net = False
        output = []
        for item in data.get("elements").get("nodes"):
            if item.get("data").get("text") == router and item.get("data").get("text") != net_edge:
                rut = True
            if item.get("data").get("parent") == net_edge:
                net = True
            if net and rut:
                break
        if net and rut:
            output = [{"group": "edges", "data": {"color": "#000",
                                                  "source": router,
                                                  "target": net_edge,
                                                  "id": "ele{}{}".format(router, net_edge)}}]

        return output

    def delete(self, data):
        net_edge = data.get("net_edge")
        router = data.get("router")
        idEdge = None

        for item in data.get("elements").get("edges"):
            if item.get("data").get("source") == router and item.get("data").get("target") == net_edge:
                idEdge = item.get("data").get("id")

        return idEdge


class Router(object):
    def __init__(self):
        pass

    def get(self):
        pass

    def put(self, data):
        name = data.get("name")
        net = data.get("net")
        output = []
        parent = None
        id = None

        for item in data.get("elements").get("nodes"):
            if item.get("data").get("text") == name:
                return []
            if item.get("data").get("text") == net:
                net = item.get("data").get("id")
            if item.get("data").get("type") == "rectangle":
                id = item.get("data").get("id")
            if item.get("data").get("name") == net:
                parent = item.get("data").get("id")
        if parent is None:
            output.append({"group": 'nodes', "data": {"id": str(net), "text": str(net), "meta": "net",
                                                      "type": "rectangle", "color": "#D7D7D7"},
                           "position": {"x": random.random() * 200, "y": random.random() * 200}})

        output.append({"group": 'nodes', "data": {"id": str(name), "text": str(name),
                                                  "type": "rectangle", "color": "grey", "parent": net},
                       "position": {"x": random.random() * 200, "y": random.random() * 200}})

        return output

    def delete(self, data):
        name = data.get("name")
        id = None
        ok = True
        net = None
        result = []
        for item in data.get("elements").get("nodes"):
            if item.get("data").get("text") == name and item.get("data").get("type") == "rectangle":
                id = item.get("data").get("id")
                result.append(id)
                net = item.get("data").get("parent")

        for other in data.get("elements").get("nodes"):
            if net == other.get("data").get("parent") and id != other.get("data").get("id"):
                ok = False
        if ok:
            result.append(net)

        return result
