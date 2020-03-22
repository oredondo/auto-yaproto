from lib.config import Config
from lib.generateVagrantFile import GenerateVagrantFile
import os
import subprocess
import json

pope = None

class Deploy(object):

    def __init__(self, data=None):
        self.data = json.loads(data)
        self.cmd = ['vagrant']
        self.vagrantdir = os.getcwd().replace("web-flask", "vagrant_getting_started")
        os.chdir(self.vagrantdir)

    def run(self):
        conf = Config(data=self.data).get()
        vagrantfile_path = os.path.join(self.vagrantdir,
                                        "Vagrantfile")
        GenerateVagrantFile(template_path="Vagrantfile", vagrantfile_path=vagrantfile_path, config=conf)

        self.cmd.append('up')
        return self._run_command()

    def destroy(self):
        self.cmd.extend(["destroy", "-f"])
        return self._run_command()

    def run_rip(self):
        name = self.data.get("name")
        command = "sudo java -Djava.library.path=/vagrant/data/yaproto/lib -jar /vagrant/data/builds/ProtocoloRIPv2.jar"
        self.cmd.extend(["ssh", name, "-c", command])
        return self._run_command()

    def _run_command(self):
        global pope
        pope = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                universal_newlines=True)
        return pope

    def stream(self):
        def generate():
            for item in iter(pope.stdout.readline, ""):
                yield str("<p style='color:#f8f9ff'; >" + item + "</p>")

        return generate()

        # sleep(1)
