from typing import Callable

import trio.hazmat
from async_generator import async_generator, yield_, asynccontextmanager, aclosing

from .._networking import BaseSocket
from .._utils import dummy_awaitable
from .. import abc, claim_worker_thread, T_Retval, _local, TaskInfo
from ..exceptions import ExceptionGroup, ClosedResourceError


#
# Event loop
#

run = trio.run


#
# Miscellaneous
#

finalize = aclosing
sleep = trio.sleep


#
# Timeouts and cancellation
#

class CancelScopeWrapper:
    __slots__ = '__original'

    def __init__(self, original: trio.CancelScope):
        assert type(original) is trio.CancelScope
        self.__original = original

    def __getattr__(self, item):
        return getattr(self.__original, item)

    def __setattr__(self, key, value):
        if key != '_CancelScopeWrapper__original':
            setattr(self.__original, key, value)
        else:
            super().__setattr__(key, value)

    async def __aenter__(self):
        self.__original.__enter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self.__original.__exit__(exc_type, exc_val, exc_tb)

    def cancel(self):
        self.__original.cancel()
        return dummy_awaitable


def open_cancel_scope(shield):
    return CancelScopeWrapper(trio.CancelScope(shield=shield))


@asynccontextmanager
@async_generator
async def move_on_after(seconds, shield):
    with trio.move_on_after(seconds) as cancel_scope:
        cancel_scope.shield = shield
        await yield_(CancelScopeWrapper(cancel_scope))


@asynccontextmanager
@async_generator
async def fail_after(seconds, shield):
    try:
        with trio.fail_after(seconds) as cancel_scope:
            cancel_scope.shield = shield
            await yield_(CancelScopeWrapper(cancel_scope))
    except trio.TooSlowError as exc:
        raise TimeoutError().with_traceback(exc.__traceback__) from None


async def current_effective_deadline():
    return trio.current_effective_deadline()


#
# Task groups
#

class TaskGroup:
    __slots__ = '_active', '_nursery', 'cancel_scope'

    def __init__(self, nursery) -> None:
        self._active = True
        self._nursery = nursery
        self.cancel_scope = CancelScopeWrapper(nursery.cancel_scope)

    async def spawn(self, func: Callable, *args, name=None) -> None:
        if not self._active:
            raise RuntimeError('This task group is not active; no new tasks can be spawned.')

        self._nursery.start_soon(func, *args, name=name)


abc.TaskGroup.register(TaskGroup)


@asynccontextmanager
@async_generator
async def create_task_group():
    tg = None
    try:
        async with trio.open_nursery() as nursery:
            tg = TaskGroup(nursery)
            await yield_(tg)
    except trio.MultiError as exc:
        raise ExceptionGroup(exc.exceptions) from None
    finally:
        if tg is not None:
            tg._active = False


#
# Threads
#

async def run_in_thread(func: Callable[..., T_Retval], *args) -> T_Retval:
    def wrapper():
        with claim_worker_thread('trio'):
            _local.portal = portal
            return func(*args)

    portal = trio.BlockingTrioPortal()
    return await trio.run_sync_in_worker_thread(wrapper)


def run_async_from_thread(func: Callable[..., T_Retval], *args) -> T_Retval:
    return _local.portal.run(func, *args)


#
# Async file I/O
#

aopen = trio.open_file


#
# Sockets and networking
#

class Socket(BaseSocket):
    __slots__ = ()

    def _wait_readable(self):
        return wait_socket_readable(self._raw_socket)

    def _wait_writable(self):
        return wait_socket_writable(self._raw_socket)

    async def _notify_close(self):
        trio.hazmat.notify_socket_close(self._raw_socket)

    def _check_cancelled(self):
        return trio.hazmat.checkpoint_if_cancelled()

    def _run_in_thread(self, func: Callable, *args):
        return run_in_thread(func, *args)


async def wait_socket_readable(sock):
    try:
        await trio.hazmat.wait_socket_readable(sock)
    except trio.ClosedResourceError as exc:
        raise ClosedResourceError().with_traceback(exc.__traceback__) from None


async def wait_socket_writable(sock):
    try:
        await trio.hazmat.wait_socket_writable(sock)
    except trio.ClosedResourceError as exc:
        raise ClosedResourceError().with_traceback(exc.__traceback__) from None


#
# Synchronization
#

Lock = trio.Lock


class Event(trio.Event):
    async def set(self) -> None:
        super().set()


class Condition(trio.Condition):
    async def notify(self, n: int = 1) -> None:
        super().notify(n)

    async def notify_all(self) -> None:
        super().notify_all()


Semaphore = trio.Semaphore


class Queue:
    def __init__(self, max_items: int) -> None:
        self._send_channel, self._receive_channel = trio.open_memory_channel(max_items)

    def empty(self):
        return self._receive_channel.statistics().current_buffer_used == 0

    def full(self):
        statistics = self._receive_channel.statistics()
        return statistics.current_buffer_used >= statistics.max_buffer_size

    def qsize(self) -> int:
        return self._receive_channel.statistics().current_buffer_used

    async def put(self, item) -> None:
        await self._send_channel.send(item)

    async def get(self):
        return await self._receive_channel.receive()


abc.Lock.register(Lock)
abc.Condition.register(Condition)
abc.Event.register(Event)
abc.Semaphore.register(Semaphore)
abc.Queue.register(Queue)


#
# Signal handling
#

@asynccontextmanager
@async_generator
async def receive_signals(*signals: int):
    with trio.open_signal_receiver(*signals) as cm:
        await yield_(cm)


#
# Testing and debugging
#

def get_running_tasks():
    import gc

    task_infos = []
    for task in gc.get_referrers(trio.hazmat.Task):
        if isinstance(task, trio.hazmat.Task) and task.coro.cr_frame is not None:
            task_infos.append(TaskInfo(id(task), task.name, task.coro))

    return task_infos


def wait_all_tasks_blocked():
    import trio.testing
    return trio.testing.wait_all_tasks_blocked()
