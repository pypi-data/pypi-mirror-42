"""
Low level convenience utility functions.
"""

import random

DEFAULT_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def random_string(length=16, charset=DEFAULT_CHARSET):
    """
    Returns a random string of the given length using characters from the given charset.
    """
    return ''.join(random.choice(charset) for _ in range(length))
