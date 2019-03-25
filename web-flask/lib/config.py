class Config(object):

    def __init__(self, data=None):
        self.__parse(data)

    def __parse(self, data):

        for item in data.get("elements").get("nodes"):
            if  # TODO: parsear para crear un diccionario con info para generar el vVagrant file
