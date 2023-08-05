Pygments ARM
============

This is a lexer for ARM Assembly language.


Install
+++++++

Using PyPI and pip
------------------

::

    $ (sudo) pip install pygments-arm


Manual
------

::

    $ git clone https://github.com/heia-fr/pygments-arm.git
    $ cd pygments-arm
    $ (sudo) python setup.py install


Using
+++++

Just use the **ARM** "language".


Using in LaTeX documents
++++++++++++++++++++++++

See the minted package at http://minted.googlecode.com.


Extra information
+++++++++++++++++

Pygments supported languages
----------------------------

Pygments at the moment supports over 150 different programming languages,
template languages and other markup languages. To see an exhaustive list of the
currently supported languages, use the command::

    $ pygmentize -L lexers

Pygments styles avaible
-----------------------

To get a list of all available stylesheets, execute the following command on the
command line::

    $ pygmentize -L styles

Please read the `official documentation`_ for further information on the usage
of pygment styles.

.. _official documentation: http://pygments.org/docs/