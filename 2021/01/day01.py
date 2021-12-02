#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 01
"Sonar Sweep"
"""

from os.path import join, dirname, realpath
from argparse import ArgumentParser
from functools import reduce
from math import inf
from sys import stderr

__author__ = "John P Lettman"
__email__ = "the@johnlettman.com"
__license__ = "MIT"

CHALLENGE = """
As the submarine drops below the surface of the ocean, it automatically performs
a sonar sweep of the nearby sea floor. On a small screen, the sonar sweep report
(your puzzle input) appears: each line is a measurement of the sea floor depth
as the sweep looks further and further away from the submarine.

For example, suppose you had the following report:

199
200
208
210
200
207
240
269
260
263

This report indicates that, scanning outward from the submarine, the sonar sweep
found depths of 199, 200, 208, 210, and so on.

The first order of business is to figure out how quickly the depth increases,
just so you know what you're dealing with - you never know if the keys will get
carried into deeper water by an ocean current or a fish or something.

To do this, count the number of times a depth measurement increases from the
previous measurement. (There is no measurement before the first measurement.)
In the example above, the changes are as follows:

199 (N/A - no previous measurement)
200 (increased)
208 (increased)
210 (increased)
200 (decreased)
207 (increased)
240 (increased)
269 (increased)
260 (decreased)
263 (increased)

--- Part Two ---

Considering every single measurement isn't as useful as you expected: there's
just too much noise in the data.

Instead, consider sums of a three-measurement sliding window. Again considering
the above example:

199  A      
200  A B    
208  A B C  
210    B C D
200  E   C D
207  E F   D
240  E F G  
269    F G H
260      G H
263        H

Start by comparing the first and second three-measurement windows. The
measurements in the first window are marked A (199, 200, 208); their sum is
199 + 200 + 208 = 607. The second window is marked B (200, 208, 210); its sum is
618. The sum of measurements in the second window is larger than the sum of the
first, so this first comparison increased.

Your goal now is to count the number of times the sum of measurements in this
sliding window increases from the previous sum. So, compare A with B, then
compare B with C, then C with D, and so on. Stop when there aren't enough
measurements left to create a new three-measurement sum.

In the above example, the sum of each three-measurement window is as follows:

A: 607 (N/A - no previous sum)
B: 618 (increased)
C: 618 (no change)
D: 617 (decreased)
E: 647 (increased)
F: 716 (increased)
G: 769 (increased)
H: 792 (increased)

In this example, there are 5 sums that are larger than the previous sum.
"""


def increases(measurements: iter, window_size: int = 1, verbose: bool = True) -> int:
    """
    Count the number of increases from a list of sonar measurements.

    Function is capable of outputting a processing sequence similar to challenge
    documentation to stderr for debugging purposes.

    Parameters:
    measurements (iter): Iterable list of sonar measurements
    window_size (int): Sliding window size for accuracy tuning
    verbose (bool): Output processing sequence to stderr

    Returns:
    int: Number of increases in sonar measurements 
    """
    # This function bends the Python language in every imaginable way.

    if window_size <= 0:
        # range check the window size for sensible values
        raise ValueError("Window size must be greater than zero")

    def out(new: float, window: list, increase: bool = False) -> None:
        """
        Output a representation of the window and increase/decrease state if
        verbose is enabled.

        Attempts to round the new measurement to a human-readable value taking
        in to account infinity values (used at the start).

        No-op if verbose is not enabled.

        Parameters:
        new (float): Current measurement value
        window (list): Current measurement window
        increase (bool): Defines whether the last operation was an increase
        """
        if verbose:
            repr = f"{'inf' if new == inf else round(new)} window({','.join(map(str, window))})" if window_size > 1 else new
            print(f"{repr} ({'increase' if increase else 'decrease'})", file=stderr)

    def count(last: tuple, measurement: float) -> tuple:
        """
        Add the next measurement to the sliding window and increment increases
        if the new window is greater than the old window.

        Parameters:
        last (tuple): Last (increases, window) values from previous call of the function
        measurement (float): Next measurement
        """
        # extract last values
        increases, window = last

        # calculate new working values
        window = window + [measurement]  # add next measurement to window
        new = sum(window[1:]) / window_size  # slide over 1 to sum new window
        old = sum(window[:-1]) / window_size  # slide back 1 to sum old window

        # compare
        if new > old:
            out(new, window[1:], True)
            increases += 1  # new window is greater, increase
        else:
            out(new, window[1:])

        return increases, window[1:]

    # reduce all measurements through count() with:
    # - increases: 0 (accumulator starts at 0)
    # - window: array of window_size len containing infinities to N/A first comparisons
    incr, _ = reduce(count, measurements, (0, [inf] * window_size))
    return incr


def main():
    """Command-line interface main function."""
    parser = ArgumentParser(prog="day01", description=__doc__)
    parser.add_argument("-c", "--challenge",
                        action="store_true", help="show the Advent of Code challenge and exit")
    parser.add_argument("-m", "--measurements", metavar="FILE", default=join(
        dirname(realpath(__file__)), "input.txt"), help="path to the measurements file")
    parser.add_argument("-w", "--window", type=int, default=1,
                        help="sliding window size for accuracy tuning")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")

    args = parser.parse_args()

    if args.challenge:
        print(CHALLENGE)
        return

    with open(args.measurements, 'r') as lines:
        measurements = map(lambda line: int(line.strip()), lines)
        count = increases(measurements, args.window, args.verbose)
        print(count)


if __name__ == "__main__":
    main()
