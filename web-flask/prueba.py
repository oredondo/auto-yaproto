# !/usr/bin/env python
import logging
import os
from lib.lib_vagrant.vagrant_interface import Vagrant_Interface
from lib.lib_vagrant.vagrant_params import Vagrant_Params


class AutoVagrant(object):

    def __init__(self):
        os.chdir("/home/oscar/git/auto-yaproto/vagrant_getting_started")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.params = Vagrant_Params()
        self.interface = Vagrant_Interface()
        self.params.up = True
        logging.info("TEST log")
        self.logger.setLevel(logging.DEBUG)

    def run(self):
        self.logger.info("COMIENZA LA EJECUCION")
        return_code, stdout, stderr = \
            self.interface.run(self.params)

        return return_code, stdout, stderr


def main():
    pryeba = AutoVagrant()
    pryeba.run()


if __name__ == "__main__":
    main()
