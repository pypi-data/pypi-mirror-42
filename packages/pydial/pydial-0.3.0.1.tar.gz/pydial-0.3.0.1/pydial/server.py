from eulfedora.server import Repository
from eulfedora.api import API_A_LITE
import os
import json


class DialRepository(Repository):

    def __init__(self, configuration_file=None):
        if configuration_file is None:
            configuration_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conf', 'services.json')
        with open(configuration_file) as sh:
            self.services = json.load(sh)
        if 'fedora' not in self.services:
            raise KeyError("'fedora' section is missing from configuration file")
        for k in [k for k in ['url', 'username', 'password'] if k not in self.services['fedora']]:
            raise KeyError("'{0}' parameter are required into 'fedora' configuration section".format(k))

        credentials = {
            'username': self.services['fedora']['username'],
            'password': self.services['fedora']['password'],
        }
        api_a = API_A_LITE(self.services['fedora']['url'], **credentials)
        api_a.describeRepository()  # this operation generate an error if connection failed.
        del api_a
        super(DialRepository, self).__init__(self.services['fedora']['url'], **credentials)
