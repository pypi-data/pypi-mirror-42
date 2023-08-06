# bombfuse
Python module for specifying timeouts when executing functions

## Installation
To install this package, run the following command:

    $ pip install bombfuse

## Usage

    >>> import time
    >>> import bombfuse
	>>> # here's an infinite loop
    >>> def func(msg):
    >>>     while True:
    >>>         time.sleep(1)
    >>>         print msg
    >>>
	>>> # time out in 5 seconds
    >>> bombfuse.timeout(5, func, "Hello world!")
    Hello world!
    Hello world!
    Hello world!
    Hello world!
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	  File "bombfuse\__init__.py", line 64, in timeout
	    raise e
	bombfuse.TimeoutError: The function 'func' timed out
    >>>