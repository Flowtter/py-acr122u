# PY-ACR122U


![PyPI - License](https://img.shields.io/pypi/v/py-acr122u)
![PyPI - License](https://img.shields.io/pypi/l/py-acr122u)
![PyPI - License](https://img.shields.io/pypi/dm/py-acr122u)
![PyPI - License](https://img.shields.io/pypi/pyversions/py-acr122u)
![PyPI - License](https://img.shields.io/pypi/wheel/py-acr122u)



This is a python library for the ACR122U NFC reader

## Installation
- git clone https://github.com/Flowtter/py-acr122u.git
- cd py-acr122u
- pip install -r requirements.txt

## Usage

```python

from py_acr122u import nfc

reader = nfc.Reader()
reader.print_data(reader.get_uid())
reader.info()
```
- python main.py
