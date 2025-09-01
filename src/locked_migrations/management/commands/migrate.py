"""Override the built-in `django.core.management.commands.migrate.Command`."""

from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence
from typing import Any

from django.core.management.base import CommandParser
from django.core.management.commands.migrate import Command as BaseCommand

from locked_migrations.backends import AbstractBaseLock, get_backend

logger = logging.getLogger(__name__)


class GetBackend(argparse.Action):
    """Custom action to get the lock backend class from its name."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        """Set the backend class on the namespace."""
        setattr(namespace, self.dest, get_backend(str(values)))


class Command(BaseCommand):
    """Override the built-in `django.core.management.commands.migrate.Command`."""

    def add_arguments(self, parser: CommandParser) -> None:
        """Add two new arguments for specifying the lock backend and timeout."""
        super().add_arguments(parser)

        parser.add_argument(
            '--lock-backend',
            action=GetBackend,
            default=get_backend('file'),
            help='The locking backend to use during migrations',
            type=str,
        )

        parser.add_argument(
            '--lock-timeout',
            default=60,
            help='The number of seconds to wait for acquiring the lock before timing out; default is 60 seconds',
            type=int,
        )

    def handle(self, *args: Any, **options: Any) -> Any:
        """Execute the base method within a lock."""
        Lock: type[AbstractBaseLock] = options.pop('lock_backend')  # noqa: N806  # it's a class — should be capitalized
        timeout = options.pop('lock_timeout')

        lock = Lock()
        lock.acquire(timeout=timeout)

        try:
            return super().handle(*args, **options)
        finally:
            lock.release()


logger.debug('successfully imported %s', __name__)
