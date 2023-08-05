# waddle
the penguins api and tooling around aws's parameter store
![codebuild](https://codebuild.us-east-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiUU82MEFwb2JTUzJ2OFJSOUI4eURSc01BNnBNb04zVTRvaUZxTERxb3U3Ui9HdkVJRUllOHBUdlNXVGpGVXpUeXllVkVncVE4cDIxcFBIMzh6SFFMUWFzPSIsIml2UGFyYW1ldGVyU3BlYyI6IkJlcmc3clNIbVVBaFRCWFUiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

## Bunch

A class that offers pathy semantics 
to access values in a dictionary.

### Bunch -- general usage
e.g.,

```python
from waddle import Bunch
values = {
    'a': {
        'b': {
            'c': True,
            'd': False,
        },        
    },
}
a = Bunch(values)
assert a.b.c == True
assert a.b.d == False
a.cat.name = 'mycat'
assert a['cat.name'] == 'mycat'
assert 'cat.age' in a == False
assert a.get('cat.age', 22) == 22
assert a.setdefault('cat.age', 45) == 45
``` 

### Bunch -- env

You can use the built-in `env` function to use
the dictionary as a set of default values that
can be overridden by environment variables.

e.g.,

```python
import os
from waddle import Bunch
os.environ['FTP_PASSWORD'] = 'password'
config = {
    'ftp': {
        'host': '127.0.0.1',
        'user': 'user',
    }
}
config = Bunch(config)
env = config.env()
assert env('FTP_PASSWORD') == 'password'
assert env('FTP_HOST') == '127.0.0.1'
```
