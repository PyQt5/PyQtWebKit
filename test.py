#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月10日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: test
@description: 
"""
import argparse
import os
import sys


try:
    from pip._internal import main as _main  # @UnusedImport
except:
    from pip import main as _main  # @Reimport @UnresolvedImport


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--platform', default=None,
                    metavar='[Windows or Linux]',
                    choices=['Windows', 'Linux'],
                    required=True, help='System platform')
parser.add_argument('-a', '--arch', default=None, type=str.lower,
                    metavar='[x86 or x64]',
                    choices=['x86', 'x64'],
                    required=True, help='System Arch')
parser.add_argument('-v', '--version', default=None, type=str.lower,
                    required=True, help='PyQt5 Version')
parser.add_argument('-t', '--tags', default=['cp35', 'cp36', 'cp37', 'cp38'], nargs='+',
                    metavar='cp35 cp36 cp37 cp38', help='Python version')

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

if args.platform == 'Windows':
    Tag = '{0}-none{1}'.format(Tags, 
        '-win32' if args.arch == 'x86' else '-win_amd64' if args.arch == 'x64' else '')
elif args.platform == 'Linux':
    Tag = '{0}-abi3-manylinux1_x86_64'.format(Tags)
else:
    Tag = '{0}-none'.format(Tags)

_main(['install', os.path.abspath(
    'dist/{0}-{1}-{2}.whl'.format(Name, args.version, Tag))])

# 加载模块是否正常
try:
    from PyQt5 import QtCore
    print(QtCore)
    print(QtCore.PYQT_VERSION_STR)
    print(QtCore.QT_VERSION_STR)
    from PyQt5.QtWebKit import QWebSettings
    from PyQt5.QtWebKitWidgets import QWebView
    print(QWebSettings)
    print(QWebView)
except Exception as e:
    print(e)
    sys.exit(-1)
