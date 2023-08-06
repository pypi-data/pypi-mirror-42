# print_msg module 

![Python 3.4, 3.5, 3.6, 3.7](https://img.shields.io/pypi/pyversions/print-msg.svg)
![pypi version](https://img.shields.io/pypi/v/print-msg.svg)
![requirements](https://img.shields.io/requires/github/shvetsovdmitry/print-msg.svg)

![wheel](https://img.shields.io/pypi/wheel/print-msg.svg)
![license](https://img.shields.io/github/license/shvetsovdmitry/print-msg.svg) 
![commit activity](https://img.shields.io/github/commit-activity/m/shvetsovdmitry/print-msg.svg)
![goto counter](https://img.shields.io/github/search/shvetsovdmitry/print-msg/goto.svg)

#### This module helps to print status messages in color depending on their content.

## Installation:
#### Github:
1. `$ git clone https://github.com/shvetsovdmitry/print-msg/`
2. `$ cd print-msg/`
3. `$ python3 setup.py sdist`
4. `$ cd dist/`
5. `$ sudo pip install print_msg-0.9.3.tar.gz`
#### pip:
`$ sudo pip install print-msg`

## Using:
```python
import print_msg

print_msg(status='%status_code%', msg='%message%', end='%optional%')
```

#### Status codes:
* *`'ok'`* -> `[--OK--] %Message%`;
* *`'error'`* -> `[-ERROR-] %Message%`;
* *`'status'`* -> `[STATUS] %Message%`;
* *`'time'`* -> `[-TIME-] Execution time -> %time%`;
