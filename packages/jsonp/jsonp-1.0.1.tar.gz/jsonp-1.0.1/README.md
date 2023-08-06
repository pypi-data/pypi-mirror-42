# Simple pipeline json parser

It is as jq but better because you can use python syntax and you do not need to look in documentation every time.

## Install

```
pip install jsonp
```

## Usage

Pretty print
```
echo '{"userId":1,"id":1,"title":"delectus aut autem","completed":false}' | j
{
    "completed": false,
    "id": 1,
    "title": "delectus aut autem",
    "userId": 1
}
```

Modify data as you want until returned data is correct json object
```
echo '{"userId":1,"id":1,"title":"delectus aut autem","completed":false}' | j '{str(v):k for k, v in it.items()}'
{
    "1": "id",
    "False": "completed",
    "delectus aut autem": "title"
}

```
