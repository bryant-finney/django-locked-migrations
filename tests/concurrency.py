"""Spawn a set of subprocesses to execute concurrent migrations."""

from __future__ import annotations

import logging
import multiprocessing as mp

import django
from django.core.management import call_command

logger = logging.getLogger(__name__)


def migrate(i_runner: int) -> None:
    """Invoke the `migrate` command."""
    django.setup()

    logger.info('Runner %d is executing the migrate command', i_runner)

    try:
        call_command('migrate')
    except Exception:
        logger.exception('Runner %d failed', i_runner)


def main() -> None:
    """Spawn a pool of 10 subprocesses that each executes `django-admin migrate`."""
    with mp.Pool(processes=10) as pool:
        pool.map(migrate, range(10))


if __name__ == '__main__':
    main()
else:
    logger.debug('successfully imported %s', __name__)
