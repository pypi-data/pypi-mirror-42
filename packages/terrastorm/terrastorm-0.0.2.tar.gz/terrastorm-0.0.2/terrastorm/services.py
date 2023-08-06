import os
import shutil

from glob import glob
from terrastorm.settings import data
from cookiecutter.vcs import clone
from cookiecutter.main import cookiecutter
from pebble import ThreadPool
from python_terraform import Terraform


class PathNotExistsException(Exception): pass
class ProjectExistsException(Exception): pass
class ModuleExistsException(Exception): pass
class EnvironmentExistsException(Exception): pass
class ServiceExistsException(Exception): pass


class TerrastormService:
    conf = None
    default_settings = """
base:
    environments: {base}/environments
    modules: {base}/modules
templates:
    project: https://github.com/williamtsoi1/terraservices-example.git
    module: https://github.com/rosscdh/cookiecutter-terramodule.git
    service: https://github.com/rosscdh/cookiecutter-terraservice.git
aws:
    region: eu-west-1
    """
    def __init__(self, conf):
        self.conf = conf

    def environments(self):
        """
        List environments based on the configued environments path location subdirectories
        """
        try:
            if not os.path.exists(self.conf.base.environments):
                raise PathNotExistsException(self.conf.base.environments)
            return [os.path.basename(f.path) for f in os.scandir(self.conf.base.environments) if f.is_dir() ]
        except PathNotExistsException:
            return ['No Environment Defined, Please run `terrastorm setup` or `terrastorm create environment development`']

    def service_paths(self, environment: str):
        services_path = os.path.join(self.conf.base.environments, environment)
        if not os.path.exists(services_path):
            raise PathNotExistsException( services_path)
        return [f.path for f in os.scandir(services_path) if f.is_dir() ]

    def services(self, environment: str):
        return [os.path.basename(f) for f in self.service_paths(environment=environment)]

    def create(self, object_type: str, name: str, **kwargs):
        return getattr(self, 'create_{}'.format(object_type))(name=name, **kwargs)

    def initialize_project(self, path: str):
        """
        Create a new project at a specific path
        """
        output_dir = path
        if os.path.exists(output_dir):
            raise ProjectExistsException(output_dir)

        template_config = self.default_settings.format(base=output_dir)

        # clone the base template project to specified path
        repo_dir = clone(self.conf.templates.project,
                         checkout=None,
                         clone_to_dir='/tmp/',
                         no_input=True)
        # move from tmp to the target dir
        shutil.move(repo_dir, output_dir)

        return template_config

    def create_environment(self, name: str, **kwargs):
        """
        Copy one of the other environments and give it a new name
        """
        output_dir = os.path.join(self.conf.base.environments, name)
        if os.path.exists(output_dir):
            raise EnvironmentExistsException(output_dir)
        return output_dir

    def create_module(self, name: str, **kwargs):
        """
        Create a new Terraservice Module
        """
        output_dir = os.path.join(self.conf.base.modules, name)
        if os.path.exists(output_dir):
            raise ModuleExistsException(output_dir)

        cookie_template = cookiecutter(self.conf.templates.module,
                                      extra_context={'module_name': name},
                                      output_dir=self.conf.base.modules,
                                      no_input=True,
                                      overwrite_if_exists=False)

        return output_dir if cookie_template else False

    def create_layer(self, name: str, **kwargs):
        """
        Create a new Terraservice Layer
        """
        output_dir = os.path.join(self.conf.base.layers, name)
        if os.path.exists(output_dir):
            raise ModuleExistsException(output_dir)

        cookie_template = cookiecutter(self.conf.templates.layer,
                                      extra_context={'module_name': name},
                                      output_dir=self.conf.base.layers,
                                      no_input=True,
                                      overwrite_if_exists=False)

        return output_dir if cookie_template else False

    def create_service(self, name: str, **kwargs):
        """
        Create a new Service
        """
        environment = kwargs.get('environment', 'development')
        output_dir = os.path.join(self.conf.base.environments, environment)

        if os.path.exists(os.path.join(output_dir, name)):
            raise ServiceExistsException(os.path.join(output_dir, name))

        cookie_template = cookiecutter(self.conf.templates.service,
                                      extra_context={'service_name': name,
                                                     'environment': environment,
                                                     'region': self.conf.aws.region},
                                      output_dir=output_dir,
                                      no_input=True,
                                      overwrite_if_exists=False)

        return os.path.join(output_dir, name) if cookie_template else False

    def run(self, command: str, environment: str, services: set):
        """
        """
        args = []
        kwargs = {}
        known_services = set(self.services(environment=environment))
        known_service_paths = self.service_paths(environment=environment)

        if not services or services == ['all']:
            target_services = [service for service in known_services]
        else:
            target_services = [service for service in services & known_services]
        with ThreadPool(max_workers=5) as pool:
            for service in target_services:
                for path in known_service_paths:
                    if service in path:
                        print('*****'*15)
                        print('Starting: {} @ {}'.format(service, path))
                        print('*****'*15)
                        future = pool.schedule(process_command, args=[path, command, args, kwargs])
                        #import pdb;pdb.set_trace()
                        # return_code, stdout, stderr = future.result()
                        yield future
                        # tf = Terraform(working_dir=path)
                        # yield tf.cmd(command, *args, **kwargs)


def process_command(path: str, command: str, *args: list, **kwargs: dict):
    tf = Terraform(working_dir=path)
    return_code, stdout, stderr = tf.cmd(command)
    return return_code, stdout, stderr