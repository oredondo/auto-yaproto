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
                    "id": "0",
                    "text": 'router',
                    "type": 'rectangle',
                    "color": "grey"
                }
            }, {
                "data": {
                    "id": '1',
                    "text": 'nodo1',
                    "parent": 'a',
                    "type": "ellipse",
                    "color": "grey"
                }
            }, {
                "data": {
                    "id": '2',
                    "parent": 'b',
                    "text": 'nodo2',
                    "type": "ellipse",
                    "color": "grey"
                }
            }, {
                "data": {
                    "id": '3',
                    "parent": 'b',
                    "text": 'nodo3',
                    "type": "ellipse",
                    "color": "grey"
                }
            },
                {
                    "data": {
                        "id": 'b',
                        "text": 'net0',
                        "type": "rectangle",
                        "color": "#D7D7D7"
                    }
                },
                {
                    "data": {
                        "id": 'a',
                        "text": 'net1',
                        "type": "rectangle",
                        "color": "#D7D7D7"
                    }
                }
            ],  # nodes
            "edges": [{
                "data": {
                    "color": '#000',
                    "source": '0',
                    "target": '1'
                }
            }, {
                "data": {
                    "color": '#000',
                    "source": '0',
                    "target": '2'
                }
            }, {
                "data": {
                    "color": '#000',
                    "source": '0',
                    "target": '3'
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
        for item in data.get("elements").get("nodes"):
            if item.get("data").get("type") == "ellipse":
                id = item.get("data").get("id")
        id = int(id)
        return {"group": 'nodes', "data": {"id": str(id + 1), "text": str(name),
                                           "type": "ellipse", "color": "grey", "parent": net},
                "position": {"x": random.random()*200,
                             "y": random.random()*200}}

    def delete(self, data):
        for item in data.get("elements").get("nodes"):
            if item.get("data").get("type") == "ellipse":
                id = item.get("data").get("id")
        id = int(id)
        return 3
