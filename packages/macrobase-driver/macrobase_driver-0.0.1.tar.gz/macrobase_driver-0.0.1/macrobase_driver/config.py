from enum import Enum


class LogFormat(Enum):
    json = 'json'
    plain = 'plain'

    @property
    def raw(self) -> str:
        return str(self.value)


class LogLevel(Enum):
    critical = 'CRITICAL'
    error = 'ERROR'
    warning = 'WARNING'
    info = 'INFO'
    debug = 'DEBUG'
    notset = 'NOTSET'

    @property
    def raw(self) -> str:
        return str(self.value)


class SimpleConfig:

    LOGO: str = """
 _____       _
|  __ \     (_)               
| |  | |_ __ ___   _____ _ __ 
| |  | | '__| \ \ / / _ \ '__|
| |__| | |  | |\ V /  __/ |   
|_____/|_|  |_| \_/ \___|_|
"""

    WORKERS: int = 1

    LOG_FORMAT: LogFormat = LogFormat.json
    LOG_LEVEL: LogLevel = LogLevel.info


class WrappedConfig(dict, SimpleConfig):

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as ke:
            raise AttributeError(f"Config has no '{ke.args[0]}'")

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self[key] = value

    def from_object(self, obj):
        """
        Update the values from the given object.
        :param obj: an object holding the configuration
        """
        if isinstance(obj, type):
            params = dir(obj)
        elif isinstance(obj, dict):
            params = obj.keys()

        for key in params:
            if key.isupper():
                self[key] = getattr(obj, key)
                setattr(self, key, self[key])


class DriverConfig(WrappedConfig):
    pass
