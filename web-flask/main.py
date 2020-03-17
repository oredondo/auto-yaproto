from flask import Flask, request
from flask import render_template
from flask_restful import Resource, Api, reqparse
from lib.actions import Style, Elements, Node, Edge, Router
from lib.deploy import Deploy
from flask import stream_with_context, request, Response

app = Flask(__name__, static_folder='statics')
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('hola')


class Puertos(object):

    def __init__(self):
        self.port = 4203

    def get(self):
        self.port = self.port + 1
        return self.port


puerto = Puertos()


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


class ViewNode(Resource):

    @staticmethod
    def get():
        out = Node().get()
        return out

    def put(self):
        data = Node().put(request.json, puerto.get())
        return data, 200

    def delete(self):
        data = Node().delete(request.json)
        return data, 200


api.add_resource(ViewNode, '/api/node')


class ViewEdge(Resource):

    def put(self):
        data = Edge().put(request.json)
        return data, 200

    def delete(self):
        data = Edge().delete(request.json)
        return data, 200


api.add_resource(ViewEdge, '/api/edge')


class ViewRouter(Resource):

    @staticmethod
    def get():
        out = Router().get()
        return out

    def put(self):
        data = Router().put(request.json, puerto.get())
        return data, 200

    def delete(self):
        data = Router().delete(request.json)
        return data, 200


api.add_resource(ViewRouter, '/api/router')


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.disable_buffering()
    return rv


class ViewDeploy(Resource):

    def put(self):
        out = Deploy(request.data)
        out.run()
        rows = out.stream()
        return Response(stream_with_context(rows))


api.add_resource(ViewDeploy, '/api/deploy')


class ViewDestroy(Resource):

    def put(self):
        out = Deploy(request.data)
        out.destroy()
        rows = out.stream()
        return Response(stream_with_context(rows))


api.add_resource(ViewDestroy, '/api/destroy')


class ViewRunRip(Resource):

    def put(self):
        out = Deploy(request.data)
        out.run_rip()
        rows = out.stream()
        return Response(stream_with_context(rows))


api.add_resource(ViewRunRip, '/api/runrip')


@app.route('/logrip<name>')
def landing_page(name):
    return render_template("logejecution.html", name=name)


if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=True, passthrough_errors=True)
