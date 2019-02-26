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
