# Nested-multipart-parser

[![build](https://github.com/remigermain/nested-multipart-parser/actions/workflows/main.yml/badge.svg)](https://github.com/remigermain/nested-multipart-parser/actions/workflows/main.yml)
[![pypi](https://img.shields.io/pypi/v/nested-multipart-parser)](https://pypi.org/project/nested-multipart-parser/)

Parser for nested data in multipart form, you can use it anyways, and you have a django rest framework integration

# Installation

```bash
pip install nested-multipart-parser
```

# How to use it

## for every framwork

```python
from nested_multipart_parser import NestedParser

def my_view():
	parser = NestedParser(data)
	if parser.is_valid():
		validate_data = parser.validate_data
		...
	else:
		print(parser.errors)

```

## for django rest framwork

```python
from nested_multipart_parser.drf import DrfNestedParser
...

class YourViewSet(viewsets.ViewSet):
	parser_classes = (DrfNestedParser,)
```

## What is doing

the parser take the request data and transform to dictionary

exemple:

```python
# input
{
	'title': 'title',
	'date': "time",
	'simple_object[my_key]': 'title'
	'simple_object[my_list][0]': True,
	'langs[0][id]': 666,
	'langs[0][title]': 'title',
	'langs[0][description]': 'description',
	'langs[0][language]': "language",
	'langs[1][id]': 4566,
	'langs[1][title]': 'title1',
	'langs[1][description]': 'description1',
	'langs[1][language]': "language1"
}

# results are:
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

## How is work

for this working perfectly you need to follow this rules:

- a first key need to be set ex: 'title[0]' or 'title', in both the first key is 'title'
- each sub key need to enclose by brackets "[--your-key--]"
- if sub key are a full number, is converted to list
- if sub key is Not a number is converted to dictionary
- the key can't be rewite
  ex:

```python
	data = {
		'title[0]': 'my-value'
	}
	# output
	output = {
		'title': [
			'my-value'
		]
	}

	# invalid key
	data = {
		'title[688]': 'my-value'
	}
	# ERROR , you set a number is upper thans actual list


	# wrong format
	data = {
		'title[0]]]': 'my-value',
		'title[0': 'my-value',
		'title[': 'my-value',
		'title[]': 'my-value',
		'[]': 'my-value',
	}

	data = {
		'title': 42,
		'title[object]': 42
	}
	# Error , title as alerady set by primitive value (int, boolean or string)

	# many element in list
	data = {
		'title[0]': 'my-value',
		'title[1]': 'my-second-value'
	}
	# output
	output = {
		'title': [
			'my-value',
			'my-second-value'
		]
	}

	# converted to object
	data = {
		'title[key0]': 'my-value',
		'title[key7]': 'my-second-value'
	}
	# output
	output = {
		'title': {
			'key0': 'my-value',
			'key7': 'my-second-value'
		}
	}

	# you have no limit for chained key
	data = {
		'the[0][chained][key][0][are][awesome][0][0]': 'im here !!'
	}
	# output
	output: {
		'the': [
			{
				'chained':{
					'key': [
						{
							'are': {
								'awesome':
								[
									[
										'im here !!'
									]
								]
							}
						}
					]
				}
			}
		]
	}
```


## Javscript
You can use this [multipart-object](https://github.com/remigermain/multipart-object) library to easy convert object to flat nested object formated for this library
