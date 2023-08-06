import requests
import os

from itertools import chain
from threading import Thread
from collections import OrderedDict
from abc import ABCMeta, abstractmethod
from requests.exceptions import RequestException

from .object import Sendable, Receivable
from .exception import SDKException

from validation.validator import ValidatorFactory


class ActionFailedException(Exception):
    pass


class CouldNotSendRequest(Exception):
    pass


class UnexpectedOutcome(Exception):
    pass


class EventHook(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplemented


class Factory(object):
    @staticmethod
    @abstractmethod
    def get_actions():
        """
        :return: a dictionary of {'action name': action class}
        """
        raise NotImplemented

    def __init__(self, api_context, cache=None, presend_hooks=None, success_hooks=None, failure_hooks=None):
        self.api_context = api_context
        self.cache = cache
        self.presend_hooks = OrderedDict() if presend_hooks is None else presend_hooks
        self.success_hooks = OrderedDict() if success_hooks is None else success_hooks
        self.failure_hooks = OrderedDict() if failure_hooks is None else failure_hooks

    def make(self, action):
        result = self.__class__.get_actions()[action](self.api_context)
        result.presend_hooks = OrderedDict(chain(self.presend_hooks.items(),
                                                 result.__class__.get_presend_hooks().items()))
        result.success_hooks = OrderedDict(chain(self.success_hooks.items(),
                                                 result.__class__.get_success_hooks().items()))
        result.failure_hooks = OrderedDict(chain(self.failure_hooks.items(),
                                                 result.__class__.get_failure_hooks().items()))
        return result


class UnknownContentType(Exception):
    pass


class Request(object):
    content_types = {'json': 'application/json',
                     'form': 'application/x-www-form-urlencoded'}

    accept = {'json': 'application/json',
              'xml': 'application/xml'}

    def __init__(self, verb, url, query_params, body_params, headers, content_type='json', accept='json'):
        self.verb = verb
        self.url = url
        self.body_params = body_params
        self.query_params = query_params
        self.headers = headers
        self.headers['Content-Type'] = self.__class__.content_types[content_type]
        self.headers['Accept'] = self.__class__.accept[accept]
        self.content_type = content_type

    def send(self, verify_ssl=True):
        kwargs = {'params': self.query_params,
                  'headers': self.headers,
                  'verify': verify_ssl}
        if self.content_type == 'json':
            kwargs['json'] = self.body_params
        elif self.content_type == 'form':
            kwargs['data'] = self.body_params
        else:
            raise UnknownContentType(self.content_type)

        return getattr(requests, self.verb)(self.url, **kwargs)

    def __str__(self):
        return 'verb: {}\nurl: {}\n, body: {}\nquery: {}\n, headers: {}'.format(self.verb,
                                                                                self.url,
                                                                                self.body_params,
                                                                                self.query_params,
                                                                                self.headers)


class Action(metaclass=ABCMeta):
    disabled_hooks = set()  # this disables specific event hooks defined in the following methods
    overridden_presend_hooks = OrderedDict()  # this allows to override the hooks defined in the following methods
    overridden_success_hooks = OrderedDict()  # this allows to override the hooks defined in the following methods
    overridden_failure_hooks = OrderedDict()  # this allows to override the hooks defined in the following methods
    content_type = 'json'  # available content types: `json`, `form`
    accept = 'json'  # available values: `json`, `xml`

    @staticmethod
    def get_presend_hooks():
        """
        :return: an ordered dictionary of named `EventHook`s to run in order before a request. These hooks can expect
        the following inputs:
        * request: Request,
        * action: Action,
        * api_context: ApiContext
        """
        return OrderedDict()

    @staticmethod
    def get_success_hooks():
        """
        :return: an ordered dictionary of named `EventHook`s to run in order in the case of a successful request.
        These hooks can expect the following inputs:
        * request: Request,
        * response: requests.Response
        * action: Action,
        * api_context: ApiContext
        """
        return OrderedDict()

    @staticmethod
    def get_failure_hooks():
        """
        :return: an ordered dictionary of named `EventHook`s to run in order in the case of a failed request.
        These hooks can expect the following inputs:
        * request: Request,
        * response: requests.Response
        * action: Action,
        * api_context: ApiContext
        """
        return OrderedDict()

    @staticmethod
    @abstractmethod
    def get_verb():
        """
        :return: the http verb, possible (case insensitive) values are: GET, POST, PATCH, PUT, DELETE
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def get_route():
        """
        :return: the route this action calls with potential variable parameters, example: /booking/{id}
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def get_url_schema():
        """
        :return: a dictionary {'param_name': Sendable}, where Sendable is either a subclass of object.Sendable
        or a function which validates the parameter.
        This dictionary should have as keys every key present in the get_route()'s return value as .../{param_name}/...
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def get_body_schema():
        """
        :return: a dictionary {'param_name': Sendable}, where Sendable is either a subclass of object.Sendable
        or a function which validates a primitive type.
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def get_query_schema():
        """
        :return: a dictionary {'param_name': Sendable}, where Sendable is either a subclass of object.Sendable
        or a function which validates a primitive type.
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def get_response_schema():
        """
        :return: a dictionary of {'param_name': Receivable} where Receivable is either a subclass of object.Receivable
        or a function which validates a json and returns the desired object
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def get_status_exceptions():
        """
        :return: a dictionary of {'status_code': Exception} where Exception should be a class inheriting from python's
        default Exception and taking as constructor input a request.
        """
        raise NotImplemented

    @classmethod
    def json_to_object(cls, json_):

        response_schema = cls.get_response_schema()
        if isinstance(response_schema, dict):
            return json_
        elif issubclass(response_schema, Receivable):
            return response_schema.from_json(json_)
        else:
            raise ValueError("Unknown response schema type")

    def validate_body_params(self, params):
        valid, errors = self._validate(params, self.__class__.get_body_schema())
        if not valid:
            raise ValueError("Body params are invalid, errors: {}".format(errors))

    def validate_response(self, params):
        valid, errors = self._validate(params, self.__class__.get_response_schema())
        if not valid:
            raise ValueError("Response params are invalid, errors: {}".format(errors))

    def validate_url_params(self, params):

        valid, errors = self._validate(params, self.__class__.get_url_schema())
        if not valid:
            raise ValueError("Url params are invalid, errors: {}".format(errors))

    def validate_query_params(self, params):
        valid, errors = self._validate(params, self.__class__.get_query_schema())
        if not valid:
            raise ValueError("Query params are invalid, errors: {}".format(errors))

    def _validate(self, params, schema):
        if isinstance(schema, dict):
            # TODO empty schema fill until actions are automatically generated
            schema = schema or {'type': 'object',
                                'rules': ['nullable'],
                                'schema': {}}
        elif issubclass(schema, Sendable):
            schema = schema.get_sending_schema()
        elif issubclass(schema, Receivable):
            schema = schema.get_receiving_schema()
        if isinstance(params, Sendable) or isinstance(params, Receivable):
            params = params.to_json()

        validator = ValidatorFactory.make(schema)
        valid = validator.validate(params)
        if valid:
            return valid, None
        return valid, validator.errors.to_dict()

    def __init__(self, api_context, cache=None):
        cls = self.__class__
        self.api_context = api_context
        self._url_param_names = set()
        self._url_params = {}
        self._body_params = {}
        self._query_params = {}
        self.headers = {}
        self.url = None
        self.compiled = False
        self.request = None
        self.cache = cache
        self.presend_hooks = cls.get_presend_hooks()
        self.success_hooks = cls.get_success_hooks()
        self.failure_hooks = cls.get_failure_hooks()
        self.runs = 0

        for chunk in self.__class__.get_route().split('/'):
            if len(chunk) >= 2 and chunk[0] == '{' and chunk[-1] == '}':
                self._url_param_names.add(chunk[1:-1])

    @property
    def body_params(self):
        return self._body_params

    @body_params.setter
    def body_params(self, params):
        if isinstance(params, dict):
            self._body_params = params
        elif isinstance(params, Sendable):
            self._body_params = params.to_json()
        elif isinstance(params, list):
            # assume list of sendables
            self._body_params = [obj.to_json() for obj in params]
        else:
            raise ValueError('Body params of type {}'.format(type(params)))
        self.validate_body_params(params)

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, params):
        if isinstance(params, dict):
            self._query_params = params
        else:
            raise ValueError('Must provide a dictionary for query params')
        self.validate_query_params(params)

    @property
    def url_params(self):
        return self._url_params

    @url_params.setter
    def url_params(self, params):
        self.validate_url_params(params)
        self._url_params = params

    def set_headers(self, headers):
        self.headers = headers

    def compile(self):
        if self.compiled:
            raise ValueError('Action already compiled')

        route = self.__class__.get_route()
        for param_name in self._url_param_names:
            route = route.replace('{{{}}}'.format(param_name), self.url_params[param_name])

        host = '{}:{}'.format(self.api_context.hostname, self.api_context.port)

        self.url = self.api_context.url_template.format(hostname=host,
                                                        base_url=self.api_context.base_url,
                                                        version=self.api_context.version,
                                                        route=route)
        self.compiled = True

    @classmethod
    def get_exception(cls, request, response):
        return cls.get_status_exceptions()[response.status_code](request, response)

    def run(self):
        self.compile()

        cls = self.__class__
        verb = cls.get_verb().lower()

        self.request = Request(verb,
                               self.url,
                               self.query_params,
                               self.body_params,
                               self.headers,
                               content_type=self.__class__.content_type,
                               accept=self.__class__.accept)

        for name, hook in self.presend_hooks.items():
            if name not in self.__class__.disabled_hooks:
                try:
                    self.__class__.overridden_presend_hooks[name](self.request, api_context=self.api_context,
                                                                  action=self)
                except KeyError:
                    hook(self.request, api_context=self.api_context, action=self)

        try:
            response = self.request.send(verify_ssl=self.api_context.verify_ssl)
            self.runs += 1
        except RequestException as exc:
            raise CouldNotSendRequest(str(exc))

        status = response.status_code
        if 200 <= status <= 299:

            for name, hook in self.success_hooks.items():
                if name not in self.__class__.disabled_hooks:
                    try:
                        self.__class__.overridden_success_hooks[name](self.request,
                                                                      response,
                                                                      api_context=self.api_context,
                                                                      action=self)
                    except KeyError:
                        hook(self.request, response, api_context=self.api_context, action=self)

        else:

            for name, hook in self.failure_hooks.items():
                if name not in self.__class__.disabled_hooks:
                    try:
                        self.__class__.overridden_failure_hooks[name](self.request,
                                                                      response,
                                                                      api_context=self.api_context,
                                                                      action=self)
                    except KeyError:
                        hook(self.request, response, api_context=self.api_context, action=self)

            try:
                raise self.get_exception(self.request, response)

            except KeyError:
                raise ValueError('Request returned unhandled status: {}'.format(status))

        if response.content.decode() == '':
            return None
        response_data = response.json()

        self.validate_response(response_data)
        return self.__class__.json_to_object(response_data)

    def rerun(self):
        self.compiled = False
        return self.run()


