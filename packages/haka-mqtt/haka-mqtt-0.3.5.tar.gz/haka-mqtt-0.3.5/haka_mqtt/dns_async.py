import errno
import fcntl
import os
import socket
import threading
from Queue import Queue, Empty
from time import sleep


class _Future(object):
    def __init__(self, call, *args, **kwargs):
        assert callable(call)
        self.__cancelled = False
        self.__done = False
        self.__result = None
        self.__exception = None
        self.__notified = False
        self.__callbacks = []
        self.__callable = call
        self.__args = args
        self.__kwargs = kwargs

    def _work(self):
        try:
            self.__result = self.__callable(*self.__args, **self.__kwargs)
        except Exception as e:
            self.__exception = e
        self.__done = True

    def _notify(self):
        if not self.__notified:
            self.__notified = True
            for cb in self.__callbacks:
                cb(self)

    def cancel(self):
        if self.done():
            rv = False
        else:
            self.__cancelled = True
            self.__done = True
            self._notify()
            rv = True

        return rv

    def cancelled(self):
        return self.__cancelled

    def done(self):
        return self.__done

    def result(self, timeout=None):
        if timeout != 0:
            raise NotImplementedError('Blocking, waiting for results is not implemented.  timeout must be zero.')

        return self.__result

    def exception(self, timeout=None):
        if timeout != 0:
            raise NotImplementedError('Blocking, waiting for results is not implemented.  timeout must be zero.')

        return self.__exception

    def add_done_callback(self, fn):
        if self.done():
            fn(self)
        else:
            self.__callbacks.append(fn)


_Poison = object()


def _worker_task(work_queue, wd, done_queue):
    """Listens for tasks on work_queue, completes them, then places the
    completed tasks on the done_queue.

    Parameters
    ----------
    work_queue: Queue
    wd: fileno
    done_queue: Queue of _Future
    """

    while True:
        future = work_queue.get()
        if future is _Poison:
            break
        else:
            future._work()
            done_queue.put(future)

            while True:
                num_bytes_written = os.write(wd, b'x')
                if num_bytes_written == 1:
                    break
                elif num_bytes_written == 0:
                    sleep(0.01)
                else:
                    raise NotImplementedError(num_bytes_written)


class AsyncFutureDnsResolver(object):
    """An executor that spawns a small thread pool for performing DNS
    lookups.  DNS lookup task sare submitted by using calling this
    object as a function and those tasks will be completed
    asynchronously by threads in a thread pool.  The completed tasks
    are posted back to an internal queue and the :meth:`poll` method
    gets the completed tasks from the queue and notifies their
    subscribers of completion.  Tasks with done callback methods will
    be called by poll on the same threat that poll is called on.

    >>> resolver = AsyncFutureDnsResolver()
    >>>
    >>> lookup_result = None
    >>>
    >>> def lookup_finished(future):
    ...   global lookup_result
    ...   lookup_result = future.result()
    ...
    >>> future = resolver('localhost', 80)
    >>> future.add_done_callback(lookup_finished)
    >>>
    >>> while not future.done():
    ...   # Calling poll services callbacks and sets future to done.
    ...   resolver.poll()
    ...   sleep(0.1)
    ...
    >>> assert future.done()
    >>>
    >>> # Only timeout=0 presently supported.
    >>> assert not future.exception(timeout=0)
    >>> assert not future.cancelled()
    >>> # future.result(0) contains outcome of asynchronous call
    >>> # to socket.getaddrinfo.  Note that at this time only timeout=0
    >>> # is supported by this limited api.

    .. aafig::

                                 |                      Worker Threads
                                 |                      +------------+
                                 |                  +-->| Worker 0   |-->+
                                 |                  |   +------------+   |
                                 |                  |                    |
                                 |                  |   +------------+   |
                                 |                  +-->| Worker 1   |-->+
                                 |                  |   +------------+   |
                                 |                  |                    |
                                 |                  |   +------------+   |
      resolver('google.com', 80) |--> task queue----+-->| Worker ... |-->+
                                 |                  |   +------------+   |
                                 |                  |                    |
          AsyncFutureDnsResolver |                  |   +------------+   |
                          Thread |                  +-->| Worker n   |-->+
                                 |                      +------------+   |
                                 |                                       |
                                 |                                       |
                resolver.poll()  |<-- completion queue<------------------+
                                 |
    """
    def __init__(self, thread_pool_size=1):
        self.__closed = False
        self.__work_queue = Queue()
        self.__done_queue = Queue()
        self.__threads = []
        self.__rd, self.__wd = os.pipe()

        flags = fcntl.fcntl(self.__rd, fcntl.F_GETFL)
        fcntl.fcntl(self.__rd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        flags = fcntl.fcntl(self.__wd, fcntl.F_GETFL)
        fcntl.fcntl(self.__wd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        for i in range(0, thread_pool_size):
            t = threading.Thread(target=_worker_task, args=(self.__work_queue, self.__wd, self.__done_queue))
            t.daemon = True
            self.__threads.append(t)
            t.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def closed(self):
        """bool: True if the object has been closed; False otherwise."""
        return self.__closed

    def close(self):
        """Closes resolver by completing all tasks in queue and joining
         with worker threads.  New dns resolutions cannot be scheduled
         after this method begins executing (calling the resolver will
         result in an assertion failure)."""
        if not self.closed():
            self.__closed = True
            for i in xrange(0, len(self.__threads)):
                self.__work_queue.put(_Poison)

            for thread in self.__threads:
                thread.join()
                self.poll()

            os.close(self.__wd)
            os.close(self.__rd)

    def __call__(self, host, port, family=0, socktype=0, proto=0, flags=0):
        """Queues an asynchronous DNS resolution task.

        Parameters
        ----------
        host: str or None
            A host `str` must contain either a domain name for lookup
            or a string representation of an IPv4/v6 address.
        port: str or int or None
            A string service name such as 'http', a numeric port number,
            or None.
        family: int
            One of the socket.AF_* constants.
        socktype: int
            One of the socket.SOCK_* constants.
        proto: int
            socket.IPPROTO_TCP
        flags: int
            One of several of the AI_* constants; default is zero.

        Returns
        -------
        Future
            If the DNS lookup succeeds then the `future.result()` will
            immediately return a 5-tuple with a structure like
            (family, socktype, proto, canonname, sockaddr).  On failure
            then `future.exception()` will immediately return a
            `socket.gaierror`.

            In these tuples, family, socktype, proto are all integers
            and are meant to be passed to the socket() function.
            canonname will be a string representing the canonical name
            of the host if AI_CANONNAME is part of the flags argument;
            else canonname will be empty. sockaddr is a tuple
            describing a socket address, whose format depends on the
            returned family (a (address, port) 2-tuple for AF_INET, a
            (address, port, flow info, scope id) 4-tuple for AF_INET6),
            and is meant to be passed to the socket.connect() method.
        """
        assert not self.__closed, 'Async dns lookup after resolver closed.'

        getaddrinfo_params = (host, port, family, socktype, proto, flags)
        future = _Future(socket.getaddrinfo, *getaddrinfo_params)
        self.__work_queue.put(future)

        return future

    def read_fd(self):
        """int: fileno"""
        return self.__rd

    def poll(self):
        """Calls done callbacks of any newly completed futures."""
        try:
            rc = os.read(self.__rd, 1)
        except OSError as e:
            if e.errno is errno.EAGAIN:
                # No data available in pipe.
                pass
            else:
                # Unknown error; crash!
                raise
        else:
            if rc:
                # A byte was read.
                try:
                    future = self.__done_queue.get_nowait()
                except Empty:
                    pass
                else:
                    future._notify()
