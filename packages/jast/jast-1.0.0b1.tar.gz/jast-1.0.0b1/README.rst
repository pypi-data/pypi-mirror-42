========
 jast
========

Construct javascript AST structures using python objects.

Requirements
============

* Python 2.7

Setup
=====

::

  $ python -m pip install --user jast
  or
  (venv)$ python -m pip install jast

Usage
=====

::

  $ python
  >>> import jast
  >>> jast.Object({"a": 1, "b": 2}).ast()
  '{
    "type": "ObjectExpression",
    "properties": [
        {
            "type": "ObjectProperty",
            "method": false,
            "key": {
                "type": "Identifier",
                "name": "a",
                "definition": null
            },
            "computed": false,
            "shorthand": false,
            "value": {
                "type": "NumericLiteral",
                "value": 1,
                "extra": {
                    "rawValue": 1,
                    "raw": "1"
                }
            }
        },
        {
            "type": "ObjectProperty",
            "method": false,
            "key": {
                "type": "Identifier",
                "name": "b",
                "definition": null
            },
            "computed": false,
            "shorthand": false,
            "value": {
                "type": "StringLiteral",
                "value": "2",
                "extra": {
                    "rawValue": "2",
                    "raw": "\"2\""
                }
            }
        }
    ]
   }'

