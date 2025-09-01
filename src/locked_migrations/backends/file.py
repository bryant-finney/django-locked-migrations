"""Define a file-based locking backend."""

from __future__ import annotations

import logging
from typing import Any

from django.conf import settings
from filelock import FileLock as BaseFileLock

from locked_migrations.backends import AbstractBaseLock

logger = logging.getLogger(__name__)


class FileLock(AbstractBaseLock):
    """A file-based locking backend (not for use in production).

    WARNING: This backend is not effective for distributed systems because it relies on the local filesystem of a single
    host.
    """

    def __init__(self) -> None:
        """Use a containment strategy to wrap the `filelock.FileLock` class."""
        lockfile = getattr(settings, 'LOCKED_MIGRATIONS_LOCKFILE', 'migrations.lock')
        self._lock = BaseFileLock(lockfile, blocking=True)

    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
        """Acquire the lock, blocking or non-blocking."""
        return self._lock.acquire(blocking=blocking, timeout=timeout).lock.is_locked

    def release(self) -> None:
        """Release the lock."""
        self._lock.release()

    def locked(self) -> bool:
        """Return `True` if the lock is acquired."""
        return self._lock.is_locked

    def __enter__(self) -> bool:
        """Acquire the lock when entering a `with` statement context."""
        return self._lock.acquire().lock.is_locked

    def __exit__(self, exc_type: type[BaseException] | None, value: BaseException | None, traceback: Any) -> None:
        """Release the lock when exiting the context."""
        self._lock.release()


logger.debug('successfully imported %s', __name__)
