#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2022年7月24日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: mkdist
@description: 
"""
import argparse
import base64
import hashlib
import os
from pathlib import Path
import shutil
from zipfile import ZIP_DEFLATED, ZipFile

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2022'

parser = argparse.ArgumentParser()
parser.add_argument('-p',
                    '--platform',
                    default=None,
                    metavar='[Windows or Linux or MacOS]',
                    choices=['Windows', 'Linux', 'MacOS'],
                    required=True,
                    help='System platform')
parser.add_argument('-a',
                    '--arch',
                    default=None,
                    type=str.lower,
                    metavar='[x86 or x64]',
                    choices=['x86', 'x64'],
                    required=True,
                    help='System Arch')
parser.add_argument('-v',
                    '--version',
                    default=None,
                    type=str.lower,
                    required=True,
                    help='PyQt5 Version')
parser.add_argument('-t',
                    '--tags',
                    default=['cp35', 'cp36', 'cp37', 'cp38', 'cp39'],
                    nargs='+',
                    metavar='cp35 cp36 cp37 cp38 cp39',
                    help='Python version')

args = parser.parse_args()

assert args.version != None

print('Platform:', args.platform)
print('Arch:', args.arch)
print('Version:', args.version)
Name = 'PyQtWebKit'
print('Name:', Name)
print(args.tags)
Tags = '.'.join(args.tags)
print('Tags:', Tags)

# 创建描述信息目录
dist_info_dir = '{0}-{1}.dist-info'.format(Name, args.version)
os.makedirs(dist_info_dir, exist_ok=True)

info_files = []
# 遍历需要安装的文件
pyqt_dir_path = 'tmp'
for path in Path(os.path.join(pyqt_dir_path, 'PyQt5')).rglob('*'):
    if path.is_file():
        if '__pycache__' in str(path):
            continue
        info_files.append(path)

# 写入INSTALLER文件
path = os.path.join(dist_info_dir, 'INSTALLER')
info_files.append(Path(path))
with open(path, 'w') as fp:
    fp.write('pip\n')

# 写入METADATA文件
METADATA = """Metadata-Version: 1.0
Name: {Name}
Version: {Version}
Summary: Python bindings for the Qt WebKit library
Home-page: https://github.com/PyQt5/PyQtWebKit
Author: Irony
Author-email: 892768447@qq.com
License: GPL v3
Platform: UNIX
Platform: Windows
Platform: MacOS
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: 3.6
Classifier: Programming Language :: Python :: 3.7
Classifier: Programming Language :: Python :: 3.8
Classifier: Programming Language :: Python :: 3.9
Requires-Dist: PyQt5 (=={Version})

Installation
------------

pip install {Name}=={Version}

The wheels include a copy of the required parts of the LGPL version of Qt.

""".format(Name=Name, Version=args.version, Platform=args.platform)
path = os.path.join(dist_info_dir, 'METADATA')
info_files.append(Path(path))
with open(path, 'w') as fp:
    fp.write(METADATA)

# 写入RECORD文件
record_path = os.path.join(dist_info_dir, 'RECORD')
with open(record_path, 'w') as fp:
    for path in info_files:
        try:
            cpath = path.relative_to(pyqt_dir_path)
        except ValueError:
            cpath = path
        path = str(path)
        cpath = str(cpath).replace('\\', '/')

        # 计算文件的sha256
        data = open(path, 'rb').read()
        digest = base64.urlsafe_b64encode(
            hashlib.sha256(data).digest()).rstrip(b'=').decode('ascii')
        fp.write('{0},sha256={1},{2}\n'.format(cpath, digest, len(data)))
    fp.write('{0}/RECORD,,\n'.format(dist_info_dir))

info_files.append(Path(record_path))

# 写入WHEEL文件
if args.platform == 'Windows':
    Tag = '{0}-none{1}'.format(
        Tags, '-win32'
        if args.arch == 'x86' else '-win_amd64' if args.arch == 'x64' else '')
elif args.platform == 'Linux':
    Tag = '{0}-none-manylinux1_x86_64'.format(Tags)
elif args.platform == 'MacOS':
    Tag = '{0}-none-macosx_10_13_intel'.format(Tags)

WHEEL = """Wheel-Version: 1.0
Generator: Irony
Root-Is-Purelib: false
Tag: {0}

""".format(Tag)
path = os.path.join(dist_info_dir, 'WHEEL')
info_files.append(Path(path))
with open(path, 'w') as fp:
    fp.write(WHEEL)

print('wirte dist info ok')

# 生成whl文件
os.makedirs('dist', exist_ok=True)
dist_file = os.path.join('dist',
                         '{0}-{1}-{2}.whl'.format(Name, args.version, Tag))
print('make {0}'.format(dist_file))
zipfp = ZipFile(dist_file, 'w', ZIP_DEFLATED)
for path in info_files:
    try:
        cpath = path.relative_to(pyqt_dir_path)
    except ValueError:
        cpath = path
    path = str(path)
    cpath = str(cpath).replace('\\', '/')
    zipfp.write(str(path), str(cpath))
zipfp.close()

try:
    shutil.rmtree(dist_info_dir)
except Exception as e:
    print(e)
print('make dist file ok')
