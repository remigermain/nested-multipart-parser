# Nested-multipart-parser

<a href="https://u8views.com/github/remigermain"><img src="https://u8views.com/api/v1/github/profiles/66946113/views/day-week-month-total-count.svg" width="1px" height="1px"></a>
[![CI](https://github.com/remigermain/nested-multipart-parser/actions/workflows/main.yml/badge.svg)](https://github.com/remigermain/nested-multipart-parser/actions/workflows/main.yml)
[![pypi](https://img.shields.io/pypi/v/nested-multipart-parser)](https://pypi.org/project/nested-multipart-parser/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/Nested-multipart-parser)](https://pypistats.org/packages/nested-multipart-parser)

Parser for nested data for *multipart/form*, usable in any Python project or via the [Django Rest Framework integration](https://www.django-rest-framework.org/community/third-party-packages/#parsers)..
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

you can define parser for all view in settings.py
```python
REST_FRAMEWORK = {
	"DEFAULT_PARSER_CLASSES": [
		"nested_multipart_parser.drf.DrfNestedParser",
	]
}
```
or directly in your view

```python
from nested_multipart_parser.drf import DrfNestedParser
...

class YourViewSet(viewsets.ViewSet):
	parser_classes = (DrfNestedParser,)
```


## What it does:

The parser takes the request data and transforms it into a Python dictionary.

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

## How it works
### Lists

Attributes whose sub‑keys are *only numbers* become Python lists:
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
```
> Important notes

- Indices must be contiguous and start at 0.
- You cannot turn a primitive (int, bool, str) into a list later, e.g.
```python
    'title': 42,
    'title[object]': 42   # ❌ invalid
```

### Dictionaries

Attributes whose sub‑keys are *not pure numbers* become nested dictionaries:
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
```

### Chaining keys

>Keys can be chained arbitrarily. Below are examples for each separator option:

|Separator|	Example key |	Meaning|
|-|-|-|
|mixed‑dot|	the[0].chained.key[0].are.awesome[0][0]	|List → object → list → object …|
|mixed|	the[0]chained.key[0]are.awesome[0][0] |	Same as mixed‑dot but without the dot after a list|
|bracket|	the[0][chained][key][0][are][awesome][0][0]	| Every sub‑key is wrapped in brackets|
|dot	|the.0.chained.key.0.are.awesome.0.0 |	Dots separate every level; numeric parts become lists|


Rules to keep in mind
- First key must exist – e.g. title[0] or just title.
- For mixed / mixed‑dot, [] denotes a list and . denotes an object.
- mixed‑dot behaves like mixed but inserts a dot when an object follows a list.
- For bracket, each sub‑key must be surrounded by brackets ([ ]).
- For bracket or dot, numeric sub‑keys become list elements; non‑numeric become objects.
- No spaces between separators.
- By default, duplicate keys are disallowed (see options).
- Empty structures are supported:
        Empty list → "article.authors[]": None → {"article": {"authors": []}}
        Empty dict → "article.": None → {"article": {}} (available with dot, mixed, mixed‑dot)


  

## Options

```python
{
    # Separator (default: 'mixed‑dot')
    #   mixed‑dot : article[0].title.authors[0] -> "john doe"
    #   mixed    : article[0]title.authors[0]   -> "john doe"
    #   bracket  : article[0][title][authors][0] -> "john doe"
    #   dot      : article.0.title.authors.0   -> "john doe"
    'separator': 'bracket' | 'dot' | 'mixed' | 'mixed‑dot',

    # Raise an exception when duplicate keys are encountered
    #   Example:
    #   {
    #       "article": 42,
    #       "article[title]": 42,
    #   }
    'raise_duplicate': True,   # default: True

    # Override duplicate keys (requires raise_duplicate=False)
    #   Example:
    #   {
    #       "article": 42,
    #       "article[title]": 42,
    #   }
    #   Result:
    #   {
    #       "article": {
    #           "title": 42
    #       }
    #   }
    'assign_duplicate': False, # default: False
}
```

## Options for Django Rest Framwork:
```python
# settings.py
DRF_NESTED_MULTIPART_PARSER = {
    "separator": "mixed‑dot",
    "raise_duplicate": True,
    "assign_duplicate": False,

    # If True, the parser’s output is converted to a QueryDict;
    # if False, a plain Python dict is returned.
    "querydict": True,
}
```

## JavaScript integration:
A companion [multipart-object](https://github.com/remigermain/multipart-object) library exists to convert a JavaScript object into the flat, nested format expected by this parser.

## License

[MIT](https://github.com/remigermain/multipart-object/blob/main/LICENSE)
