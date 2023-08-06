from typing import ClassVar

from macrobase_driver.config import DriverConfig


class MacrobaseDriver(object):

    def __init__(self, name: str = None):
        self.name = name
        self.config = DriverConfig

    def update_config(self, config_obj: ClassVar[DriverConfig]):
        pass

    def run(self, *args, **kwargs):
        pass
