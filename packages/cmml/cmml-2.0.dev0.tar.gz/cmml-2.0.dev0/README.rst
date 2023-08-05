cmml
=====

cmml is a lightweight machine learning application framework.


Installing
----------

Install and update using `pip`_:

.. code-block:: text

    pip install -U cmml


A Simple Example
----------------

.. code-block:: python
    from  cmml.regression import ridgeTest
    from  cmml.regression import predict

    trainX,trainY = loadDataSet("C:\\abalone.txt")
    wMat=ridgeTest(trainX,trainY)
    y=predict(trainX,trainY,[1,1,2,5,4,6,7,1])
    print (y)


Contributing
------------

For guidance on setting up a development environment and how to make a
contribution to cmml, see the `contributing guidelines`_.

.. _contributing guidelines: https://github.com/pallets/flask/blob/master/CONTRIBUTING.rst


Donate
------

The Pallets organization develops and supports Flask and the libraries
it uses. In order to grow the community of contributors and users, and
allow the maintainers to devote more time to the projects, `please
donate today`_.

.. _please donate today: https://psfmember.org/civicrm/contribute/transact?reset=1&id=20


Links
-----

* Website: https://www.palletsprojects.com/p/flask/
* Documentation: http://flask.pocoo.org/docs/
* License: `BSD <https://github.com/pallets/flask/blob/master/LICENSE>`_
* Releases: https://pypi.org/project/Flask/
* Code: https://github.com/pallets/flask
* Issue tracker: https://github.com/pallets/flask/issues
* Test status:

  * Linux, Mac: https://travis-ci.org/pallets/flask
  * Windows: https://ci.appveyor.com/project/pallets/flask

* Test coverage: https://codecov.io/gh/pallets/flask

.. _WSGI: https://wsgi.readthedocs.io
.. _Werkzeug: https://www.palletsprojects.com/p/werkzeug/
.. _Jinja: https://www.palletsprojects.com/p/jinja/
.. _pip: https://pip.pypa.io/en/stable/quickstart/
