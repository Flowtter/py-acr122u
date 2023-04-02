# PY-ACR122U

[![PyPI - Version](https://img.shields.io/pypi/v/py-acr122u)](https://pypi.org/project/py-acr122u/)
[![PyPI - License](https://img.shields.io/pypi/l/py-acr122u)](https://pypi.org/project/py-acr122u/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py-acr122u)](https://pypi.org/project/py-acr122u/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-acr122u)](https://pypi.org/project/py-acr122u/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/py-acr122u)](https://pypi.org/project/py-acr122u/)

This is a python library for the ACR122U NFC reader

## Installation

```shell
pip install py-acr122u
```

## Usage

```python

from py_acr122u import nfc

reader = nfc.Reader()
reader.connect()
reader.print_data(reader.get_uid())
reader.info()
```
