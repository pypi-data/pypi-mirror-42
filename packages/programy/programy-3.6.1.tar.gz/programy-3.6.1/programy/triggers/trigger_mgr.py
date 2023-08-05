"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

from programy.triggers.config import TriggerConfiguration
from programy.context import ClientContext
from programy.storage.factory import StorageFactory


class TriggerEvents(object): # Enum

    UNKNOWN = 0
    SYSTEM_STARTUP = 1
    SYSTEM_SHUTDOWN = 2
    CONVERSATION_START = 3

    @staticmethod
    def to_str(event: int) -> str:
        if event == TriggerEvents.SYSTEM_STARTUP:
            return 'SYSTEM_STARTUP'

        if event == TriggerEvents.SYSTEM_SHUTDOWN:
            return 'SYSTEM_SHUTDOWN'

        if event == TriggerEvents.CONVERSATION_START:
            return 'CONVERSATION_START'

        return "UNKNOWN"

    @staticmethod
    def to_id(text: str) -> int:
        if text == 'SYSTEM_STARTUP':
            return TriggerEvents.SYSTEM_STARTUP

        if text == 'SYSTEM_SHUTDOWN':
            return TriggerEvents.SYSTEM_SHUTDOWN

        if text == 'CONVERSATION_START':
            return TriggerEvents.CONVERSATION_START

        return TriggerEvents.UNKNOWN


class TriggerManager(object):

    def __init__(self, config: TriggerConfiguration):

        assert isinstance(config, TriggerConfiguration)

        self._config = config
        self._triggers = {}

    def trigger(self, event: int, client_context: ClientContext = None, data = None):

        assert isinstance(client_context, ClientContext)

        if event in self._triggers:
            trigger_list = self._triggers[event]
            for trigger in trigger_list:
                try:
                    trigger.trigger(client_context, data)

                except Exception as exec:
                    YLogger.exception(client_context, "Trigger %d failed to fire", exec, event)

    def load_triggers(self, storage_factory: StorageFactory):

        assert isinstance(storage_factory, StorageFactory)

        YLogger.debug(self, "Loading Triggers")
        if storage_factory.entity_storage_engine_available(StorageFactory.Triggers) is True:
            trigger_engine = storage_factory.entity_storage_engine(StorageFactory.Triggers)
            if trigger_engine:
                try:
                    trigger_store = trigger_engine.trigger_store()
                    trigger_store.load_all(self)

                except Exception as e:
                    YLogger.exception(self, "Failed to load triggers from storage", e)
