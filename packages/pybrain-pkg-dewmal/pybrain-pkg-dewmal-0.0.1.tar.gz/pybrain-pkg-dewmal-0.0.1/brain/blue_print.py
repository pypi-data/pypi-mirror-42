class Brain:
    __facts_senders__ = {}
    __facts_readers__ = {}
    __action_receivers__ = {}

    class Context:

        def __init__(self, brain, fact_sender) -> None:
            self.fact_sender = fact_sender
            self.brain = brain

        async def feed(self, time, data):
            await self.brain.__feed__(source=self.fact_sender, time=time, data=data)

    def fact_reader_register(self, name, fn):

        if name is not None and name in self.__facts_readers__:
            self.__facts_readers__[name].append(fn)

    def fact(self, name, source=None, sync_time=False):
        def decorator(_fn):
            _fn.name = name
            _fn.sync_time = sync_time
            self.__facts_senders__[name] = _fn

            if name not in self.__facts_readers__:
                self.__facts_readers__[name] = []

            if source is not None:
                self.fact_reader_register(source, _fn)

        return decorator

    async def __feed__(self, source, time, data):
        for reader in self.__facts_readers__[source]:
            await reader(Brain.Context(self, reader.name), time, data)

    async def run(self):
        for fact_sender in self.__facts_senders__:
            sender_fn = self.__facts_senders__[fact_sender]
            await sender_fn(Brain.Context(self, fact_sender))
