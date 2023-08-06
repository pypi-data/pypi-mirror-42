from queue import Queue


class Brain:
    __facts_senders__ = {}
    __facts_readers__ = {}
    __action_receivers__ = {}

    class Context:

        def __init__(self, brain, fact_sender) -> None:
            self.fact_sender = fact_sender
            self.brain = brain

        async def feed(self, index, data):
            await self.brain.__feed__(source=self.fact_sender, index=index, data=data)

    def fact_reader_register(self, name, fn, config):

        if name is not None and name in self.__facts_readers__:
            self.__facts_readers__[name].append((fn, config))

    def fact(self, name, source=None, sync_time=False, buffer_size=0, skip_size=1):
        def decorator(_fn):
            _fn.name = name
            _fn.sync_time = sync_time
            self.__facts_senders__[name] = _fn

            if name not in self.__facts_readers__:
                self.__facts_readers__[name] = []

            if source is not None:
                config = {
                    'buffer_size': buffer_size,
                    'skip_size': skip_size,
                }
                self.fact_reader_register(source, _fn, config)

        return decorator

    temp_buffer = {}

    async def __feed__(self, source, index, data):
        for _reader_meta_ in self.__facts_readers__[source]:
            reader = _reader_meta_[0]
            reader_config = _reader_meta_[1]

            if reader_config['buffer_size'] > 0:
                buffer_size = reader_config['buffer_size']
                skip_size = reader_config['skip_size']
                temp_name = source + str(reader)
                if not temp_name in self.temp_buffer:
                    self.temp_buffer[temp_name] = Queue(maxsize=buffer_size)

                self.temp_buffer[temp_name].put({
                    'index': index,
                    'data': data
                })

                if self.temp_buffer[temp_name].full():
                    await reader(Brain.Context(self, reader.name), index, list(self.temp_buffer[temp_name].queue))
                    for s in range(skip_size):
                        self.temp_buffer[temp_name].get()

            else:
                await reader(Brain.Context(self, reader.name), index, data)

    async def run(self):
        for fact_sender in self.__facts_senders__:
            sender_fn = self.__facts_senders__[fact_sender]
            await sender_fn(Brain.Context(self, fact_sender))
