#!/usr/bin/env python3

# Copyright (c) 2019 Jakob Meng, <jakobmeng@web.de>

import logging
import datetime
import os
import sys
import subprocess
from xml.etree import ElementTree
from .os import list_filesystems
from typing import List
import shutil
from .process import run_live
import json

if sys.platform.startswith('linux'):
    class SnapshotInfo(object):
        def __init__(
            self,
            path : str = None,
            type_ : str = None,
            num : int = None,
            date : datetime.datetime = None,
            description : str = None,
            cleanup : str = None
        ):
            self._path = path
            self._type_ = type_
            self._num = num
            self._date = date
            self._description = description
            self._cleanup = cleanup

        def __str__(self):
            return '{{path:{}; type:{}; num:{}; date:{}; description:{}; cleanup:{}}}'.format(
                self._path, self._type_, self._num, self._date, self._description, self._cleanup)
        
        @property
        def path(self):
            return self._path

        @path.setter
        def path(self, path):
            if self._path != path:
                self._path = path
        
        @property
        def type_(self):
            return self._type_

        @type_.setter
        def type_(self, type_):
            if self._type_ != type_:
                self._type_ = type_
                
        @property
        def num(self):
            return self._num

        @num.setter
        def num(self, num):
            if self._num != num:
                self._num = num
                
        @property
        def date(self):
            return self._date

        @date.setter
        def date(self, date):
            if self._date != date:
                self._date = date
                
        @property
        def description(self):
            return self._description

        @description.setter
        def description(self, description):
            if self._description != description:
                self._description = description
        
        @property
        def cleanup(self):
            return self._cleanup

        @cleanup.setter
        def cleanup(self, cleanup):
            if self._cleanup != cleanup:
                self._cleanup = cleanup
    
    class SnapshotBackupInfo(object):
        def __init__(
            self,
            mountpoint      : str,
            backup_dir      : str,
            tag             : str       = None,
            includes        : List[str] = None,
            excludes        : List[str] = None
        ):
            self._mountpoint = mountpoint
            self._backup_dir = backup_dir
            self._tag = tag
            self._includes = includes
            self._excludes = excludes

        def __str__(self):
            return '{{mountpoint:{}; type:{}; tag:{}; includes:{}; excludes:{}}}'.format(
                self._mountpoint, self._backup_dir, self._tag, self._includes, self._excludes)
        
        @property
        def mountpoint(self):
            return self._mountpoint

        @mountpoint.setter
        def mountpoint(self, mountpoint):
            if self._mountpoint != mountpoint:
                self._mountpoint = mountpoint
        
        @property
        def backup_dir(self):
            return self._backup_dir

        @backup_dir.setter
        def backup_dir(self, backup_dir):
            if self._backup_dir != backup_dir:
                self._backup_dir = backup_dir
                
        @property
        def tag(self):
            return self._tag

        @tag.setter
        def tag(self, tag):
            if self._tag != tag:
                self._tag = tag
                
        @property
        def includes(self):
            return self._includes

        @includes.setter
        def includes(self, includes):
            if self._includes != includes:
                self._includes = includes
                
        @property
        def excludes(self):
            return self._excludes

        @excludes.setter
        def excludes(self, excludes):
            if self._excludes != excludes:
                self._excludes = excludes
    
    class SnapshotBackupInfoEncoder(json.JSONEncoder):
        def default(self, obj):
            if not isinstance(obj, SnapshotBackupInfo):
                # Let the base class default method raise the TypeError
                return json.JSONEncoder.default(self, obj)
            
            return {
                '__type__'   : 'pywana.snapper.SnapshotBackupInfo',
                'mountpoint' : obj.mountpoint,
                'backup_dir' : obj.backup_dir,
                'tag'        : obj.tag,
                'includes'   : json.dumps(obj.includes),
                'excludes'   : json.dumps(obj.excludes)
            }
    
    def read_snapshot_info(snapshot_path : str):
        info_xml_path = os.path.join(snapshot_path, 'info.xml')
        info_xml = ElementTree.parse(info_xml_path)
        root = info_xml.getroot()
        
        path        = snapshot_path
        type_       = root.find('type').text
        num         = root.find('num').text
        date        = root.find('date').text
        description = root.find('description').text
        cleanup     = root.find('cleanup').text
        
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") if date is not None else None
        return SnapshotInfo(path, type_, num, date, description, cleanup)
    
    
    def list_snapshots(mountpoint : str):
        snp_lst = []
        snp_parent_dir = os.path.join(mountpoint, '.snapshots')
        for snp_dir in os.listdir(snp_parent_dir):
            snp_path = os.path.join(snp_parent_dir, snp_dir)
            snp_lst.append(read_snapshot_info(snp_path))
        return snp_lst

    class InvalidMountpointError(Exception):
        pass
    
    class NotALinkError(Exception):
        pass
    
    def backup_snapshot(
        from_mountpoint : str,
        to_dir          : str,
        tag             : str       = None,
        includes        : List[str] = None,
        excludes        : List[str] = None,
        dry_run         : bool      = False,
        overwrite       : bool      = False
    ):
        fs = next((fs for fs in list_filesystems() if fs.mountpoint == from_mountpoint), None)
        
        if fs is None:
            raise InvalidMountpointError('\'{}\' is not a mountpoint'.format(from_mountpoint))
        
        if fs.fstype != 'btrfs':
            logging.warning('{} is not a btrfs filesystem'.format(from_mountpoint))
        
        if not os.path.isdir(to_dir):
            raise NotADirectoryError('{} is not a directory'.format(to_dir))
        
        if not os.access(to_dir, os.W_OK):
            raise PermissionError('{} is not writeable'.format(to_dir))
        
        if tag is None:
            if fs.uuid is None:
                raise ValueError('No tag given and filesystem {} has no valid uuid'.format(from_mountpoint))
            
            logging.debug('tag is {}'.format(fs.uuid))
            tag = fs.uuid
        
        snp_lst = list_snapshots(from_mountpoint)
        if not snp_lst:
            raise FileNotFoundError('No snapshots found for {}'.format(from_mountpoint))
        
        logging.debug('Found snapshots {}'.format([str(x) for x in snp_lst]))
        
        # take latest snapshot
        lst_by_date = sorted(snp_lst, key=lambda snp: snp.date)
        snp = lst_by_date[-1]
        
        bak_name = 'snapshot_of_uuid_{}_num_{}_date_{}'.format(fs.uuid, snp.num, snp.date.strftime('%Y%m%d%H%M%S'))
        bak_path = os.path.join(to_dir, bak_name)
        
        last_bak_name = 'snapshot_of_uuid_{}_LAST'.format(fs.uuid)
        last_bak_path = os.path.join(to_dir, last_bak_name)
        
        if os.path.exists(bak_path):
            if not overwrite:
                logging.warning('Backup dir {} already exists'.format(bak_path))
                return False
            logging.warning('Overwriting existing backup dir {}'.format(bak_path))
        
        if os.path.lexists(last_bak_path) and not os.path.islink(last_bak_path):
            raise NotALinkError('{} is not a link'.format(last_bak_path))
        
        if os.path.lexists(last_bak_path) and not os.path.exists(last_bak_path):
            logging.warning('Removing broken symlink {}'.format(last_bak_path))
            if not dry_run:
                os.unlink(last_bak_path)
        
        logging.info('Doing backup of snapshot {} to {}'.format(snp, bak_path))
        
        # make backup dir
        assert(overwrite if os.path.exists(bak_path) else True)
        if not os.path.exists(bak_path):
            if not dry_run:
                os.mkdir(bak_path)
        
        # write backup info first
        bak_nfo_path = os.path.join(bak_path, 'backup_info.json')
        bak_nfo = SnapshotBackupInfo(from_mountpoint, to_dir, tag, includes, excludes)
        bak_nfo_json = json.dumps(bak_nfo, cls=SnapshotBackupInfoEncoder, 
                                  sort_keys=True, indent=4, separators=(',', ': '))
        logging.debug('Writing backup info to {}: {}'.format(bak_nfo_path, bak_nfo_json))
        if not dry_run:
            with open(bak_nfo_path, 'w' if overwrite else 'x') as f:
                f.write(bak_nfo_json)
        
        # run rsync commands next
        default_cmd = ['rsync', '--stats', '--human-readable', '-vaHAX', '--one-file-system']
        
        if dry_run:
            default_cmd.append('--dry-run')
        
        def log_run(args):
            try:
                p = run_live(args,check=True)
            except subprocess.CalledProcessError as e:
                logging.exception('Command failed with exit code {}'.format(e.returncode))
                raise
            assert(type(p) is subprocess.CompletedProcess)
            logging.info('Command exited with code {}'.format(p.returncode))
            logging.debug('stdout:\n{}'.format(p.stdout))
            logging.debug('stderr:\n{}'.format(p.stderr))
        
        # rsync snapshot metadata
        meta_cmd = default_cmd.copy()
        meta_cmd.extend(['{}/'.format(snp.path), '{}/'.format(bak_path)])
        meta_cmd.extend(['--exclude', '/snapshot'])
        log_run(meta_cmd)
        
        # rsync snapshot data
        data_cmd = default_cmd.copy()
        data_cmd.extend(['{}/snapshot/'.format(snp.path), '{}/snapshot/'.format(bak_path)])
        
        if os.path.exists(last_bak_path):
            data_cmd.append('--link-dest={}/'.format(last_bak_path))
        
        if includes:
            for include in includes:
                data_cmd.extend(['--include', include])
        
        if excludes:
            for exclude in excludes:
                data_cmd.extend(['--exclude', exclude])
        
        log_run(data_cmd)
        
        # renew symlink to last backup
        if not dry_run:
            if os.path.lexists(last_bak_path):
                os.unlink(last_bak_path)
            os.symlink(bak_path, last_bak_path, target_is_directory=True)
        logging.debug('Created new symlink from {} to {}'.format(bak_path, last_bak_path))
        
        return True
