"""

This is the conductor which controls everything

"""

import glob
import imp
from commandcontrol.malware import *
from commandcontrol.apt import *
from protocols.servers import *
from protocols.clients import *
from datatypes import *


class Conductor:

    def __init__(self):
        # Create dictionaries of supported modules
        # empty until stuff loaded into them
        self.client_protocols = {}
        self.server_protocols = {}
        self.datatypes = {}
        self.actor_modules = {}

    def load_client_protocols(self, command_line_object):
        for name in glob.glob('protocols/clients/*.py'):
            if name.endswith(".py") and ("__init__" not in name):
                loaded_client_proto = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
                self.client_protocols[name] = loaded_client_proto.Client(command_line_object)
        return

    def load_server_protocols(self, command_line_object):
        for name in glob.glob('protocols/servers/*.py'):
            if name.endswith(".py") and ("__init__" not in name):
                loaded_server_proto = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
                self.server_protocols[name] = loaded_server_proto.Server(command_line_object)

    def load_datatypes(self, command_line_object):
        for name in glob.glob('datatypes/*.py'):
            if name.endswith(".py") and ("__init__" not in name):
                loaded_datatypes = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
                self.datatypes[name] = loaded_datatypes.Datatype(command_line_object)

    def load_actors(self, command_line_object):
        for name in glob.glob('commandcontrol/malware/*.py'):
            if name.endswith(".py") and ("__init__" not in name):
                loaded_actors = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
                self.actor_modules[name] = loaded_actors.Actor(command_line_object)
        for name in glob.glob('commandcontrol/apt/*.py'):
            if name.endswith(".py") and ("__init__" not in name):
                loaded_actors = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
                self.actor_modules[name] = loaded_actors.Actor(command_line_object)
