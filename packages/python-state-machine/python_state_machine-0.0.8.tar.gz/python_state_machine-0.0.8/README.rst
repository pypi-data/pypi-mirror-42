python\_state\_machine
==============

Basic python state machine with no added extensions 

|Build Status|

I forked this project out from Jonathan Tushman's ``state_machine``, because I wanted 
to be able to pass arguments when calling events.
I also removed ORM support (sorry about that).

Install
-------

.. code:: bash

    pip install python_state_machine

.. |Build Status| image:: https://travis-ci.org/jtushman/state_machine.svg?branch=master
   :target: https://travis-ci.org/jtushman/state_machine

Basic Usage
-----------

.. code:: python


    @acts_as_state_machine
    class Person():
        name = 'Billy'

        sleeping = State(initial=True)
        running = State()
        cleaning = State()

        run = Event(from_states=sleeping, to_state=running)
        cleanup = Event(from_states=running, to_state=cleaning)
        sleep = Event(from_states=(running, cleaning), to_state=sleeping)

        @before('sleep')
        def do_one_thing(self):
            print "{} is sleepy".format(self.name)

        @before('sleep')
        def do_another_thing(self):
            print "{} is REALLY sleepy".format(self.name)

        @after('sleep')
        def snore(self):
            print "Zzzzzzzzzzzz"

        @after('sleep')
        def big_snore(self):
            print "Zzzzzzzzzzzzzzzzzzzzzz"

    person = Person()
    print person.current_state == Person.sleeping       # True
    print person.is_sleeping                            # True
    print person.is_running                             # False
    person.run()
    print person.is_running                             # True
    person.sleep()

    # Billy is sleepy
    # Billy is REALLY sleepy
    # Zzzzzzzzzzzz
    # Zzzzzzzzzzzzzzzzzzzzzz

    print person.is_sleeping                            # True

Features
--------

Before / After Callback Decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can add callback hooks that get executed before or after an event
(see example above).

*Important:* if the *before* event causes an exception or returns
``False``, the state will not change (transition is blocked) and the
*after* event will not be executed.

Blocks invalid state transitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An *InvalidStateTransition Exception* will be thrown if you try to move
into an invalid state.

ORM support
-----------

None. If you need it, please use Jonathan Tushman's `state\_machine`

..Issues / Roadmap:
..------------------

..-  Nothing for now

Questions / Issues
------------------

or add issues or PRs at https://github.com/girante/python_state_machine

Thank you
---------

to Jonathan Tushman for developing `state\_machine` and making it available to all

