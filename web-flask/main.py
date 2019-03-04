from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
from lib.actions import Style, Elements
app = Flask(__name__, static_folder='statics')
api = Api(app)


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
