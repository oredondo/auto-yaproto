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
                }
            ],  # nodes
            "edges": [{
                "data": {
                    "color": '#000',
                    "source": 'router',
                    "target": 'nodo1'
                }
            }, {
                "data": {
                    "color": '#000',
                    "source": 'router',
                    "target": 'nodo2'
                }
            }, {
                "data": {
                    "color": '#000',
                    "source": 'router',
                    "target": 'nodo3'
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
            output.append({"group": 'nodes', "data": {"id": net, "text": net, "meta":"net",
                                                      "type": "rectangle", "color": "#D7D7D7"}})

        output.append({"group": 'nodes', "data": {"id": str(name), "text": str(name),
                                                  "type": "ellipse", "color": "grey", "parent": net},
                       "position": {"x": random.random() * 200, "y": random.random() * 200}})

        return output

    def delete(self, data):
        name = data.get("name")
        id = None
        for item in data.get("elements").get("nodes"):
            if item.get("data").get("text") == name and item.get("data").get("type") == "ellipse":
                id = item.get("data").get("id")
        return id


class Edge(object):
    def __init__(self):
        pass

    def put(self, data):
        node = data.get("node")
        router = data.get("router")
        output = []
        id = []
        for item in data.get("elements").get("nodes"):
            if item.get("data").get("text") == node or \
                    item.get("data").get("text") == router:
                id.append(str(item.get("data").get("id")))
        try:
            output.append({"group": "edges", "data": {"color": "#000",
                                                      "source": id[0],
                                                      "target": id[1],
                                                      "id": "ele"+id[0]+id[1]}})
        except ValueError:
            pass

        return output

    def delete(self, data):
        name = data.get("name")
        id = None
        idEdge = None
        for item in data.get("elements").get("nodes"):
            if item.get("data").get("text") == name:
                id = str(item.get("data").get("id"))

        for item in data.get("elements").get("edges"):
            if item.get("data").get("source") == id or item.get("data").get("target") == id:
                idEdge = item.get("data").get("id")
        return idEdge


class Router(object):
    def __init__(self):
        pass

    def get(self):
        pass

    def put(self, data):
        name = data.get("name")
        output = []
        parent = None
        id = None

        for item in data.get("elements").get("nodes"):
            if item.get("data").get("text") == name:
                return []
            if item.get("data").get("type") == "rectangle":
                id = item.get("data").get("id")
        output.append({"group": 'nodes', "data": {"id": str(name), "text": str(name),
                                                  "type": "rectangle", "color": "grey"},

                       "position": {"x": random.random() * 200, "y": random.random() * 200}})

        return output

    def delete(self, data):
        name = data.get("name")
        id = None
        for item in data.get("elements").get("nodes"):
            if item.get("data").get("text") == name and item.get("data").get("type") == "rectangle":
                id = item.get("data").get("id")
                try:
                    id = int(id)
                except ValueError:
                    pass
        return id