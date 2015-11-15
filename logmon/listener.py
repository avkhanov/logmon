from logmon.logreader import LogReader
from threading import Thread, Lock
from logmon.exceptions import InvalidLogReaderException, \
    AlreadyListeningException,\
    AlreadyNotListeningException

import time


class Listener(object):
    def __init__(self, log_or_loglist, interval=1):
        if isinstance(log_or_loglist, list):
            for i in log_or_loglist:
                if not isinstance(i, LogReader):
                    raise InvalidLogReaderException(i)
            self.loglist = log_or_loglist
        elif isinstance(log_or_loglist, LogReader):
            self.loglist = [log_or_loglist]
        else:
            raise InvalidLogReaderException(log_or_loglist)

        self._interval = interval
        self._thread = None
        self._thread_started = Lock()

        self._thread_started.acquire()
        self._prepare_to_stop = False
        self._event_list = {}

    def _main_thread(self):
        while not self._prepare_to_stop:
            for i in self.loglist:
                lines = i.read().split('\n')

                for line in lines:
                    for event in self._event_list:
                        if event._match(line):
                            data = event._gen_event_object(line)

                            for callback in self._event_list[event]:
                                callback(data)

            time.sleep(self._interval)

    def start(self):
        if self._thread is not None:
            raise AlreadyListeningException(self)

        for i in self.loglist:
            i.attach()

        self._thread = Thread(target=self._main_thread)
        self._thread.start()
        self._thread_started.release()

    def attach(self, event, callback_or_callbacklist):
        if hasattr(callback_or_callbacklist, '__call__'):
            callbacks = [callback_or_callbacklist]
        elif isinstance(callback_or_callbacklist, list):
            callbacks = callback_or_callbacklist

        try:
            self._event_list[event]
        except KeyError:
            self._event_list[event] = []

        self._event_list[event].extend(callbacks)


    def stop(self):
        if self._thread is None:
            raise AlreadyNotListeningException(self)

        self._thread_started.acquire()
        self._prepare_to_stop = True
        self._thread.join()
        self._thread = None

        for i in self.loglist:
            i.detach()

        self._prepare_to_stop = False

if __name__ == "__main__":
    from logmon.textlog import TextLog
    from logmon.event import Event

    def test(e):
        pass

    def test2(e):
        pass

    t = TextLog("../logmon_test/manual/test.txt")

    e1 = Event("huhra")
    e2 = Event("hahra")

    l = Listener(t)

    l.attach(e1, test)
    l.attach(e2, test)
    l.attach(e2, test2)

    l.start()
    # time.sleep(20)
    l.stop()

    print(l._event_list)
