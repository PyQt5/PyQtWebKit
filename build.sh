#!/bin/bash

echo "you must to be install python3 and install Qt5.13.1 to ~/Qt5.13.1"

# install lib  apt or yum
sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev freeglut3-dev -y
sudo yum install mesa-* freeglut* -y

# copy webkit
cp -rf Linux/x64/PyQt5/Qt/* ~/Qt5.13.1/5.13.1/gcc_64/
pushd ~/Qt5.13.1/5.13.1/gcc_64/lib/
ln -s libQt5WebKit.so.5.212.0 libQt5WebKit.so
ln -s libQt5WebKit.so.5.212.0 libQt5WebKit.so.5
ln -s libQt5WebKitWidgets.so.5.212.0 libQt5WebKitWidgets.so
ln -s libQt5WebKitWidgets.so.5.212.0 libQt5WebKitWidgets.so.5
popd

# install PyQt5
su
python3 -m pip install PyQt5 -U
exit

# build sip
python3 build.py --platform=Linux --arch=x64 --build=sip --qmake=~/Qt5.13.1/5.13.1/gcc_64/bin/qmake

# build PyQt5 Webkit
export PATH=~/Qt5.13.1/5.13.1/gcc_64/bin:$PATH
python3 build.py --platform=Linux --arch=x64 --build=PyQt5

# make whl
python3 mkdist.py --platform=Linux --arch=x64 --version=5.13.0

# test
su
python3 test.py --platform=Linux --arch=x64 --version=5.13.0
exit

# if you see <class 'PyQt5.QtWebKit.QWebSettings'> and <class 'PyQt5.QtWebKitWidgets.QWebView'>
# it's ok
