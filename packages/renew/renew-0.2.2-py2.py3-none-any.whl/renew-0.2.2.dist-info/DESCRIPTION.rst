renew
=====

Semi-text-pickling in pure python. If you meet just a few restrictions,
you can store classes state into a python file and import or evaluate it
somewhere else or later on.

repr(object)
------------

Does ``repr`` stand for "representation" or "reproduction"? According to
python documentation ``__repr__`` functionality has two separate
approaches. From https://docs.python.org/3/library/functions.html#repr
(v 3.7.2)

    ``repr(object)`` Return a string containing a printable
    representation of an object. For many types, this function makes an
    attempt to return a string that would yield an object with the same
    value when passed to eval(), otherwise the representation is a
    string enclosed in angle brackets that contains the name of the type
    of the object together with additional information often including
    the name and address of the object. A class can control what this
    function returns for its instances by defining a ``__repr__()``
    method.

1. reproducible repr:
---------------------

For several native objects it returns a string that can be used to
reproduce given object, i.e. to create a copy of given object.

sa

.. code:: python

    a = [1, 3.141559, None, "string"]
    statement_str = repr(a)
    assert statement_str == '[1, 3.141559, None, "string"]'

You may tell that repr of an object is ``reproducible`` if this is meet:

.. code:: python

    a = [1, 3.14159, None, "string"]
    statement_str = repr(a)
    assert repr(eval(statement_str)) == statement_str
    # if the object implements __eq__ this should be also true:
    assert eval(statement_str) == a

2. descriptive repr:
--------------------

Unfortunately python does not serve the "reproducible repr" out of the
box for types defined by user:

.. code:: python

    class Car(object):
        def __init__(self, body_type, engine_power):
            self.body_type = body_type
            self.engine_power = engine_power

    car = Car("coupe", 124.0)
    # repr(car) == '<__main__.Car object at 0x7f0ff6313290>'
    # but using renew:

    import renew

    @renew.reproducible(namespace="")
    class ReproducibleCar(object):
        def __init__(self, body_type, engine_power):
            self.body_type = body_type
            self.engine_power = engine_power

    car2 = ReproducibleCar("sedan", 110.0)
    assert repr(car2) == 'ReproducibleCar("sedan", 110.0)'
    assert repr(eval(repr(car2))) == 'ReproducibleCar("sedan", 110.0)'

How it works?
-------------

Note that ReproducibleCar does not explicitly implement the
``__repr__``, but the ``renew.reproducible`` decorator supplements
(overrides) it. ``renew.reproduction`` inspects constructor's argument
specification of decorated class and yields a string that tries to be a
call statement composed of \* ``namespace``, e.g. your package name
(according to desired importing convention) \* given class name \* given
class' attributes values, that have the same names and order as
constructor arguments

That forms the only one usage restriction:

**The class has to store all the constructor arguments in its attributes
with the same name** (as in ``ReproducibleCar`` definition above).

Limitations
-----------

Besides the statement above: \* plain ``keyword-arguments`` are not
(yet) supported (``default-arguments`` work well, however) \* keys of
``dict`` being complex objects are getting a bit ugly layout.

For full list of features and usage examples, please refer to unit
tests.


