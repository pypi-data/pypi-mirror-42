tcli
=============

Tools for nice user interfaces in the terminal.

.. image:: https://img.shields.io/travis/TankerHQ/python-cli-tcli.svg?branch=master
  :target: https://travis-ci.org/TankerHQ/tcli

.. image:: https://img.shields.io/pypi/v/python-cli-tcli.svg
  :target: https://pypi.org/project/tcli/

.. image:: https://img.shields.io/github/license/TankerHQ/python-cli-tcli.svg
  :target: https://github.com/TankerHQ/tcli/blob/master/LICENSE


Documentation
-------------


See `tcli documentation <https://TankerHQ.github.io/tcli>`_.

Demo
----


Watch the `asciinema recording <https://asciinema.org/a/112368>`_.


Usage
-----

.. code-block:: console

    $ pip install tcli

Example:

.. code-block:: python

    import ui

    # coloring:
    tcli.info("This is", tcli.red, "red",
            tcli.reset, "and this is", tcli.bold, "bold")

    # enumerating:
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        tcli.info_count(i, len(list_of_things), thing)

    # progress indication:
    tcli.info_progress("Done",  5, 20)
    tcli.info_progress("Done", 10, 20)
    tcli.info_progress("Done", 20, 20)

    # reading user input:
    with_sugar = tcli.ask_yes_no("With sugar?", default=False)

    fruits = ["apple", "orange", "banana"]
    selected_fruit = tcli.ask_choice("Choose a fruit", fruits)

    #  ... and more!
