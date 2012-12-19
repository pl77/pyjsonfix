pyjsonfix
=========

pyjsonfix tries to "fix" broken JSON. 

JSON is actually a subset of JavaScript object literals. And more often than not, it isn't valid JSON. 
If you want to use the [json module](http://docs.python.org/2/library/json.html), it's not going to work.
That's where pyjsonfix is useful. It'll try to coax it into a useable form.

Please note, it hasn't been extensively tested, so I don't know what it'll break on. It's been pretty good with what I've come across.

## Example
	Valid javascript, invalid json:
		{'ca"ke': 5.05, pie:[0,0xb,,2,{foo:"foob",bar:'barb'}], null:null, false:true, ' ':true, "'":false, 010: 4,  l3l :  10  }

	Fixed json:
		{"ca\"ke": 5.05, "pie":[0,11,null,2,{"foo":"foob","bar":"barb"}], "null":null, "false":true, " ":true, "'":false, "8": 4,  "l3l":  10  }

	To python:
		{u' ': True, u'false': True, u"'": False, u'l3l': 10, u'pie': [0, 11, None, 2, {u'foo': u'foob', u'bar': u'barb'}], u'ca"ke': 5.05, u'8': 4, u'null': None}

