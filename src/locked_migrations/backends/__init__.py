"""Locking mechanisms are implemented here."""

import importlib
from abc import ABC, abstractmethod
from types import TracebackType


class AbstractBaseLock(ABC):
    """Abstract base class defines the API for concrete lock backend implementations.

    This API is modeled after the built-in `threading.Lock` class.
    """

    @abstractmethod
    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
        """Acquire a lock, blocking or non-blocking.

        When invoked with the blocking argument set to `True` (the default), block until the lock is unlocked, then set it
        to locked and return `True`.

        When invoked with the blocking argument set to `False`, do not block. If a call with blocking set to `True` would
        block, return `False` immediately; otherwise, set the lock to locked and return `True`.

        When invoked with the floating-point timeout argument set to a positive value, block for at most the number of
        seconds specified by timeout and as long as the lock cannot be acquired. A timeout argument of -1 specifies an
        unbounded wait. It is forbidden to specify a timeout when blocking is `False`.

        The return value is `True` if the lock is acquired successfully, `False` if not (for example if the timeout
        expired).

        Reference: https://docs.python.org/3/library/threading.html#threading.Lock
        """

    @abstractmethod
    def release(self) -> None:
        """Release a lock. This can be called from any thread, not only the thread which has acquired the lock.

        When the lock is locked, reset it to unlocked, and return. If any other threads are blocked waiting for the lock
        to become unlocked, allow exactly one of them to proceed.

        When invoked on an unlocked lock, a RuntimeError is raised.

        There is no return value.

        Reference: https://docs.python.org/3/library/threading.html#threading.Lock
        """

    @abstractmethod
    def locked(self) -> bool:
        """Return `True` if the lock is acquired."""

    @abstractmethod
    def __enter__(self) -> bool:
        """Acquire the lock when entering a `with` statement context."""

    @abstractmethod
    def __exit__(
        self, exc_type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        """Release the lock when exiting the context."""


def get_backend(name: str) -> type[AbstractBaseLock]:
    """Import the `locked_migrations.backends.Backend` subclass for the given module name."""
    module = importlib.import_module(f'locked_migrations.backends.{name}')
    for val in module.__dict__.values():
        try:
            is_subclass = issubclass(val, AbstractBaseLock)
        except TypeError:
            continue

        if is_subclass and val is not AbstractBaseLock:
            return val  # type: ignore[no-any-return]  # the conditional ensures this is a type[AbstractBaseLock]

    raise ValueError(f'No backend found for {name}')  # pragma: no cover
