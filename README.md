# PY-ACR122U

[![PyPI - Version](https://img.shields.io/pypi/v/py122u)](https://pypi.org/project/py122u/)
[![PyPI - License](https://img.shields.io/pypi/l/py122u)](https://pypi.org/project/py122u/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py122u)](https://pypi.org/project/py122u/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py122u)](https://pypi.org/project/py122u/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/py122u)](https://pypi.org/project/py122u/)

This is a python library for the ACR122U NFC reader

## Installation

```shell
pip install py122u
```

## Usage

```python

from py122u import nfc

reader = nfc.Reader()
reader.connect()
reader.print_data(reader.get_uid())
reader.info()
```
