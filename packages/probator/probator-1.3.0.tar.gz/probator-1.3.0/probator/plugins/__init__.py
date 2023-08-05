import json
import logging
from abc import abstractmethod, ABC
from collections import namedtuple
from enum import Enum

from flask import current_app, make_response
from flask_restful import Resource, reqparse
from flask_script import Command
from pkg_resources import EntryPoint

from probator import PROBATOR_PLUGINS
from probator.config import dbconfig
from probator.constants import HTTP, UNAUTH_MESSAGE
from probator.json_utils import ProbatorJSONEncoder

Worker = namedtuple('Worker', ('name', 'interval', 'entry_point'))


class CollectorType(Enum):
    GLOBAL = 1
    AWS_REGION = 2
    AWS_ACCOUNT = 3


class BasePlugin(object):
    options = ()
    dbconfig = dbconfig

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__module__)

    @property
    @abstractmethod
    def name(self):
        """Human friendly name of the Plugin"""


class BootstrappedBasePlugin(BasePlugin, ABC):
    bootstrapped = False

    @staticmethod
    def bootstrap():
        """Bootstrapping method for the plugin"""


class BaseAuditor(BootstrappedBasePlugin, ABC):
    start_delay = 30

    @classmethod
    def enabled(cls):
        return dbconfig.get('enabled', cls.ns, False)

    @property
    @abstractmethod
    def ns(self):
        """Namespace prefix for configuration settings"""

    @property
    @abstractmethod
    def interval(self):
        """Interval, in minutes, of how frequently the auditor executus"""

    @abstractmethod
    def run(self, *args, **kwargs):
        """Main worker entry point for the auditor"""


class BaseAuthPlugin(BasePlugin, ABC):
    # region Methods
    def bootstrap(self):
        """Default bootstrapping method, auth plugin's can do initialization tasks here, will only be run on startup
        of the API server.

        Returns:
            `None`
        """

    def _is_active_auth_system(self):
        """Return `True` if the current system is the active auth system, otherwise `False`

        Returns:
            `bool`
        """
        return current_app.active_auth_system == self.__class__.ns
    # endregion

    # region Properties
    @property
    @abstractmethod
    def ns(self):
        pass

    @property
    @abstractmethod
    def views(self):
        pass

    @property
    @abstractmethod
    def readonly(self):
        pass

    @property
    @abstractmethod
    def login(self):
        pass

    @property
    @abstractmethod
    def logout(self):
        pass
    # endregion


class BaseCollector(BasePlugin, ABC):
    @classmethod
    def enabled(cls):
        return dbconfig.get('enabled', cls.ns, False)

    @property
    @abstractmethod
    def interval(self): pass

    @property
    @abstractmethod
    def ns(self): pass

    @property
    @abstractmethod
    def type(self): pass

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError('Collector has not implemented the run method')


class BaseCommand(BasePlugin, Command, ABC):
    pass


class BaseNotifier(BasePlugin, ABC):
    @classmethod
    def enabled(cls):
        return dbconfig.get('enabled', cls.ns, False)

    @property
    @abstractmethod
    def ns(self): pass


class BaseScheduler(BasePlugin, ABC):
    def __init__(self):
        super().__init__()

        self.auditors = []
        self.collectors = {}

    @staticmethod
    def get_class_from_ep(entry_point):
        return EntryPoint(**entry_point).resolve()

    def load_plugins(self):
        """Refresh the list of available collectors and auditors

        Returns:
            `None`
        """
        for entry_point in PROBATOR_PLUGINS['probator.plugins.collectors']['plugins']:
            cls = entry_point.load()
            if cls.enabled():
                self.log.debug(f'Collector loaded: {cls.__name__} in module {cls.__module__}')
                self.collectors.setdefault(cls.type, []).append(Worker(
                    cls.name,
                    cls.interval,
                    {
                        'name': entry_point.name,
                        'module_name': entry_point.module_name,
                        'attrs': entry_point.attrs
                    }
                ))
            else:
                self.log.debug(f'Collector disabled: {cls.__name__} in module {cls.__module__}')

        for entry_point in PROBATOR_PLUGINS['probator.plugins.auditors']['plugins']:
            cls = entry_point.load()
            if cls.enabled():
                self.log.debug(f'Auditor loaded: {cls.__name__} in module {cls.__module__}')
                self.auditors.append(Worker(
                    cls.name,
                    cls.interval,
                    {
                        'name': entry_point.name,
                        'module_name': entry_point.module_name,
                        'attrs': entry_point.attrs
                    }
                ))
            else:
                self.log.debug(f'Auditor disabled: {cls.__name__} in module {cls.__module__}')

        collector_count = sum(len(x) for x in self.collectors.values())
        auditor_count = len(self.auditors)

        if collector_count + auditor_count == 0:
            raise Exception('No auditors or collectors loaded, aborting scheduler')

        self.log.info(f'Scheduler loaded {collector_count} collectors and {auditor_count} auditors')

    @abstractmethod
    def execute_scheduler(self):
        """Entry point to execute the scheduler

        The scheduler should execute as a daemon, which will ensure that the worker threads will get scheduled
        until the process is stopped"""

    @abstractmethod
    def execute_worker(self):
        """Main worker execution entry point

        Each execution of the worker thread should handle a single request from the scheduler and exit, to allow for
        manual/stepped execution of the jobs. The command line worker utility will handle running schedulers in daemon
        mode, unless the user explicitly requests single a execution"""


class BaseView(BasePlugin, Resource):
    enabled = True
    URLS = []
    name = 'view'

    def __init__(self):
        super().__init__()
        self.reqparse = reqparse.RequestParser()

        # Monkey patch parse_args to return a munch so we can use object notation instead of slices/keys
        self.reqparse._org_parse_args = self.reqparse.parse_args
        self.reqparse.parse_args = lambda *args, **kwargs: self.reqparse._org_parse_args(*args, **kwargs)

    @staticmethod
    def make_response(data, code=HTTP.OK, content_type='application/json'):
        if isinstance(data, str):
            data = {'message': data}

        else:
            if 'message' not in data:
                data['message'] = None

        resp = make_response(json.dumps(data, sort_keys=False, cls=ProbatorJSONEncoder), code)
        resp.mimetype = content_type

        return resp

    @staticmethod
    def make_unauth_response():
        return BaseView.make_response(UNAUTH_MESSAGE, HTTP.UNAUTHORIZED)
