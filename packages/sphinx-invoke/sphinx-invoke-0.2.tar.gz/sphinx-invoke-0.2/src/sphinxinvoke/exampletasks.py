from __future__ import print_function
from invoke import task  # pylint: disable=import-error


__copyright__ = 'Copyright (C) 2019, Nokia'


@task
def task_a(arga):
    """Task a description.

    Args:
        arga:   arga description
    """
    print(arga)


@task
def task_b(argb):
    """Task b description.

    Args:
        argb:   argb description
    """
    print(argb)
