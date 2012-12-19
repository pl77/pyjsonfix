pyjsonfix
=========

pyjsonfix tries to "fix" broken JSON. 

JSON is actually a subset of JavaScript object literals. And more often than not, it isn't valid JSON. 
If you want to use the [json module](http://docs.python.org/2/library/json.html), it's not going to work.
That's where pyjsonfix is useful. It'll try to coax it into a useable form.

Please note, it hasn't been extensively tested, so I don't know what it'll break on. It's been pretty good with what I've come across.

## Example
```python
bad_json = """{'ca"ke': 5.05, pie:[0,0xb,,2,{foo:"foob",bar:'barb'}], 
	null:null, false:true, ' ':true, "'":false, 010: 4,  l3l :  10  }"""

from jsonfix import fixJSON

fixed_json = fixJSON(bad_json)
print fixed_json
# {"ca\"ke": 5.05, "pie":[0,11,null,2,{"foo":"foob","bar":"barb"}], 
#     "null":null, "false":true, " ":true, "'":false, "8": 4,  "l3l":  10  }

import json
from pprint import pprint
pprint(json.loads(fixed_json))
# {u' ': True,
# u"'": False,
# u'8': 4,
# u'ca"ke': 5.05,
# u'false': True,
# u'l3l': 10,
# u'null': None,
# u'pie': [0, 11, None, 2, {u'bar': u'barb', u'foo': u'foob'}]}
```
