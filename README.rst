=========================
django-codenerix-examples
=========================

Here you can find examples using `CODENERIX <https://github.com/codenerix/django-codenerix>`_.

.. image:: https://github.com/codenerix/django-codenerix/raw/master/codenerix/static/codenerix/img/codenerix.png
    :target: https://www.codenerix.com
    :alt: Try our demo with Codenerix Cloud


****
Demo
****

You can have a look to our `demo online <http://demo.codenerix.com>`_.

You can get in touch with us `here <https://codenerix.com/contact/>`_.


**********
Quickstart
**********

1. Install your Linux

2. Make sure you have installed the required packages to work with GIT and Python (zlib1g-dev, libjpeg-dev, python-dev, python3-dev are required by Pillow library)::

    apt-get install git python-pip python3-pip zlib1g-dev libjpeg-dev python-dev python3-dev

3. Clone the `CODENERIX Examples <https://github.com/codenerix/django-codenerix-examples>`_ project::

    git clone https://github.com/codenerix/django-codenerix-examples

4. Create a virtualenv and activate it::

    virtualenv -p python3 env
    source env/bin/activate

4. Go to the desired folder (we will go to **agenda**)::

    cd django-codenerix-examples/agenda/

5. Install all requirements for the choosen example::

    For python 3: sudo pip3 install -r requirements.txt

6. That's all...check it out::

    In python 3: python3 manage.py runserver

7. The default user and password are::

    user: demo
    password: demo
