# Nested-multipart-parser

[![build](https://github.com/remigermain/nested-multipart-parser/actions/workflows/main.yml/badge.svg)](https://github.com/remigermain/nested-multipart-parser/actions/workflows/main.yml)
[![pypi](https://img.shields.io/pypi/v/nested-multipart-parser)](https://pypi.org/project/nested-multipart-parser/)

Parser for nested data for '*multipart/form*', you can use it in any python project, or use the Django Rest Framework integration.

# Installation:

```bash
pip install nested-multipart-parser
```

# Usage:

```python
from nested_multipart_parser import NestedParser

options = {
	"separator": "bracket"
}

def my_view():
	# `options` is optional
	parser = NestedParser(data, options)
	if parser.is_valid():
		validate_data = parser.validate_data
		...
	else:
		print(parser.errors)

```

### Django Rest Framework

```python
from nested_multipart_parser.drf import DrfNestedParser
...

class YourViewSet(viewsets.ViewSet):
	parser_classes = (DrfNestedParser,)
```


## What it does:

The parser take the request data and transform it to a Python dictionary:

example:

```python
# input:
{
	'title': 'title',
	'date': "time",
	'simple_object.my_key': 'title'
	'simple_object.my_list[0]': True,
	'langs[0].id': 666,
	'langs[0].title': 'title',
	'langs[0].description': 'description',
	'langs[0].language': "language",
	'langs[1].id': 4566,
	'langs[1].title': 'title1',
	'langs[1].description': 'description1',
	'langs[1].language': "language1"
}

# result:
 {
	'title': 'title',
	'date': "time",
	'simple_object': {
		'my_key': 'title',
		'my_list': [
			True
		]
	},
	'langs': [
		{
			'id': 666,
			'title': 'title',
			'description': 'description',
			'language': 'language'
		},
		{
			'id': 4566,
			'title': 'title1',
			'description': 'description1',
			'language': 'language1'
		}
	]
}
```

## How it works:

Attributes where sub keys are full numbers only are automatically converted into lists:

```python
	data = {
		'title[0]': 'my-value',
		'title[1]': 'my-second-value'
	}
	output = {
		'title': [
			'my-value',
			'my-second-value'
		]
	}

	# Be aware of the fact that you have to respect the order of the indices for arrays, thus 
    	'title[2]': 'my-value' # Invalid (you have to set title[0] and title[1] before)

    # Also, you can't create an array on a key already set as a prinitive value (int, boolean or string):
		'title': 42,
		'title[object]': 42 # Invalid
```



Attributes where sub keys are other than full numbers are converted into Python dictionary:

```python
	data = {
		'title.key0': 'my-value',
		'title.key7': 'my-second-value'
	}
	output = {
		'title': {
			'key0': 'my-value',
			'key7': 'my-second-value'
		}
	}
    

    # You have no limit for chained key:
	# with "mixed-dot" separator option (same as 'mixed' but with dot after list to object):
	data = {
		'the[0].chained.key[0].are.awesome[0][0]': 'im here !!'
	}
	# with "mixed" separator option:
	data = {
		'the[0]chained.key[0]are.awesome[0][0]': 'im here !!'
	}
	# With "bracket" separator option:
	data = {
		'the[0][chained][key][0][are][awesome][0][0]': 'im here !!'
	}
	# With "dot" separator option:
	data = {
		'the.0.chained.key.0.are.awesome.0.0': 'im here !!'
	}
```



For this to work perfectly, you must follow the following rules:

- A first key always need to be set. ex: `title[0]` or `title`. In both cases the first key is `title`

- For `mixed` or `mixed-dot` options, brackets `[]` is for list, and dot `.` is for object

- For `mixed-dot` options is look like `mixed` but with dot when object follow list

- For `bracket` each sub key need to be separate by brackets `[ ]` or with `dot` options `.`

- For `bracket` or `dot`options, if a key is number is convert to list else a object

- Don't put spaces between separators.

- By default, you can't set set duplicates keys (see options)
  
  

## Options

```python
{
	# Separators:
	# with mixed-dot:      article[0].title.authors[0]: "jhon doe"
	# with mixed:      article[0]title.authors[0]: "jhon doe"
	# with bracket:  article[0][title][authors][0]: "jhon doe"
	# with dot:      article.0.title.authors.0: "jhon doe"
	'separator': 'bracket' or 'dot' or 'mixed' or 'mixed-dot', # default is `mixed-dot`


	# raise a expections when you have duplicate keys
	# ex :
	# {
	#	"article": 42,
	#	"article[title]": 42,
	# }
	'raise_duplicate': True, # default is True

	# override the duplicate keys, you need to set "raise_duplicate" to False
	# ex :
	# {
	#	"article": 42,
	#	"article[title]": 42,
	# }
	# the out is
	# ex :
	# {
	#	"article"{
	# 		"title": 42,
	#	}
	# }
	'assign_duplicate': False # default is False
}
```

## Options for Django Rest Framwork:
```python

# settings.py
...

DRF_NESTED_MULTIPART_PARSER = {
	"separator": "mixed-dot",
	"raise_duplicate": True,
	"assign_duplicate": False,

	# output of parser is converted to querydict 
	# if is set to False, dict python is returned
	"querydict": True,
}
```

## JavaScript integration:

You can use this [multipart-object](https://github.com/remigermain/multipart-object) library to easy convert object to flat nested object formatted for this library

## License

[MIT](https://github.com/remigermain/multipart-object/blob/main/LICENSE)
