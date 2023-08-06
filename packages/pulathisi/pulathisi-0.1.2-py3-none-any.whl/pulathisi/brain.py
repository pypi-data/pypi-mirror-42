from collections import Mapping

from persistent import persistence

from pulathisi import Reactor


class DictObj(persistence.Persistent):

    def __init__(self) -> None:
        self.key = None
        self.value = None


class MultiProcessDist(Mapping):

    def __init__(self, *args, **kw):
        self._storage = dict(*args, *kw)

    def __getitem__(self, key):
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def __setitem__(self, key, value):
        self._storage[key] = value


__facts_senders__ = MultiProcessDist()
__facts_readers__ = MultiProcessDist()
__action_receivers__ = MultiProcessDist()
temp_buffer = MultiProcessDist()
latest_buffer = MultiProcessDist()


class Brain(Reactor):

    def process_sum(self, sources, _fn):
        pass

    def sum(self, name, sources):
        def decorator(_fn):
            @self.processor(name=name, source=self.time_sync_source_name)
            async def decorator_temp(context: Reactor.Context, index=-1, data=None):
                values = {}
                for source in sources:
                    source_data = await context.get_current_value(source=source)
                    values[source] = source_data
                await _fn(context, index, values)

        return decorator
