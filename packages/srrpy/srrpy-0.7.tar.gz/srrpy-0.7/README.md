# srrpy
Simple Remote Run Python/Script

Introduction
------

Base for Redis , is a run in-memory key value data structure server .
SRRPY is like RPC that C/S mode who redis transport data .

Install
------

Source
------

Debian/Ubuntu

```bash
sudo apt install virtualenv redis-server redis-tools -y

git clone https://github.com/heysion/srrpy.git && cd srrpy

virtualenv --system-site-packages -p python3 run-test

source run-test/bin/activate

pip install -r requirements.txt

```

Pip
------

Debian/Ubuntu

```bash
sudo apt install virtualenv redis-server redis-tools -y

pip install srrpy
```

test
-----

### run server

```bash
cd tests
python3 test-server.py
```

### run client

```bash
cd tests
python3 test-client.py
```


Example
------

### client

```python
import redis
from srrpy import TemplatesInterface
from srrpy import Client
import logging
import sys

__meta__data__ = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
{% for mod in import_modules %}
import {{ mod }}
{% endfor %}

def run_test(a,b):
    print("a + b = %d"%(a+b))

run_test({% for item in list_args -%} {{ item[0] }} = {{ item[1] }} {%- if loop.index == list_args|length -%} {%- else %} , {% endif %} {%- endfor %})

'''

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class MyTemplate(TemplatesInterface):
    name = "mytemplate"
    metadata = __meta__data__


db = redis.Redis()

test_client = Client(db,queue="test",5,codec="json",templates=MyTemplate())
test_client.call(import_modules=["sys","os"],list_args={("a",10),("b",3)},execute="exec")

```


### server

```python

import redis
from srrpy import Server
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

db = redis.Redis()

test_server = Server(db,queue="test",timeout=5,codec="json")

test_server.run()

```
