###########
brom-Spades
###########

brom-Spades is a scoring agent for `Spades <https://en.wikipedia.org/wiki/Spades>`_.

The core package includes a commandline interface, but other interfaces will come later in separate packages (though still relying on the core.)


**********
Developers
**********

The ``main`` function is what handles control flow. It is what calls all of the basic functions from both the backend and the frontend.

Each of these is a class that is expected to define particular methods. The ``RequiredMethods`` metaclass ensures that all necessary methods are defined (based on the ``_METHODS`` class variable). To write a backend or frontend from scratch, you should still inherit from the ``FrontEnd`` or ``BackEnd`` classes as these define the correct ``_METHODS`` and use the ``RequiredMethods`` metaclass.

A ``SimpleBackEnd`` class is included that should be suitable for most needs, though it can be inherited from if expansion is necessary.

The ``TerminalFrontEnd`` class has also been included, which can be referred to as an example of a properly-written frontend class.

Once backend and frontend classes have been defined, they can be used as::

    backend = BackEnd()
    frontend = FrontEnd()
    main(backend, frontend)

although a frontend class will very likely want the backend instance as an argument (as is the case with the default ``TerminalFrontEnd``).


Required Methods for Frontend
=============================

The only method that accepts an argument is ``win``, which takes the index of the winning team (0 or 1).

What is returned must use the following format only if a standard backend is used. ``main`` uses it merely to pass it on to the backend.

``_input`` is an extra method in the default frontend that wraps ``input`` to give additional commands like ``exit`` or ``undo``. These are implemented by raising the ``Undo`` or ``Exit`` exceptions, which ``main`` then handles by calling ``backend.undo()`` or ``frontend.exit()``.

+-----------------+------------------------------------------------------------+
|   Name          | Returns                                                    |
+=================+============================================================+
| ``ask_bids``    | list: four numerical bids starting with the original       |
|                 | dealer                                                     |
+-----------------+------------------------------------------------------------+
| ``ask_names``   | list: four strings starting with the original dealer       |
+-----------------+------------------------------------------------------------+
| ``ask_tricks``  | list: four numerical tricks taken starting with the        |
|                 | original dealer                                            |
+-----------------+------------------------------------------------------------+
| ``exit``        | *nothing*. Exits application (yes, it calls ``exit()``)    |
+-----------------+------------------------------------------------------------+
| ``welcome``     | *nothing*. **Optional** Starts off the game with a warm    |
|                 | welcome.                                                   |
+-----------------+------------------------------------------------------------+
| ``win(winner)`` | *nothing*. Just a celebration                              |
+-----------------+------------------------------------------------------------+


Required Methods for Backend
============================


Only the number of arguments is really unchangeable. What type and format is expected must merely be consistent with the frontend. A typical function call in ``main`` is::

    backend.set_names(frontend.ask_names())

Therefore, the description of each argument below describes only the default format; it is not a requirement. Also of note is that there are no methods that accept more than one argument.

The scoring is never directly called by the ``main`` function. That is to be implemented as you wish (the default calls a ``_score`` method at the end of ``add_tricks``.)


+----------------+-------------------------------+-----------------------------+
| Name           | Argument                      | Returns                     |
+================+===============================+=============================+
| ``add_bids``   | list containing four          |                             |
|                | numerical bids starting with  |                             |
|                | the original dealer           |                             |
+----------------+-------------------------------+-----------------------------+
| ``add_tricks`` | list containing four          |                             |
|                | numerical tricks taken        |                             |
|                | starting with the original    |                             |
|                | dealer. Also calls the        |                             |
|                | scoring function.             |                             |
+----------------+-------------------------------+-----------------------------+
| ``get_bids``   |                               | list: four numerical bids   |
|                |                               | starting with the original  |
|                |                               | dealer                      |
+----------------+-------------------------------+-----------------------------+
| ``get_dealer`` |                               | int: table position of      |
|                |                               | current dealer              |
+----------------+-------------------------------+-----------------------------+
| ``get_names``  |                               | list: four names as strings |
|                |                               | starting with the original  |
|                |                               | dealer                      |
+----------------+-------------------------------+-----------------------------+
| ``get_scores`` |                               | list: two numerical scores  |
|                |                               | starting with the           |
|                |                               | partnership that includes   |
|                |                               | the original dealer         |
+----------------+-------------------------------+-----------------------------+
| ``get_tricks`` |                               | list: four numerical tricks |
|                |                               | taken starting with the     |
|                |                               | original dealer             |
+----------------+-------------------------------+-----------------------------+
| ``set_names``  | list of four strings starting |                             |
|                | with the original dealer      |                             |
+----------------+-------------------------------+-----------------------------+
| ``undo``       |                               | *nothing*. Decrements       |
|                |                               | ``self.deal`` if possible   |
|                |                               | or raises ``CannotUndo``    |
+----------------+-------------------------------+-----------------------------+
