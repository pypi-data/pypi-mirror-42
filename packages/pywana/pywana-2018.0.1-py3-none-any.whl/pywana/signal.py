#!/usr/bin/env python3

# Copyright (c) 2019 Jakob Meng, <jakobmeng@web.de>

from typing import List, Callable, Any
import signal
import logging
from threading import Event

class SignalHandler(object):
    def __init__(
        self, 
        signalnums : List[int],
        handler : Callable[[Any, Any], None]
    ):
        self._signalnums = signalnums
        self._handler = handler
    
    def register(self):
        def signal_handler(signum, frame):
            # Printing, e.g. by logging to stderr or stdout is not safe in signal handlers!
            # Ref.: https://bugs.python.org/issue24283
            self._handler(signum, frame)
    
        # set signal handler and store old handlers for later restore
        self._handlers = []
        for signalnum in self._signalnums:
            handler = signal.signal(signalnum, signal_handler)
            self._handlers.append([signalnum, handler])
        
        logging.debug('Registered signal handlers for ' + str(self._signalnums))
        return self
    
    def unregister(self):
        # reset handlers
        for signalnum,handler in self._handlers:
            signal.signal(signalnum, handler)
        logging.debug('Unregistered signal handlers for ' + str(self._signalnums))
    
    def __enter__(self):
        self.register()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.unregister()

def wait_for_signals(signalnums : List[int], Timeout=None):
    fired = Event()
    def signal_handler(signum, frame):
        # Printing, e.g. by logging to stderr or stdout is not safe in signal handlers!
        # Ref.: https://bugs.python.org/issue24283
        fired.set()
    
    with SignalHandler(signalnums, signal_handler):
        logging.debug("Waiting for signals " + str(signalnums) + "...")
        return fired.wait(Timeout)
