#!/usr/bin/env python3

# Copyright (c) 2019 Jakob Meng, <jakobmeng@web.de>

import logging
import psutil
import tempfile
import os
import sys
from .os import get_run_dir
import subprocess
from threading import Thread
from typing import List
import re

class PidDir(object):
    def __init__(
        self,
        tag    : str  = os.path.basename(sys.argv[0] if sys.argv[0] else __file__),
        delete : bool = False
    ):
        self._tag = tag
        self._delete = delete
        
        self.path = os.path.join(get_run_dir(), tag)
        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
    
    def __del__(self):
        if self._delete:
            try:
                os.remove(self.path)
            except:
                logging.exception("Could not remove PidDir " + self._dir)

class PidFile(object):
    def __init__(
        self,
        dir : str = PidDir(delete=False).path,
        pid : int = os.getpid()
    ):
        self._dir = dir
        self._pid = pid
        
        fd, self.path = tempfile.mkstemp(suffix='.pid', prefix=str(pid), dir=dir, text=False)
        os.write(fd, '{}'.format(pid).encode())
        os.close(fd) # on windows if a file is still open it cannot be read by another process so close it and delete it later
        self._deleted = False
        logging.debug("Wrote pid file " + self.path)
    
    def remove(self):
        if not self._deleted:
            logging.debug("Removing pid file " + self.path)
            os.unlink(self.path)
            self._deleted = True
        
    def __del__(self):
        self.remove()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.remove()

class PidFileMonitor(object):
    def __init__(
        self,
        dir : str = PidDir(delete=False).path,
    ):
        self._dir = dir
    
    def running(self):
        if not os.path.isdir(self._dir):
            logging.debug("Pid dir " + self._dir + " does not exist.")
            return None
        else:
            def read_pid(pid_file : str):
                logging.debug("Reading pid file " + pid_file)
                
                with open(pid_file, "r") as f:
                    pid = f.read()
                try:
                    return int(pid)
                except ValueError as e:
                    logging.exception("Unexpected pid file " + pid_file)
                    return None
            
            pid_files = [os.path.join(self._dir, file)
                         for file in os.listdir(self._dir) 
                         if os.path.isfile(os.path.join(self._dir, file)) and
                            os.path.splitext(file)[1] == ".pid"]
            
            return [pid for pid in [read_pid(path) for path in pid_files] if pid is not None]
    
    def wait_all(self):
        for pid in self.running():
            try:
                proc = psutil.Process(pid)
            except psutil.NoSuchProcess:
                logging.info("No process with pid " + str(pid) + " found.")
            
            logging.info("Waiting for process with pid " + str(pid))
            while proc.is_running():
                try:
                    proc.wait(5)
                    logging.info("Still waiting...")
                except psutil.TimeoutExpired:
                    pass

class TeeThread(Thread):
    def __init__(self, in_file, *out_files, **kwargs):
        super(TeeThread, self).__init__(**kwargs)
        self._in_file = in_file
        self._out_files = out_files
        
        self.is_failed = False
        self.error = None
        self.traceback = None
    
    def run(self):
        self.is_failed = False
        self.error = None
        self.traceback = None
        try:
            for line in self._in_file:
                for f in self._out_files:
                    f.write(line)
        except:
            logging.debug("Writing to file or pipe failed", exc_info=True)
            self.is_failed = True
        finally:
            self.error = sys.exc_info()[1]
            self.traceback = sys.exc_info()[2]

def run_live(*popenargs, check=False, **kwargs):
    if ('stdout' in kwargs) or ('stderr' in kwargs) or ('bufsize' in kwargs) or ('universal_newlines' in kwargs):
        raise ValueError('stdout, stderr, bufsize and universal_newlines arguments may not be used')
    
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE
    kwargs['bufsize'] = 1
    kwargs['universal_newlines'] = True
    
    # References:
    #  https://github.com/python/cpython/blob/master/Lib/subprocess.py
    #  https://stackoverflow.com/a/4985080/6490710
    #  https://stackoverflow.com/a/17698359/6490710
    
    def tee(in_file, *out_files):
        t = TeeThread(in_file, *out_files, daemon=True)
        t.start()
        return t
    
    class StringWriter(object):
        def __init__(self):
            self.text = ''
            
        def write(self, text):
            self.text += text
    
    stdout = StringWriter()
    stderr = StringWriter()
    
    logging.info('$> {}'.format(*popenargs))
    
    with subprocess.Popen(*popenargs, **kwargs) as p:
        try:
            threads = []
            threads.append(tee(p.stdout, stdout, sys.stdout))
            threads.append(tee(p.stderr, stderr, sys.stderr))
            
            for t in threads: t.join()
            
            for t in threads:
                if t.is_failed:
                    raise subprocess.SubprocessError('logging thread(s) failed: {}\n{}'.format(t.error, t.traceback))
            
            if p.poll() is None:
                raise subprocess.SubprocessError('stdout/stderr logging threads stopped, but process is alive')
        except:
            p.kill()
            # No p.wait() here as __exit__ does that for us
            raise
        
        assert(p.poll() is not None) # None := process is alive
        retcode = p.poll()
        
        if check and retcode:
            raise subprocess.CalledProcessError(retcode, p.args, output=stdout.text, stderr=stderr.text)
        
        return subprocess.CompletedProcess(p.args, retcode, stdout.text, stderr.text)

def list_processes(names : List[str] = None):
    all = psutil.process_iter()
    if not names:
        return all
    
    regexes = [re.compile(name) for name in names]
    procs = []
    for proc in all:
        for regex in regexes:
            if regex.fullmatch(proc.name()):
                procs.append(proc)
    return procs
