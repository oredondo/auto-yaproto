from lib.config import Config
from lib.generateVagrantFile import GenerateVagrantFile
import os
import subprocess
import logging
from lib.lib_vagrant.vagrant_params import Vagrant_Params
from lib.lib_vagrant.vagrant_interface import Vagrant_Interface

process = None

class Deploy(object):

    def __init__(self, data=None):
        self.data = data
        self.params = Vagrant_Params()
        self.interface = Vagrant_Interface()

        logging.info("TEST log")
        self.logger.setLevel(logging.DEBUG)

    def run(self):

        conf = Config(data=self.data).get()
        vagrantdir = os.getcwd().replace("web-flask", "vagrant_getting_started")
        vagrantfile_path = os.path.join(vagrantdir,
                                        "Vagrantfile")

        GenerateVagrantFile(template_path="Vagrantfile", vagrantfile_path=vagrantfile_path, config=conf)
        os.chdir(vagrantdir)
        self.params.destroy = True
        cmd = ['vagrant', 'up']
        return self.run_command(cmd)

    def run_command(self, command):
        global process
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return process


    def stream(self):
        def generate():
            global process
            retcode = process.poll()  # returns None while subprocess is running
            line = process.stdout.readline()
            print(line)
            yield line
            if (retcode is not None):
                return
        return generate()

