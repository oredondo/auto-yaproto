from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
from lib.actions import Style, Elements, Node, Edge, Router
from lib.deploy import Deploy
from lib.aux_actions import GetIps, LoadSave, Puertos
from flask import stream_with_context, request, Response
from lib.mqttclient import MqttClient, StreamMqtt
from lib.config import Config
import queue
import json

app = Flask(__name__, static_folder='statics')
api = Api(app)


@app.route("/")
def index():
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
        return out, 200

    def put(self):
        puerto = Puertos(request.json)
        data = Node().put(request.json, puerto.get(), puerto.get())
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
        puerto = Puertos(request.json)
        data = Router().put(request.json, puerto.get(), puerto.get())
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


class ViewGetIps(Resource):

    def put(self):
        geting = GetIps(request.data)
        out = geting.get()
        return out, 200


api.add_resource(ViewGetIps, '/api/getips')


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
        return 200

api.add_resource(ViewRunRip, '/api/runrip')

class ViewMqttRip(Resource):

    def put(self):
        data = json.loads(request.data)
        if data.get("topic"):
            cola = queue.Queue()
            aux = StreamMqtt()
            MqttClient(cola, int(data.get("port")), data.get("topic"), data.get("mapa") )
            rows = aux.stream(cola)
            return Response(stream_with_context(rows))
        else:
            return 200

api.add_resource(ViewMqttRip, '/api/mqttrip')


class ViewRunOspf(Resource):

    def put(self):
        out = Deploy(request.data)
        out.run_ospf()
        rows = out.stream()
        return Response(stream_with_context(rows))


api.add_resource(ViewRunOspf, '/api/runospf')


class ViewSave(Resource):

    def put(self):
        data = LoadSave(request.data).save()
        return data, 200


api.add_resource(ViewSave, '/api/save')


class ViewLoad(Resource):

    def get(self):
        data = LoadSave({}).list_json()
        return data, 200

    def put(self):
        data = LoadSave(request.data).load()
        return data, 200


api.add_resource(ViewLoad, '/api/load')

class ViewInfoNet(Resource):


    def put(self):
        data = json.loads(request.data)
        conf = Config(data=data).get()
        return conf, 200


api.add_resource(ViewInfoNet, '/api/infonet')


@app.route('/logrip&<name>&<port>&<topic>')
def landing_page(name, port, topic):
    if topic == "all":
        topic = "#"
    return render_template("logejecution.html", name=name,
                           port=port,
                           topic=topic)


@app.route('/logospf&<name>&<local_ips>&<all_ips>')
def landing_page_ospf(name, local_ips, all_ips):
    return render_template("logejecutionOspf.html", name=name,
                           local_ips=local_ips, all_ips=all_ips)


if __name__ == '__main__':
    app.run(debug=True, use_debugger=True,
            use_reloader=True, passthrough_errors=True, threaded=True)
