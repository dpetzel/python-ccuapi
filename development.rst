Development Documentation
=========================

Environment Setup
-----------------
Its recommended you created a dedicated virtualenv.

Once you have created and activated the new virtualenv you will want to
install the required development packages:

.. code-block:: bash

    pip install -r requirements_dev.txt

Testing
-------
In order to speed up testing the `httmock <https://pypi.python.org/pypi/httmock/>`_
library is used to mock API calls so you don't need to have actual connectivity
to Akamai.

.. code-block:: bash

    nosetests -v

This will run through the unittests

Styling
-------
This project tries to adhere to PEP8 styling guidelines and leverages pylint
for lint style checking. These checks can be run by simply invoking the
`pylint ccuapi` from the root of the repo

CLI Running
-----------
In addition to being a module, there is also a runnable script that gets
installed during installation. The syntax to run this in development is a little
different:

.. code-block:: bash

    python -m ccuapi.ccu_purge