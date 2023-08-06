#!/usr/bin/env python3

# Copyright (c) 2019 Jakob Meng, <jakobmeng@web.de>

import os
import subprocess
import json
import logging
import sys

if sys.platform.startswith('linux'):
    def get_run_dir(uid : int = os.getuid()):
        run_dir = os.path.join("/run/user", str(uid))
        if not os.path.exists(run_dir) and uid == 0:
            run_dir = "/run"
        
        return run_dir

class FilesystemInfo(object):
    def __init__(self, uuid=None, name=None, fstype=None, mountpoint=None, label=None):
        self._uuid = uuid
        self._name = name
        self._fstype = fstype
        self._mountpoint = mountpoint
        self._label = label

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        if self._uuid != uuid:
            self._uuid = uuid
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self._name != name:
            self._name = name

    @property
    def fstype(self):
        return self._fstype

    @fstype.setter
    def fstype(self, fstype):
        if self._fstype != fstype:
            self._fstype = fstype

    @property
    def mountpoint(self):
        return self._mountpoint

    @mountpoint.setter
    def mountpoint(self, mountpoint):
        if self._mountpoint != mountpoint:
            self._mountpoint = mountpoint
    
    @property
    def label(self):
        return self._label

    @mountpoint.setter
    def label(self, label):
        if self._label != label:
            self._label = label

if sys.platform.startswith('linux'):
    def list_filesystems():
        p = subprocess.run(["lsblk", "--json", "--list", "--fs"],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                        check=True, universal_newlines=True)
        assert type(p) is subprocess.CompletedProcess
        
        class FilesystemInfoDecoder(json.JSONDecoder):
            def __init__(self, *args, **kargs):
                json.JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kargs)
            
            def dict_to_object(self, dct):
                if 'blockdevices' not in dct:
                    return dct
                
                fs_lst = dct.pop('blockdevices')
                try:
                    fs_nfo_lst = []
                    for fs in fs_lst:
                        uuid       = fs["uuid"]       if "uuid"       in fs else None
                        name       = fs["name"]       if "name"       in fs else None
                        fstype     = fs["fstype"]     if "fstype"     in fs else None
                        mountpoint = fs["mountpoint"] if "mountpoint" in fs else None
                        label      = fs["label"]      if "label"      in fs else None
                        
                        fs_nfo = FilesystemInfo()
                        fs_nfo.uuid       = uuid
                        fs_nfo.name       = name
                        fs_nfo.fstype     = fstype
                        fs_nfo.mountpoint = mountpoint
                        fs_nfo.label      = label
                        
                        fs_nfo_lst.append(fs_nfo)
                    return fs_nfo_lst
                except:
                    logging.exception('unexpected json')
                    dct['blockdevices'] = fs_lst
                    return dct
        
        fs_nfo_lst = json.loads(p.stdout, cls=FilesystemInfoDecoder)
        assert(type(fs_nfo_lst) is list and len(fs_nfo_lst) > 1 and type(fs_nfo_lst[0]) is FilesystemInfo)
        return fs_nfo_lst
