"""Ansible params manage ansible parameters"""
import logging


class Vagrant_Params(dict):
    """Manage wrapper possible parameters"""

    def __init__(self):
        """Init wrapper parameters"""
        self.__dict__ = self._define_params()
        super(Vagrant_Params, self).__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug("Params configured: %s", self.__dict__)

    def _define_params(self):
        """Define a dictionary with all posible parameters"""
        params = {}
        params["up"] = False
        params["destroy"] = False
        params["ssh"] = None
        params["command"] = None
        params["status"] = False
        return params

    def __deepcopy__(self, memo):
        """Do a deepcopy of a AnsibleParams object"""
        # Esto solo funciona para un nivel de diccionario
        ansibleparams_copy = Vagrant_Params()
        for key in self.__dict__:
            ansibleparams_copy.__dict__[key] = self.__dict__[key]
        return ansibleparams_copy

    def get_cmd_params(self, executable):
        """Converts parameters to a list"""
        cmd_params = []

        # Incluimos el shell command a ejecutar
        cmd_params.append(executable)

        if self.up is True:
            cmd_params.append("up")

        if self.destroy is True:
            cmd_params.append("destroy")
            cmd_params.extend(["-f"])

        if self.command is not None and self.ssh is not None:
            cmd_params.append("ssh " + self.ssh)
            cmd_params.extend(
                ["-c", self.command])

        self._logger.debug("List of parameters generated: %s", cmd_params)
        return cmd_params
