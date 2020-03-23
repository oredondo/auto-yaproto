import os

import jinja2


class GenerateVagrantFile(object):

    def __init__(self, template_path='Vagrantfile.j2', vagrantfile_path='Vagrantfile', config=None):
        self.__generate_vagrantfile(template_path, vagrantfile_path, config)

    def __load_template(self, template_path):
        return (jinja2.Environment(autoescape=True,
                                   loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
                .get_template(template_path))

    def __generate_vagrantfile(self, template_path, vagrantfile_path, config):
        file = open(vagrantfile_path, 'w+')
        file.write(self.__load_template(template_path).render(config))
        file.close()
