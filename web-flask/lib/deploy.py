from lib.config import Config
from lib.generateVagrantFile import GenerateVagrantFile
import os
import subprocess
import shlex

process = None

class Deploy(object):

    def __init__(self, data=None):
        self.data = data

    def run(self):

        # conf = Config(data=self.data).get()
        vagrantdir = os.getcwd().replace("web-flask", "vagrant_getting_started")
        vagrantfile_path = os.path.join(vagrantdir,
                                        "Vagrantfile")

        # GenerateVagrantFile(template_path="Vagrantfile", vagrantfile_path=vagrantfile_path, config=conf)

        os.chdir(vagrantdir)
        cmd = ['vagrant', 'up']
        return self.run_command(cmd)
        # proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #
        # o, e = proc.communicate()
        #
        # while True:
        #     output = proc.stdout.readline()
        #     if output == '' and proc.poll() is not None:
        #         break
        #     if output:
        #         print(output.strip())
        # rc = proc.poll()
        # # print('Output: ' + o.decode('ascii'))
        # # print('Error: ' + e.decode('ascii'))
        # # print('code: ' + str(proc.returncode))

    def run_command(self, command):
        global process
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return process
    # while True:
    #     output = process.stdout.readline()
    #     if output == '' and process.poll() is not None:
    #         break
    #     if output:
    #         print(output.strip())
    # rc = process.poll()

    def stream(self):
        def generate():
            global process
            retcode = process.poll()  # returns None while subprocess is running
            line = process.stdout.readline()
            yield line
            if (retcode is not None):
                return

        return generate()