class RollbackableAction(Action, metaclass=ABCMeta):
    def __init__(self, api_context):
        super().__init__(api_context)
        self.response = None

    def run(self):
        self.response = super().run()
        return self.response

    @abstractmethod
    def rollback(self):
        """
        Executes the operation needed to rollback a previous request. Can use self.response to get useful
        data to use for rollbacking
        :return: None
        """
        raise NotImplemented


class FailCheckThread(Thread):
    def run(self):
        try:
            Thread.run(self)
        except Exception as exc:
            self.err = exc
        else:
            self.err = None


class Summarizable(object):
    def __init__(self):
        self.summary = {'success': {'rollback': {}},
                        'failed': {'rollback': {}},
                        }

    def get_summary(self):
        return self.summary

    def report_action(self, action, index, outcome, result=None):
        if outcome == 'failed':
            self.summary[outcome][
                str(action.__class__.__name__) + '_' + str(index)] = result.__class__.__name__ + ':' + str(result)
        elif outcome == 'rollback_failed':
            self.summary['failed']['rollback'][
                str(action.__class__.__name__) + '_' + str(index)] = result.__class__.__name__ + ':' + str(result)
        elif outcome == 'rollback_success':
            self.summary['success']['rollback'] = str(action.__class__.__name__) + '_' + str(index)
        elif outcome == 'success':
            self.summary[outcome][str(action.__class__.__name__) + '_' + str(index)] = result
        else:
            raise UnexpectedOutcome('{} is not a valid outcome for report_action'.format(outcome))


