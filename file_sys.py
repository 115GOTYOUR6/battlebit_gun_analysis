"""
This module contains functions that manipulate the file system.

Functions:
create_path -- creates the path given as a string in the users file system
"""

from pathlib import Path


def create_path(path):
    """Create the path in the file system."""
    if path[-1] != '/':
        path = path+'/'
    save_path = Path(path)
    if not save_path.exists():
        save_path.mkdir(parents=True)

    return path
