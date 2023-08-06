from os import path


class Container:
    def __str__(self):
        return type(self).__name__

    def __getitem__(self, item: str):
        return self.get(item)

    def __getattr__(self, attr):
        if not attr in type(self._data).__dict__.keys():
            raise AttributeError
        return getattr(self._data, attr)

    def __init__(self):
        raise NotImplementedError

    def get(self, item=None):
        if not item:
            return self._data
        return self._data[item]


class FileStore(type):
    _instances = {}

    def __call__(cls, file_path):
        if not filepath in cls._instances:
            cls._instances[file_path] = super(FileStore, cls).__call__(file_path)

        return cls._instances[file_path]


class FileCache(metaclass=FileStore):
    def __init__(self, file_path):
        self.file_path = file_path
        self._data = None

    def get(self):
        return self._data

    def set(self, data):
        self._data = data

    def clean(self):
        self._data = None


class FileDriver(Container):
    def __init__(self, file_path: str):
        self.file_path = file_path
        file_name, extension = path.splitext(self.file_path)
        if not extension:
            if path.exists(file_name) is False:
                self.filepath += '.' + type(self).__name__.lower()

    def handle(self):
        raise NotImplementedError

    @classmethod
    def read(cls, filepath: str, reload_file=False) -> dict:
        cache = FileCache(filepath)
        if reload_file is True:
            cache.clean()

        if cache.get():
            return cache.get()

        obj = cls(filepath)
        cache.set(obj.handle())
        return cache.get()

