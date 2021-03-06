.. _queryset_reference:

QuerySet API reference
=====

Internally, a QuerySet can be constructed, filtered, sliced, and generally passed around without actually hitting the database. No database activity actually occurs until you do something to evaluate the queryset.

You can evaluate a QuerySet in the following ways:

objects
--------------------------------------
The most important attribute of a model is the Manager.
It’s the interface through which database query operations are provided to Lawes models and is used to retrieve the instances from the database.
The name is objects. Managers are only accessible via model classes, not the model instances.

Iteration
--------------------------------------
Iteration. A QuerySet is iterable, and it executes its database query the first time you iterate over it. For example, this will print the headline of all entries in the database:

.. code-block:: python

    >>> from model import Fruit
    >>> for fruit in Fruit.objects.filter():
    >>>     print fruit.name

Slicing
--------------------------------------
Slicing. As explained in Limiting QuerySets, a QuerySet can be sliced, using Python’s array-slicing syntax.
Slicing an unevaluated QuerySet usually returns another unevaluated QuerySet, but Django will execute the database query if you use the “step” parameter of slice syntax, and will return a list.
Slicing a QuerySet that has been evaluated also returns a list.

.. code-block:: python

    >>> from model import Fruit
    >>> for fruit in Fruit.objects.filter()[:1]:
    >>>     print fruit.name

.. _ensure_index:

Ensure Index
=====
Some database indexs will be created for the fields.

init_index()
--------------------------------------
If db_index is True, a database index will be created for this field.

.. code-block:: python

    >>> from model import Fruit
    >>> Fruit.objects.init_index()

.. _queryset_api:

QuerySet API
=====
Django provides a range of QuerySet refinement methods that modify either the types of results returned by the QuerySet or the way its SQL query is executed.

filter()
--------------------------------------
Returns a new QuerySet containing objects that match the given lookup parameters.Also you can find the _id in mongodb.

The lookup parameters (**kwargs) should be in the format described in Field lookups below. Multiple parameters are joined via AND in the underlying SQL statement.
The paramaters can with extra '__' like: __gt,__gte,__lt,__lte,__ne. They will find with comparsion: 'g' meas 'greater'; 't' means 'than'; e means 'equality'; 'n' means 'not';
query = {"1__gt": 1,"2__gte": 2,"3__lt": 3,"4__lte": 4,"5__ne": 5, '6': 6, '7_text__search': '77d' }
the query will change to {'1': {'$gt': 1}, '2': {'$gte': 2}, '3': {'$lt': 3}, '4': {'$lte': 4}, '5': {'$ne': 5}, '6': 6, '7': {'$regex': '7.*7.*d', '$options': 'si'}}

.. code-block:: python

    >>> from models import Fruit
    >>> fruits = Fruit.objects.filter(name='mongo')
    >>> for fruit in fruits:
    >>>     print fruit.name
    >>> fruits = Fruit.objects.filter(name__gt='mongo')
    >>> fruits = Fruit.objects.filter(_id='58f71dafd97f0e1b886b0d1c')
    >>> fruits = Fruit.objects.filter(name_text__search='ox')

order_by()
--------------------------------------
By default, results returned by a QuerySet are ordered by the _id in mongo. You can override this on a per-QuerySet basis by using the order_by method.
if there is a '-' in front of the parameter, it means order desc, else it means order asc.

.. code-block:: python

    >>> from models import Fruit
    >>> fruits = Fruit.objects.filter().order_by('-name')
    >>> for fruit in fruits:
    >>>     print fruit.name

get()
--------------------------------------
Returns the object matching the given lookup parameters, which should be in the format described in Field lookups.

get() raises MultipleObjectsReturned if more than one object was found.

get() raises a DoesNotExist exception if an object wasn’t found for the given parameters.

.. code-block:: python

    >>> from models import Fruit
    >>> fruits = Fruit.objects.get(name='mongo')
    >>> fruit.name

get_or_create()
--------------------------------------
A convenience method for looking up an object with the given kwargs (may be empty if your model has defaults for all fields), creating one if necessary.

Returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean specifying whether a new object was created.

If you want to use get_or_create(), the field must be set unique.

.. code-block:: python

    >>> from models import Fruit
    >>> obj, created = Fruit.objects.get_or_create(name='mongo')
    >>> obj.name

delete()
--------------------------------------
Performs an SQL delete query on all rows in the QuerySet and returns the number of objects deleted and a dictionary with the number of deletions per object type.

For example, to delete all the entries in a particular blog:

.. code-block:: python

    >>> from models import Fruit
    >>> Fruit.objects.filter(name='mongo').delete()
    >>> for fruit in Fruit.objects.filter(name='mongo'):
    >>>     print fruit.delete()

count()
--------------------------------------
It will returns the number of records as an integer.

.. code-block:: python

    >>> from models import Fruit
    >>> print(Fruit.objects.filter(name='mongo').count())
    >>> 1
    >>> print(bool(Fruit.objects.filter(name='mongo')))
    >>> True

