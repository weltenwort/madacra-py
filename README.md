Madacra
=======

Setting up a development environment
------------------------------------

1. Clone this repository
1. Install a mongodb server.
1. Install nodejs.
1. Install the `lesscss` and `coffee-script` compilers using npm:

    ```
    $ [sudo] npm install -g less coffee-script
    ```

1. Create and activate a Python virtualenv for the project and install the dependcies in it using

    ```
    $ pip install -r <path-to-repository>/src/server/requirements.txt
    ```

1. Inside &lt;path-to-repository&gt;/src/server/ start the watcher process that compiles assets when they are modified:

    ```
    $ python manage.py assets watch
    ```

1. Inside &lt;path-to-repository&gt;/src/server/ start the server process with your desired configuration file (the path of which is relative to the instance folder):

    ```
    $ MADACRA_SERVER_SETTINGS=<settings-file> python manage.py runserver
    ```

Testing mode
------------

When the server is configured for testing by setting the configuration key `TESTING = True`, it differs from non-testing mode in the following way:

* The function `madacraserver.testing.create_fixtures` is called on app initialisation to populate the database with some dummy data.
* Two additional routes are recognised:
  - `/tests/e2e` serves an AngularJS end-to-end test runner with all tests in `static/tests/e2e/*.coffee`
  - `/tests/unit` serves a jasmine unit test runner with all tests in `static/tests/unit/*.coffee`
* A `messaging.MessageDebugLogger` is created, that logs all messages sent on the internal event bus