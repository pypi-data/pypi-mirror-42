import socket
from google.cloud import logging
from google.cloud.logging.resource import Resource


class Logger(object):

    def create_logger(self, project_id):
        log_client = logging.Client()
        log_name = "appengine.googleapis.com%2Fgae_app"
        logger = log_client.logger(log_name.format(project_id))
        return logger

    def get_instance(selfself):
        gce_name = socket.gethostname()
        return gce_name

    def __init__(self, run_id, project_id, module_id=None, version_id=None, function_name=None, resource_type='global'):
        self.trace_id = run_id
        self.project_id = project_id
        self.module_id = module_id
        self.version_id = version_id
        self.resource_type = resource_type
        self.function_name = function_name
        # Check resource_type
        if self.resource_type == 'gae_app':
            self.res = Resource(type=self.resource_type, labels={
                "project_id": self.project_id,
                "module_id": self.module_id,
                "version_id": self.version_id
            })
        elif self.resource_type == 'cloud_function':
            self.res = Resource(type=self.resource_type, labels={
                "function_name": self.function_name,
                "project_id": self.project_id
            })
        elif self.resource_type == 'gce_instance':
            self.instance_id = self.get_instance()
            self.res = Resource(type=self.resource_type, labels={
                "instance_id": self.instance_id,
                "project_id": self.project_id
            })
        else:
            self.res = Resource(type='global', labels={"project_id": self.project_id})
        self.logger = self.create_logger(self.project_id)

    def info(self, message):
        self.logger.log_struct({'message': message, 'trace_id': self.trace_id}, resource=self.res, severity='INFO')

    def warning(self, message):
        self.logger.log_struct({'message': message, 'trace_id': self.trace_id}, resource=self.res, severity='WARNING')

    def error(self, message):
        self.logger.log_struct({'message': message, 'trace_id': self.trace_id}, resource=self.res, severity='ERROR')

    def critical(self, message):
        self.logger.log_struct({'message': message, 'trace_id': self.trace_id}, resource=self.res, severity='CRITICAL')

    def debug(self, message):
        self.logger.log_struct({'message': message, 'trace_id': self.trace_id}, resource=self.res, severity='DEBUG')

