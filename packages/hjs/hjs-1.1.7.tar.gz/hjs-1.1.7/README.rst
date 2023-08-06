===
hjs 
===
|build|_ |gpa|_ |cover|_

``hjs`` is a thin wrapper around `hjson <http://github.com/hjson/hjson-py>`_

.. |build| image:: https://api.travis-ci.org/charbeljc/hjs.svg?branch=master
.. _build: https://travis-ci.org/charbeljc/hjs
.. |gpa| image:: https://codeclimate.com/github/charbeljc/hjs/badges/gpa.svg
.. _gpa: https://codeclimate.com/github/charbeljc/hjs
.. |cover| image:: https://codeclimate.com/github/charbeljc/hjs/badges/coverage.svg
.. _cover:  https://codeclimate.com/github/charbeljc/hjs/coverage

.. image:: https://duckduckgo.com/i/bf0eb228.png
.. code-block:: python

   >>> from hjs import  hjs, load, loads, dump, load

   >>> da = loads("""
   ... {
   ...    a: 1
   ...    b: are you ok with it ?
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

install as usual with ``pip install hjs``

By the way, you should support `pypi <https://pypi.python.org/pypi>`_, because, given the strategic importance of this project, it is *way* under budgeted, as I heard...

Regards,
@CJC_2017.


