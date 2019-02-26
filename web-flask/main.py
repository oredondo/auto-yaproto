from flask import Flask
from flask import render_template
from flask_restful import Resource, Api

app = Flask(__name__, static_folder='statics')
api = Api(app)

@app.route("/")
def hello():
    return render_template("index.html")

class Style(Resource):
    def get(self):
        return [{
        "selector": 'node',
        "style": {
          'width': 60,
          'height': 60,
          "shape": 'data(type)',
          'content': 'data(text)',
          'text-valign': 'center',
          'color': 'white',
          'text-outline-width': 2,
          'text-outline-color': '#222'
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

api.add_resource(Style, '/api/style')



class Elements(Resource):
    def get(self):
        return { ##selectable: false,
                    ##grabbable: false,
                    "nodes": [{
                      "data": {
                        "id": "0",
                        "text": 'router',
                        "type": 'rectangle'
                      }
                    }, {
                      "data": {
                        "id": '1',
                        "text": 'nodo1',
                        "type":  "ellipse"
                      }
                    }, {
                      "data": {
                        "id": '2',
                        "text": 'nodo2',
                        "type":  "ellipse"
                      }
                    }, {
                      "data": {
                        "id": '3',
                        "text": 'nodo3',
                        "type":  "ellipse"
                      }
                    }], # nodes
                    "edges": [{
                        "data": {
                          "color": '#000',
                          "source": '0',
                          "target": '1'
                        }
                      }, {
                        "data": {
                          "color": '#000',
                          "source": '1',
                          "target": '2'
                        }
                      }, {
                        "data": {
                          "color": '#000',
                          "source": '2',
                          "target": '3'
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
                      }, {
                        "data": {
                          "color": '#000',
                          "source": '0',
                          "target": '3'
                        }
                      }] ## edges
                  }
api.add_resource(Elements, '/api/elements')
