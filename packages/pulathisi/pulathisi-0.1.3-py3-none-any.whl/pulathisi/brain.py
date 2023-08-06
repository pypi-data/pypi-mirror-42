from pulathisi import Reactor


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
