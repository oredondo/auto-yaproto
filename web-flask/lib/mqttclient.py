import paho.mqtt.client as mqtt
import threading


class MqttClient(object):

    def __init__(self, lista, port, topic):
        self.lista = lista
        self.port = port
        self.topic = topic
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def on_message(self, mosq, obj, msg):
        self.lista.put("<p style='color:#f8f9ff'; >{} {}</p>".format(
            str(msg.topic), str(msg.payload.decode("utf-8"))))

    def run(self):
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.connect("127.0.0.1", self.port, 60)
        self.mqttc.subscribe(self.topic, 0)
        self.mqttc.loop_forever()


class StreamMqtt(object):

    def stream(self, lista):
        def generate(lista):
            for job in iter(lista.get, None):
                yield job

        return generate(lista)
