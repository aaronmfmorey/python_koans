#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

from runner.koan import *


class AboutDecoratingWithClasses(Koan):
    def maximum(self, a, b):
        if a>b:
            return a
        else:
            return b

    def test_partial_that_wrappers_no_args(self):
        """
        Before we can understand this type of decorator we need to consider
        the partial.
        """
        max = functools.partial(self.maximum)

        self.assertEqual(23, max(7, 23))
        self.assertEqual(10, max(10, -10))

    def test_partial_that_wrappers_first_arg(self):
        max0 = functools.partial(self.maximum, 0)

        self.assertEqual(0, max0(-4))
        self.assertEqual(5, max0(5))

    def test_partial_that_wrappers_all_args(self):
        always99 = functools.partial(self.maximum, 99, 20)
        always20 = functools.partial(self.maximum, 9, 20)

        self.assertEqual(99, always99())
        self.assertEqual(20, always20())

    # ------------------------------------------------------------------

    class doubleit:
        def __init__(self, fn):
            self.fn = fn

        def __call__(self, *args):
            return self.fn(*args) + ', ' + self.fn(*args)

        def __get__(self, obj, cls=None):
            if not obj:
                # Decorating an unbound function
                return self
            else:
                # Decorating a bound method
                return functools.partial(self, obj)

    @doubleit
    def foo(self):
        return "foo"

    @doubleit
    def parrot(self, text):
        return text.upper()

    def test_decorator_with_no_arguments(self):
        # To clarify: the decorator above the function has no arguments, even
        # if the decorated function does

        self.assertEqual("foo, foo", self.foo())
        self.assertEqual("PIECES OF EIGHT, PIECES OF EIGHT", self.parrot('pieces of eight'))

    # ------------------------------------------------------------------

    def sound_check(self):
        #Note: no decorator
        return "Testing..."

    def test_what_a_decorator_is_doing_to_a_function(self):
        #wrap the function with the decorator
        self.sound_check = self.doubleit(self.sound_check)
        self.assertEqual('Testing..., Testing...', self.sound_check())

    # ------------------------------------------------------------------

    class documenter:
        def __init__(self, *args):
            self.fn_doc = args[0]

        def __call__(self, fn):
            def decorated_function(*args):
                return fn(*args)

            if fn.__doc__:
                decorated_function.__doc__ = fn.__doc__ + ": " + self.fn_doc
            else:
                decorated_function.__doc__ = self.fn_doc
            return decorated_function

    @documenter("Increments a value by one. Kind of.")
    def count_badly(self, num):
        num += 1
        if num==3:
            return 5
        else:
            return num
    @documenter("Does nothing")
    def idler(self, num):
        "Idler"
        pass

    def test_decorator_with_an_argument(self):
        self.assertEqual(5, self.count_badly(2))
        self.assertEqual("Increments a value by one. Kind of.", self.count_badly.__doc__)

    def test_documentor_which_already_has_a_docstring(self):
        self.assertEqual("Idler: Does nothing", self.idler.__doc__)

    # ------------------------------------------------------------------

    @documenter("DOH!")
    @doubleit
    @doubleit
    def homer(self):
        return "D'oh"

    def test_we_can_chain_decorators(self):
        self.assertEqual("D'oh, D'oh, D'oh, D'oh", self.homer())
        self.assertEqual("DOH!", self.homer.__doc__)
