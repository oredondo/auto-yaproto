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
        name = data.get
        net = data.get
        output = []
        parent = None
        id = None

        for item in data.get.get:
            if item.get.get == name:
                return []
            if item.get.get == net:
                net = item.get.get
            if item.get.get == "ellipse":
                id = item.get.get
            if item.get.get == net:
                parent = item.get.get

        if parent is None:
            output.append({"group": 'nodes', "data": {"id": net, "text": net, "meta":"net",
                                                      "type": "rectangle", "color": "#D7D7D7"}})

        output.append({"group": 'nodes', "data": {"id": str(name), "text": str(name),
                                                  "type": "ellipse", "color": "grey", "parent": net},
                       "position": {"x": random.random() * 200, "y": random.random() * 200}})

        return output

    def delete(self, data):
        name = data.get
        id = None
        for item in data.get.get:
            if item.get.get == name and item.get.get == "ellipse":
                id = item.get.get
        return id


class Edge(object):
    def __init__(self):
        pass

    def put(self, data):
        node = data.get
        router = data.get
        output = []
        id = []
        for item in data.get.get:
            if item.get.get == node or \
                    item.get.get == router:
                id.append(str(item.get.get))
        try:
            output.append({"group": "edges", "data": {"color": "#000",
                                                      "source": id[0],
                                                      "target": id[1],
                                                      "id": "ele"+id[0]+id[1]}})
        except ValueError:
            pass

        return output

    def delete(self, data):
        name = data.get
        id = None
        idEdge = None
        for item in data.get.get:
            if item.get.get == name:
                id = str(item.get.get)

        for item in data.get.get:
            if item.get.get == id or item.get.get == id:
                idEdge = item.get.get
        return idEdge


class Router(object):
    def __init__(self):
        pass

    def get(self):
        pass

    def put(self, data):
        name = data.get
        output = []
        parent = None
        id = None

        for item in data.get.get:
            if item.get.get == name:
                return []
            if item.get.get == "rectangle":
                id = item.get.get
        output.append({"group": 'nodes', "data": {"id": str(name), "text": str(name),
                                                  "type": "rectangle", "color": "grey"},

                       "position": {"x": random.random() * 200, "y": random.random() * 200}})

        return output

    def delete(self, data):
        name = data.get
        id = None
        for item in data.get.get:
            if item.get.get == name and item.get.get == "rectangle":
                id = item.get.get
                try:
                    id = int(id)
                except ValueError:
                    pass
        return id