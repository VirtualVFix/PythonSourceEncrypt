# All rights reserved by forest fairy.
# You cannot modify or share anything without sacrifice.
# If you don't agree, keep calm and don't look on text below...

__author__ = "VirtualV <github.com/virtualvfix>"
__date__ = "04/11/18 11:56"

from timeit import timeit


def factorial(number):
    """ recursion factorial """
    return 1 if number <= 1 else number * factorial(number - 1)


def factorial_loop(number):
    """ loop factorial """
    result = 1
    for x in range(2, number+1, 1):
        result *= x
    return result


def factorial_test(number):
    print('Recursion factorial of %s: %s in %s sec.' % (number, factorial(number),
                                                        timeit('factorial(number)', setup="number=%s" % number,
                                                               globals=globals(), number=10000)))
    print('Loop factorial of %s: %s in %s sec.' % (number, factorial_loop(number),
                                                   timeit('factorial_loop(number)', setup="number=%s" % number,
                                                          globals=globals(), number=10000)))


if __name__ == '__main__':
    factorial_test(30)
