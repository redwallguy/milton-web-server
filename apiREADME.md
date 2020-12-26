# API user interface
----
Due to current technical constraints, raw json must be posted to the API pages for creation or modification of some object types. This document will show the form those json bodies should take.

## Alias POST
- Form:
    {
        "clip": {
            "name": "NameOfClip",
            "board": "NameOfBoard"
        },
        "name": "AliasName"
    }
- Example:
    {
        "clip": {
            "name": "zawarudo",
            "board": "jojo"
        },
        "name": "za"
    }

## Clip PATCH
- Form:
    {
        "name": "NameOfClip",
        "volume": number in range [1,100]
        "board": "NameOfBoard"
    }
- Example:
    {
        "name": "zawarudo",
        "volume": 75,
        "board": "jojo"
    }
