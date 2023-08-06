__version__ = '0.2.5'

from copy import deepcopy
from functools import reduce
from os import environ, getcwd

from .base import Container
from .drivers import Yaml, Json


class Loader(Container):
    def __init__(self, **kwargs):
        self._data = self.load(**kwargs)


class Env(Loader):
    """ Loads values from environment variables

        Usage:
            Environment.read(prefix=value, defaults=dict)

        Args:
            "prefix" will be added to all variables,
            for example: prefix_variable in uppercase

            "source" is a dictionary of names for finding variables,
            result will contain only variables that will be found.
    """

    def load(self, **kwargs):
        result = dict()
        for key in kwargs.get('defaults'):
            prefix = kwargs.get('prefix', None)
            var_name = prefix + '_' + key if prefix else key
            value = environ.get(var_name.upper(), None)
            if value:
                result.update({key: value})
        return result


class File(Loader):
    """ Usage:
            File.read(prefix=value, source=value, file_path=value)

        It works in the same way as the environment class,
        except for the additional argument containing
        path to the readable file.
    """

    _drivers = (
        Json,
        Yaml,
    )

    def load(self, **kwargs):
        result = dict()
        for key in kwargs.get('defaults'):
            prefix = kwargs.get('prefix', None)
            file_path = kwargs.get('file_path')
            read = self._read_file(file_path, prefix if prefix else key)
            if isinstance(read, dict):
                value = read.get(key, None)
                if value: result.update({key: value})
            elif read:
                result.update({key: read})
        return result

    def _read_file(self, file_path, section):
        for driver in self._drivers:
            try:
                read = driver.read(file_path)
                if not section in read:
                    for value in read.values():
                        if isinstance(value, dict) and section in value:
                            return value[section]
                return read[section]
            except Exception:
                continue
        return {}


""" Base classes."""


class ABConfig(Container):
    file_path = getcwd() + '/config'

    loaders = (
        File,
        Env,
    )

    _excluded_attrs = (
        'loaders',
        'file_path',
    )

    def __init__(self, prefix=None, **kwargs):
        if type(self).__name__ == 'ABConfig':
            raise NotImplementedError

        self._prefix = prefix
        self._data = self.make(**self._attrs(**kwargs))

    def make(self, **kwargs):
        result = {}
        for name, defaults in kwargs.items():
            values = deepcopy(defaults)
            for loader in self.loaders:
                types = (int, str, bool, list, tuple)
                checks = map(lambda x: isinstance(values, x), types)
                if reduce(lambda a, b: a or b, checks):
                    read = loader(
                        prefix=self._prefix,
                        defaults=(name,),
                        file_path=self.file_path
                    ).get()
                    if read:
                        values = read[name]
                        continue

                if isinstance(values, dict):
                    read = loader(
                        prefix=name,
                        defaults=defaults.keys(),
                        file_path=self.file_path
                    ).get()
                    values.update(read)

            result.update({name: values})
        return result

    def _attrs(self, **kwargs):
        result = {}
        for attr in type(self).__dict__.keys():
            if (attr[:2] != '__' and attr[:1] != '_' and
                    attr not in self._excluded_attrs):
                result.update({str(attr): getattr(self, attr)})

        if kwargs:
            result.update(kwargs)
        return result
