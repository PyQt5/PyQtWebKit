#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2022年7月24日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: build
@description: 

# install lib  apt or yum
sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev freeglut3-dev -y
sudo yum install mesa-* freeglut* -y
"""
import argparse
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from py7zr import SevenZipFile
from py7zr.callbacks import ExtractCallback
from tarfile import TarFile

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2022 Irony'
__Version__ = 1.0

SIP_NAME = 'sip-4.19.25'
PYQT_NAME = 'PyQt5-5.15.2'

SIP_URL = 'https://www.riverbankcomputing.com/static/Downloads/sip/4.19.25/sip-4.19.25.tar.gz'
PYQT_URL = 'https://files.pythonhosted.org/packages/28/6c/640e3f5c734c296a7193079a86842a789edb7988dca39eab44579088a1d1/PyQt5-5.15.2.tar.gz'

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
parser.add_argument('-b',
                    '--build',
                    default=None,
                    metavar='[sip or pyqt5]',
                    type=str.lower,
                    required=True,
                    help='Build Target')
parser.add_argument('--qmake', default='', help='qmake tools')
parser.add_argument('--delete',
                    default='True',
                    type=str,
                    help='Delete src files')

args = parser.parse_args()

assert args.build in ('sip', 'pyqt5')

print('Platform:', args.platform)
print('Arch:', args.arch)
make = 'make'
if args.platform == 'Windows':
    make = 'nmake'
print('Make:', make)
print('Build:', args.build)
print('Qmake:', args.qmake)
args.delete = (args.delete == 'True')
print('Del:', args.delete)

os.makedirs('tmp/PyQt5/Qt', exist_ok=True)
os.makedirs('src', exist_ok=True)


class DecompressCallback(ExtractCallback):

    def report_start_preparation(self):
        """report a start of preparation event such as making list of files and looking into its properties."""
        pass  # noqa

    def report_start(self, processing_file_path, processing_bytes):
        """report a start event of specified archive file and its input bytes."""
        print(processing_file_path, processing_bytes)

    def report_end(self, processing_file_path, wrote_bytes):
        """report an end event of specified archive file and its output bytes."""
        print(processing_file_path, wrote_bytes)

    def report_warning(self, message):
        """report an warning event with its message"""
        pass  # noqa

    def report_postprocess(self):
        """report a start of post processing event such as set file properties and permissions or creating symlinks."""
        pass  # noqa


def decompressLib():
    # 解压库文件
    if args.delete:
        try:
            shutil.rmtree('tmp', ignore_errors=True)
            os.makedirs('tmp/PyQt5/Qt', exist_ok=True)
        except Exception as e:
            print('remove ', 'tmp', e)

    if os.path.exists('tmp/PyQt5/Qt/bin'):
        return

    qt_path = subprocess.check_output(
        ['qmake', '-query', 'QT_INSTALL_PREFIX']).decode('utf-8').strip()
    print('qt_path:', qt_path)

    if args.platform == 'Windows':
        with SevenZipFile(
                'QtWebKit/qtwebkit-Windows-Windows_10-MSVC2017-Windows-Windows_10-X86{}.7z'
                .format('_64' if args.arch == 'x64' else ''), 'r') as tf:
            tf.extractall(path=qt_path, callback=DecompressCallback())
        with SevenZipFile(
                'QtWebKit/qtwebkit-Windows-Windows_10-MSVC2017-Windows-Windows_10-X86{}.7z'
                .format('_64' if args.arch == 'x64' else ''), 'r') as tf:
            tf.extractall(path='tmp/PyQt5/Qt', callback=DecompressCallback())
    elif args.platform == 'Linux':
        with SevenZipFile(
                'QtWebKit/qtwebkit-Linux-RHEL_7_6-GCC-Linux-RHEL_7_6-X86_64.7z',
                'r') as tf:
            tf.extractall(path=qt_path, callback=DecompressCallback())
        with SevenZipFile(
                'QtWebKit/qtwebkit-Linux-RHEL_7_6-GCC-Linux-RHEL_7_6-X86_64.7z',
                'r') as tf:
            tf.extractall(path='tmp/PyQt5/Qt', callback=DecompressCallback())
    elif args.platform == 'MacOS':
        with SevenZipFile(
                'QtWebKit/qtwebkit-MacOS-MacOS_10_13-Clang-MacOS-MacOS_10_13-X86_64.7z',
                'r') as tf:
            tf.extractall(path=qt_path, callback=DecompressCallback())
        with SevenZipFile(
                'QtWebKit/qtwebkit-MacOS-MacOS_10_13-Clang-MacOS-MacOS_10_13-X86_64.7z',
                'r') as tf:
            tf.extractall(path='tmp/PyQt5/Qt', callback=DecompressCallback())
    else:
        raise Exception('platform error')

    paths = ['include', 'mkspecs']
    if args.platform == 'Windows':
        paths.append('lib')
        paths.append('bin/Qt5WebKitd.dll')
        paths.append('bin/Qt5WebKitWidgetsd.dll')
    else:
        paths.append('lib/cmake')
        paths.append('lib/pkgconfig')
    for d in paths:
        path = os.path.join('tmp/PyQt5/Qt', d)
        try:
            shutil.rmtree(path, ignore_errors=True)
        except Exception as e:
            print('remove ', path, e)


def buildSip():
    # 编译sip
    src_dir = 'src/{}'.format(SIP_NAME)
    src_tar = 'src/{}.tar.gz'.format(SIP_NAME)

    if args.delete:
        try:
            shutil.rmtree(src_dir, ignore_errors=True)
        except Exception as e:
            print('remove ', src_dir, e)

        def reporthook(a, b, c):
            per = 100.0 * a * b / c
            if per > 100:
                per = 100
            print('download %s %.2f%%' % (src_tar, per))

        if not os.path.isfile(src_tar):
            urllib.request.urlretrieve(SIP_URL, src_tar, reporthook)

        with TarFile.open(src_tar, 'r:*') as tf:
            tf.extractall(path='src')

        print('extractall sip ok')

    # 切换目录
    os.chdir(src_dir)

    try:
        retcode = subprocess.check_call(sys.executable +
                                        ' configure.py && {0}'.format(make),
                                        shell=True,
                                        stderr=subprocess.STDOUT)
        print('retcode:', retcode)
        assert retcode == 0
        print('\nbuild sip ok\n')
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(-1)


def buildPyQt5():
    # 编译PyQt5 QtWebkit
    src_dir = 'src/{}'.format(PYQT_NAME)
    src_tar = 'src/{}.tar.gz'.format(PYQT_NAME)
    if args.delete:
        try:
            shutil.rmtree(src_dir, ignore_errors=True)
        except Exception as e:
            print('remove ', src_dir, e)

        def reporthook(a, b, c):
            per = 100.0 * a * b / c
            if per > 100:
                per = 100
            print('download %s %.2f%%' % (src_tar, per))

        if not os.path.isfile(src_tar):
            urllib.request.urlretrieve(PYQT_URL, src_tar, reporthook)

        with TarFile.open(src_tar, 'r:*') as tf:
            tf.extractall(path='src')

        print('extractall PyQt5 ok')

    # 拷贝补丁文件
    print('src_dir:', src_dir)
    for p in Path('patchs').rglob('*.sip'):
        dfile = os.path.join(src_dir, str(p).replace('\\', '/')[7:])
        print('copy', p, 'to', dfile)
        shutil.copy(str(p), dfile)

    os.chdir(src_dir)

    try:
        cmd = '{0} configure.py ' \
              '--confirm-license ' \
              '--verbose ' \
              '--no-designer-plugin ' \
              '--no-qml-plugin ' \
              '--no-tools ' \
              '--disable=dbus ' \
              '--disable=QAxContainer ' \
              '--disable=QtAndroidExtras ' \
              '--disable=QtBluetooth ' \
              '--disable=QtCore ' \
              '--disable=QtDBus ' \
              '--disable=QtDesigner ' \
              '--disable=Enginio ' \
              '--disable=QtGui ' \
              '--disable=QtHelp ' \
              '--disable=QtLocation ' \
              '--disable=QtMacExtras ' \
              '--disable=QtMultimedia ' \
              '--disable=QtMultimediaWidgets ' \
              '--disable=QtNetworkAuth ' \
              '--disable=QtNfc ' \
              '--disable=QtOpenGL ' \
              '--disable=QtPositioning ' \
              '--disable=QtQml ' \
              '--disable=QtQuick ' \
              '--disable=QtQuickWidgets ' \
              '--disable=QtRemoteObjects ' \
              '--disable=QtSensors ' \
              '--disable=QtSerialPort ' \
              '--disable=QtSql ' \
              '--disable=QtSvg ' \
              '--disable=QtTest ' \
              '--disable=QtWebChannel ' \
              '--disable=QtWebSockets ' \
              '--disable=QtWidgets ' \
              '--disable=QtWinExtras ' \
              '--disable=QtX11Extras ' \
              '--disable=QtXml ' \
              '--disable=QtXmlPatterns ' \
              '--disable=_QOpenGLFunctions_1_0 ' \
              '--disable=_QOpenGLFunctions_1_1 ' \
              '--disable=_QOpenGLFunctions_1_2 ' \
              '--disable=_QOpenGLFunctions_1_3 ' \
              '--disable=_QOpenGLFunctions_1_4 ' \
              '--disable=_QOpenGLFunctions_1_5 ' \
              '--disable=_QOpenGLFunctions_2_0 ' \
              '--disable=_QOpenGLFunctions_2_1 ' \
              '--disable=_QOpenGLFunctions_3_0 ' \
              '--disable=_QOpenGLFunctions_3_1 ' \
              '--disable=_QOpenGLFunctions_3_2_Compatibility ' \
              '--disable=_QOpenGLFunctions_3_2_Core ' \
              '--disable=_QOpenGLFunctions_3_3_Compatibility ' \
              '--disable=_QOpenGLFunctions_3_3_Core ' \
              '--disable=_QOpenGLFunctions_4_0_Compatibility ' \
              '--disable=_QOpenGLFunctions_4_0_Core ' \
              '--disable=_QOpenGLFunctions_4_1_Compatibility ' \
              '--disable=_QOpenGLFunctions_4_1_Core ' \
              '--disable=_QOpenGLFunctions_4_2_Compatibility ' \
              '--disable=_QOpenGLFunctions_4_2_Core ' \
              '--disable=_QOpenGLFunctions_4_3_Compatibility ' \
              '--disable=_QOpenGLFunctions_4_3_Core ' \
              '--disable=_QOpenGLFunctions_4_4_Compatibility ' \
              '--disable=_QOpenGLFunctions_4_4_Core ' \
              '--disable=_QOpenGLFunctions_4_5_Compatibility ' \
              '--disable=_QOpenGLFunctions_4_5_Core ' \
              '--disable=_QOpenGLFunctions_ES2 ' \
              '--disable=pylupdate ' \
              '--disable=pyrcc ' \
              '--sip-incdir={1} ' \
              '--sip={2} ' \
              '{3} && {4} -j 16'.format(
            sys.executable,
            os.path.abspath('../{0}/siplib/'.format(SIP_NAME)),
            os.path.abspath(
                '../{0}/sipgen/sip{1}'.format(SIP_NAME,
                                                  '.exe' if args.platform == 'Windows' else '')),
            '--qmake={}'.format(args.qmake) if args.qmake else '',
            os.path.abspath(
                '../../tools/jom.exe') if args.platform == 'Windows' else 'make'
        )
        print('cmd:', cmd)
        retcode = subprocess.check_call(cmd,
                                        env=os.environ,
                                        shell=True,
                                        stderr=subprocess.STDOUT)
        print('retcode:', retcode)
        assert retcode == 0
        print('\nbuild PyQt5 QtWebkit ok\n')
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(-1)

    ext = 'pyd' if args.platform == 'Windows' else 'so'

    # 复制QtWebkit pyd
    fsrc = 'QtWebKitWidgets/QtWebKitWidgets.{0}'.format(ext)
    fdst = '../../tmp/PyQt5/QtWebKitWidgets.{0}'.format(ext)
    if os.path.exists(fsrc):
        shutil.copyfile(fsrc, fdst)
    else:
        print('QtWebKitWidgets not found')
        sys.exit(-1)

    fsrc = 'QtWebKit/QtWebKit.{0}'.format(ext)
    fdst = '../../tmp/PyQt5/QtWebKit.{0}'.format(ext)
    if os.path.exists(fsrc):
        shutil.copyfile(fsrc, fdst)
    else:
        print('QtWebKit not found')
        sys.exit(-1)


if args.build == 'sip':
    buildSip()
if args.build == 'pyqt5':
    decompressLib()
    buildPyQt5()
