hjs
===

todo ...
![build](https://api.travis-ci.org/charbeljc/hjs.svg?branch=master)\_
![gpa](https://codeclimate.com/github/charbeljc/hjs/badges/gpa.svg)\_
![cover](https://codeclimate.com/github/charbeljc/hjs/badges/coverage.svg)\_

`hjs` is a thin wrapper around [hjson](http://github.com/hjson/hjson-py)

![image](https://duckduckgo.com/i/bf0eb228.png)

``` {.sourceCode .python}
>>> from hjs import  hjs, load, loads, dump, load

>>> da = loads("""
... {
...    a: 1
...    b: are you ok with it ? // Hey, wtf are you talking about
...    c: '''
...       what a rest,
...       isn't it ?
...       '''
...    t: {
...        a: you get the point, now :-)
...    },
...    values: 42
... }
... """)

>>> assert da['values'] == 42
>>> assert da.t.a == "you get the point, now :-)"
```

install as usual with `pip install hjs`

By the way, you should support [pypi](https://pypi.python.org/pypi),
because, given the strategic importance of this project, it is *way*
under budgeted, as I heard...

Time for bugfixes

ok, ok ...
tagging 
still online.
release ...

Time to branch
Explain

Regards, @CJC\_2017.
Hum, time to be serious about doc, maybe ?
Hum, no, software needing documentation is broken software :-D

