#!/usr/bin/env python3

# Copyright (c) 2019 Jakob Meng, <jakobmeng@web.de>


import logging
import dbus
import sys
import os
from gi.repository import GLib # from debian package python3-gi
from typing import List, Callable, Any
from threading import Thread

class LoginDProperties(object):
    def __init__(
        self,
        inhibit_delay_max_usec=None,
        preparing_for_shutdown=None,
        kill_user_processes=None
    ):
        self._inhibit_delay_max_usec = inhibit_delay_max_usec
        self._preparing_for_shutdown = preparing_for_shutdown
        self._kill_user_processes = kill_user_processes

    @property
    def inhibit_delay_max_usec(self):
        return self._inhibit_delay_max_usec

    @inhibit_delay_max_usec.setter
    def inhibit_delay_max_usec(self, inhibit_delay_max_usec):
        if self._inhibit_delay_max_usec != inhibit_delay_max_usec:
            self._inhibit_delay_max_usec = inhibit_delay_max_usec
    
    @property
    def preparing_for_shutdown(self):
        return self._preparing_for_shutdown

    @preparing_for_shutdown.setter
    def preparing_for_shutdown(self, preparing_for_shutdown):
        if self._preparing_for_shutdown != preparing_for_shutdown:
            self._preparing_for_shutdown = preparing_for_shutdown
            
    @property
    def kill_user_processes(self):
        return self._kill_user_processes

    @kill_user_processes.setter
    def kill_user_processes(self, kill_user_processes):
        if self._kill_user_processes != kill_user_processes:
            self._kill_user_processes = kill_user_processes

class LoginDConnection(object):
    def __init__(self):
        assert dbus.get_default_main_loop() is not None
        self._bus = dbus.SystemBus()
        self._proxy = self._bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
        self._properties = dbus.Interface(self._proxy, dbus_interface='org.freedesktop.DBus.Properties')
    
    def get_property(self, property : str):
        try:
            return self._properties.Get("org.freedesktop.login1.Manager", property)
        except dbus.exceptions.DBusException:
            logging.exception("Failed to retrieve logind property " + property + " via dbus")
            raise
    
    def get_properties(self):
        return LoginDProperties(
            inhibit_delay_max_usec=self.get_property("InhibitDelayMaxUSec"),
            preparing_for_shutdown=self.get_property("PreparingForShutdown"),
            kill_user_processes=self.get_property("KillUserProcesses")
        )
    
    def connect_to_signal(self, signal_name, handler_function, dbus_interface=None):
        self._proxy.connect_to_signal(signal_name, handler_function, dbus_interface)

class _GlibMainLoopThread(Thread):
    def __init__(self):
        super(_GlibMainLoopThread, self).__init__()
        assert dbus.get_default_main_loop() is not None
        self.is_failed = False
        self.error = None
        self.traceback = None
        self._loop = GLib.MainLoop()
        
    def __before__(self):
        pass
    
    def __after__(self):
        pass
    
    def run(self):
        self.is_failed = False
        self.error = None
        self.traceback = None
        try:
            self.__before__()
            self._loop.run()
            self.__after__()
        except Exception as e:
            logging.exception("Exception raised.")
            self.is_failed = True
        except KeyboardInterrupt as e:
            logging.exception("KeyboardInterrupt raised")
            self.is_failed = True
        except SystemExit as e:
            logging.exception("SystemExit raised")
            self.is_failed = True
        except:
            logging.exception("Error raised.")
            self.is_failed = True
        finally:
            self.error = sys.exc_info()[1]
            self.traceback = sys.exc_info()[2]
    
    def stop(self):
        if self._loop is not None:
            self._loop.quit()



class InhibitLock(object):
    def __init__(
        self,
        what : str ="shutdown:sleep",
        who  : str = os.path.basename(sys.argv[0] if sys.argv[0] else __file__),
        why  : str = "",
        mode : str = "delay"
    ):
        self._what = what
        self._who = who
        self._why = why
        self._mode = mode
        assert dbus.get_default_main_loop() is not None
        
        if mode == "delay":
            inhibit_delay_max_usec = LoginDConnection().get_properties().inhibit_delay_max_usec
            if inhibit_delay_max_usec < 30 * 1000 * 1000:
                logging.warning("Maximum shutdown delay is very short, increase InhibitDelayMaxUSec= " +
                                "in logind.conf! Help: man logind.conf")
    
    def lock(self):
        bus = dbus.SystemBus()
        self._inhibit_lock = bus.call_blocking(
            'org.freedesktop.login1', # bus_name
            '/org/freedesktop/login1', # object_path
            'org.freedesktop.login1.Manager', # dbus_interface
            'Inhibit', # method
            'ssss', # signature
            (
                self._what, # what
                self._who, # who
                self._why, # why
                self._mode #mode
            ), # args
            timeout=2.0 # timeout=-1.0
            # byte_arrays=False
            # **kwargs
        )
        logging.debug('Aquired lock for ' + self._what)
    
    def unlock(self):
        del self._inhibit_lock
        logging.debug('Released lock for ' + self._what)
        
    def __enter__(self):
        self.lock()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.unlock()

class PrepareForShutdownMonitor(_GlibMainLoopThread):
    def __init__(
        self, 
        handler : Callable[[], None]
    ):
        super(PrepareForShutdownMonitor, self).__init__()
        self._handler = handler
        assert dbus.get_default_main_loop() is not None
        self._logind_proxy = LoginDConnection()
    
    def __before__(self):
        logging.debug("__before__")
        
        def prepare_for_shutdown_handler(active):
            logging.debug("PrepareForShutdown(" + str(active) + ") received.")
            assert active
            self._handler()
        
        self._logind_proxy.connect_to_signal("PrepareForShutdown", prepare_for_shutdown_handler)
    
    def __after__(self):
        logging.debug("__after__")
    
    def wait(self, Timeout=None):
        self.join(Timeout)
        return self.is_alive() == False
