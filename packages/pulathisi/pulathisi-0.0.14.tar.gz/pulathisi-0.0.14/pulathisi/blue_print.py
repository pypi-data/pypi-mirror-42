import asyncio
from multiprocessing import Process
from queue import Queue


def config_order_key(elm):
    return elm[1]['order_index']


class Brain:
    __facts_senders__ = {}
    __facts_readers__ = {}
    __action_receivers__ = {}

    class Monitor:
        index_flow_temp = []
        index_flow = ''
        index_changed = False

        pre_index = -1

        def index_monitor(self, index, source):
            if self.pre_index != index:
                self.index_flow = [str(s) for s in self.index_flow_temp]
                self.index_flow_temp = []
                self.index_changed = True
            else:
                self.index_changed = False

            self.index_flow_temp.append(source)

    class Context:

        def __init__(self, brain, fact_sender) -> None:
            self.fact_sender = fact_sender
            self.brain = brain

        async def get_current_value(self, source):
            return await self.brain.__read__(source=source)

        async def feed(self, index, data, source=None):
            source = source if source is not None else self.fact_sender
            await self.brain.__feed__(source=source, index=index, data=data)

    def __init__(self) -> None:
        self.monitor = Brain.Monitor()

    def fact_reader_register(self, name, fn, config):

        if name is not None and name in self.__facts_readers__:
            self.__facts_readers__[name].append((fn, config))
            self.__facts_readers__[name].sort(key=config_order_key)

    def fact_reader(self, _fn, name, source=None, sync_time=False, buffer_size=0, skip_size=1, run_separate=False,
                    order_index=0):
        _fn.name = name
        _fn.sync_time = sync_time
        _fn.order_index = order_index
        _fn.run_separate = run_separate
        self.__facts_senders__[name] = _fn

        if name not in self.__facts_readers__:
            self.__facts_readers__[name] = []

        if source is not None:
            config = {
                'buffer_size': buffer_size,
                'skip_size': skip_size,
                'order_index': order_index
            }
            self.fact_reader_register(source, _fn, config)

    def fact(self, name, source=None, sync_time=False, buffer_size=0, skip_size=1, run_separate=False):
        def decorator(_fn):
            self.fact_reader(_fn=_fn, name=name, source=source, sync_time=sync_time, buffer_size=buffer_size,
                             skip_size=skip_size, run_separate=run_separate)

        return decorator

    temp_buffer = {}
    latest_buffer = {}

    async def __read__(self, source):
        if source in self.latest_buffer:
            return self.latest_buffer[source]

    async def __feed__(self, source, index, data):

        self.monitor.index_monitor(index, source)

        self.latest_buffer[source] = (index, data)

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
                    context = Brain.Context(self, reader.name)
                    index = index
                    data_ = list(self.temp_buffer[temp_name].queue)
                    if not reader.run_separate:
                        await reader(context, index, data_)
                    else:
                        p = Process(target=reader, args=(context, index, data_))
                        p.start()

                    for s in range(skip_size):
                        self.temp_buffer[temp_name].get()
            else:
                if not reader.run_separate:
                    context = Brain.Context(self, reader.name)
                    await reader(context, index, data)
                else:

                    def start_function():
                        asyncio.run(reader(context, index, data))

                    p = Process(target=start_function)
                    p.start()

    async def run(self):

        for fact_sender in self.__facts_senders__:
            sender_fn = self.__facts_senders__[fact_sender]
            context = Brain.Context(self, fact_sender)
            if not sender_fn.run_separate:
                await sender_fn(context)
            else:
                def start_function():
                    asyncio.run(sender_fn(context))

                p = Process(target=start_function)
                p.start()
