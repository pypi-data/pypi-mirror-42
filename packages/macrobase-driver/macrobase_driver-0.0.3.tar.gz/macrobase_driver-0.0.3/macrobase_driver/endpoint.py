import abc

from macrobase_driver.context import Context


class Endpoint(object, metaclass=abc.ABCMeta):
    """
    Endpoint protocol for processing from macrobase and his drivers
    """
    context: Context

    def __init__(self, context: Context):
        self.context = context
        self.__name__ = self.__class__.__name__

    async def __call__(self, *args, **kwargs):
        return await self.handle(*args, **kwargs)

    @abc.abstractmethod
    async def handle(self, *args, **kwargs):
        raise NotImplementedError
