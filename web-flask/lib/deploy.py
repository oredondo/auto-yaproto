from lib.config import Config
from lib.generateVagrantFile import GenerateVagrantFile
import os
import subprocess
import json


class Deploy(object):

    def __init__(self, data=None):
        self.data = json.loads(data)
        self.cmd = ['vagrant']
        self.vagrantdir = os.getcwd().replace("web-flask", "")
        os.chdir(self.vagrantdir)
        self.pope = None

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
        port = self.data.get("port")
        command = "sudo java -Djava.library.path=/vagrant/data/lib -jar " \
                  "/vagrant/data/builds/ProtocoloRIPv2.jar 0.0.0.0:{} &".format(port)
        self.cmd.extend(["ssh", name, "-c", command])
        return self._run_command()

    def run_ospf(self):
        name = self.data.get("name")
        local_ips = ','.join(self.data.get("local_ips"))
        all_ips = ','.join(self.data.get("all_ips"))
        command = "sudo java -Djava.library.path=/vagrant/data/lib " \
                  "-jar /vagrant/data/builds/ProtocoloOSPFv2.jar {} {}".format(local_ips, all_ips)
        self.cmd.extend(["ssh", name, "-c", command])
        return self._run_command()

    def _run_command(self):
        self.pope = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     universal_newlines=True)
        return self.pope

    def stream(self):
        def generate():
            for item in iter(self.pope.stdout.readline, ""):
                yield str("<p style='color:#f8f9ff'; >" + item + "</p>")
        return generate()