class Rollbackable(Summarizable):
    def rollback_action(self, action, i):
        try:
            action.rollback()
            self.report_action(action, i, 'rollback_success')
        except SDKException as exc_r:
            self.report_action(action, i, 'rollback_failed', exc_r)


class ActionParallelizer(Rollbackable, Summarizable):
    def __init__(self, *actions):
        self.actions = actions
        super().__init__()

        def store(func, results, i):
            results[i] = func()

        self.results = [None] * len(actions)
        self.threads = [FailCheckThread(target=store, args=(action.run, self.results, i)) for i, action in
                        enumerate(self.actions)]
        self.started = False

    def run(self, raise_exception=True):
        if self.started:
            raise ValueError('Already started')

        self.started = True

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

        failed = {action for action, thread in zip(self.actions, self.threads) if thread.err is not None}
        for index, (action, thread) in enumerate(zip(self.actions, self.threads)):
            if thread.err is not None:
                self.report_action(action, index, 'failed', thread.err)
        for index, result in enumerate(self.results):
            if result is not None:
                self.report_action(self.actions[index], index, 'success', result)
        if failed and raise_exception:
            to_raise = next(t.err for t in self.threads if t.err is not None)
            for index, action in enumerate([act for act in self.actions if act not in failed]):
                if isinstance(action, RollbackableAction):
                    self.rollback_action(action, index)
            raise to_raise

        return self.results


