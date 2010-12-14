"""
Django App Test Helpers
"""
from django.test import TestCase as DjangoTestCase

from contextlib import contextmanager

class TestCase(DjangoTestCase):
    @contextmanager
    def assertChanges(self, thing, attr=None, by=None):
        """
        Context manager to Fail unless thing (or thing.attr) changes (by a
        value, if 'by' is specified.

        :param `thing`: callable or object
        :param `attr`: if thing is an object, name of an attribute to watch
        :param `by`: optional delta to check for

        Example code:

        >>> with self.assertChanges(object_pool.count, 5):
        ...    for x in xrange(10):
        ...        object_pool.add(x)
        Traceback (most recent call last):
            ...
        AssertionError
        """
        def get_value(thing, attr):
            if callable(thing):
                value = thing()
            else:
                value = getattr(thing, attr)
            return value

        old_value = get_value(thing, attr)
        yield
        new_value = get_value(thing, attr)

        if by is None:
            self.assertNotEqual(new_value, old_value)
        else:
            self.assertEqual(new_value - old_value, by)
