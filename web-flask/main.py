from flask import Flask, request
from flask import render_template
from flask_restful import Resource, Api, reqparse
from lib.actions import Style, Elements, AddNode
app = Flask(__name__, static_folder='statics')
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('hola')


@app.route("/")
def hello():
    return render_template("index.html")


class ViewStyle(Resource):

    @staticmethod
    def get():
        out = Style().get()
        return out


api.add_resource(ViewStyle, '/api/style')


class ViewElements(Resource):

    @staticmethod
    def get():
        out = Elements().get()
        return out


api.add_resource(ViewElements, '/api/elements')


class ViewAddNode(Resource):

    @staticmethod
    def get():
        out = AddNode().get()
        return out

    def put(self):
        data = AddNode().put(request.json)
        return data, 200


api.add_resource(ViewAddNode, '/api/addnode')

if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=True, passthrough_errors=True)