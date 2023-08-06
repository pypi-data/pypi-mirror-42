Development Notes
==================================================================================

Using a temporary, local Docker container with an ssh private key and some Python 3 packages for initial tests.

Very important: Do not share this Docker image with your private key information.

Change to the directory where the Dockerfile is and build the image from there. Note the use of $(date) to use today's date as part of the image's name.

.. code-block:: bash

  $ docker build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t alexisbellido/znbstatic-$(date +%Y%m%d) .

Then run the container and make sure you don't map over the /root directory because that's where ssh key from the host is stored if you use a temporary container.

.. code-block:: bash

  $ docker run -it --rm --mount type=bind,source=$PWD,target=/root/project alexisbellido/znbstatic-20190107:latest docker-entrypoint.sh /bin/bash

Configuration and Django settings.py
------------------------------------------------------------------------------

Review partial settings files production.py and locals3.py in docs directory.

Distribute as a setuptools-based Package
------------------------------------------------------------------------------

This can be run from a host or a container. My tests have been on a container.

.. code-block:: bash

  $ pip install setuptools wheel twine

Run this from the same directory where setup.py is located.

.. code-block:: bash

  $ python setup.py sdist bdist_wheel

Upload to Test PyPi at `<https://test.pypi.org>`_.

  $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*

The package is now available at `<https://test.pypi.org/project/znbstatic/>`_ and can be installed with pip.

.. code-block:: bash

  $ pip install -i https://test.pypi.org/simple/ znbstatic

Upload to the real PyPi at `<https://pypi.org>`_.

.. code-block:: bash

  $ twine upload dist/*

The package is now available at `<https://pypi.org/project/znbstatic/>`_ and can be installed with pip.

.. code-block:: bash

  $ pip install znbstatic

Additional Resources
------------------------------------------------------------------------------

  * `packaging projects <https://packaging.python.org/tutorials/packaging-projects>`_.
  * `sample project on GitHub <https://github.com/pypa/sampleproject>`_.
  * `setuptools <https://setuptools.readthedocs.io/en/latest/setuptools.html>`_.
  * `pip install <https://pip.pypa.io/en/stable/reference/pip_install>`_ documentation.
  * `include additional files with distribution <https://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files>`_.
