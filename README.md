# PyQtWebKit

QtWebKit for PyQt 5.15.2

## Install

pip install PyQtWebKit==5.15.2

## Buiding

pip3 install py7zr

- Windows
  - run `vcvars32.bat`
  - run `qtenv2.bat`
  - `python build.py -p Windows -a x86 -b sip`
  - `python build.py -p Windows -a x86 -b PyQt5`
  - `python mkdist.py -p Windows -a x86 -v 5.15.2`
  - `python test.py -p Windows -a x86 -v 5.15.2`

- Linux
  - `export PATH=${QMAKE_PATH}:$PATH`
  - `python build.py -p Linux -a x64 -b sip`
  - `python build.py -p Linux -a x64 -b PyQt5`
  - `python mkdist.py -p Linux -a x64 -v 5.15.2`
  - `python test.py -p Linux -a x64 -v 5.15.2`

- MacOS
  - `export PATH=${QMAKE_PATH}:$PATH`
  - `python build.py -p MacOS -a x64 -b sip`
  - `python build.py -p MacOS -a x64 -b PyQt5`
  - `python mkdist.py -p MacOS -a x64 -v 5.15.2`
  - `python test.py -p MacOS -a x64 -v 5.15.2`

## Thanks

[https://github.com/qtwebkit/qtwebkit/releases](https://github.com/qtwebkit/qtwebkit/releases)