class ActionSequentializer(Rollbackable, Summarizable):
    def __init__(self, actions, steps):
        self.init_action = actions[0]
        self.actions = actions[1:]
        self.steps = steps
        self.results = []
        self.started = False
        super().__init__()

    def run(self):
        if self.started:
            raise ValueError('Sequentializer Already Started')
        self.started = True
        try:
            result = self.init_action.run()
            self.results.append(result)
            self.report_action(self.init_action, 'init', 'success', result)
        except SDKException as exc_init:
            self.report_action(self.init_action, 'init', 'failed', exc_init)
            raise exc_init
        else:
            for index, (action, step) in enumerate(zip(self.actions, self.steps)):
                try:
                    result = self.run_action(result, step, action, index)
                except SDKException as exc:
                    for rb_index, to_rollback in reversed(list(enumerate(self.actions[:index]))):
                        if isinstance(to_rollback, RollbackableAction):
                            self.rollback_action(to_rollback, rb_index)
                    if isinstance(self.init_action, RollbackableAction):
                        self.rollback_action(self.init_action, 'init')
                    raise exc
            return self.results

    def run_action(self, previous_result, step, action, i):
        try:
            result = step(previous_result, action)
            self.results.append(result)
            self.report_action(action, i, 'success', result)
            return result
        except SDKException as exc:
            self.report_action(action, i, 'failed', exc)
            raise exc
