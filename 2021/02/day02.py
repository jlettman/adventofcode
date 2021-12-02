#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 02
"Dive!"
"""

from os.path import join, dirname, realpath
from argparse import ArgumentParser
from functools import reduce
from sys import stderr

__author__ = "John P Lettman"
__email__ = "the@johnlettman.com"
__license__ = "MIT"


CHALLENGE = """
Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1,
down 2, or up 3:

    forward X increases the horizontal position by X units.
    down X increases the depth by X units.
    up X decreases the depth by X units.

Note that since you're on a submarine, down and up affect your depth, and so
they have the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You
should probably figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2

Your horizontal position and depth both start at 0. The steps above would then
modify them as follows:

    forward 5 adds 5 to your horizontal position, a total of 5.
    down 5 adds 5 to your depth, resulting in a value of 5.
    forward 8 adds 8 to your horizontal position, a total of 13.
    up 3 decreases your depth by 3, resulting in a value of 2.
    down 8 adds 8 to your depth, resulting in a value of 10.
    forward 2 adds 2 to your horizontal position, a total of 15.

After following these instructions, you would have a horizontal position of 15
and a depth of 10. (Multiplying these together produces 150.)

--- Part Two ---

Based on your calculations, the planned course doesn't seem to make any sense.
You find the submarine manual and discover that the process is actually slightly
more complicated.

In addition to horizontal position and depth, you'll also need to track a third
value, aim, which also starts at 0. The commands also mean something entirely
different than you first thought:

    down X increases your aim by X units.
    up X decreases your aim by X units.
    forward X does two things:
        It increases your horizontal position by X units.
        It increases your depth by your aim multiplied by X.

Again note that since you're on a submarine, down and up do the opposite of what
you might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

    forward 5 adds 5 to your horizontal position, a total of 5. 
    Because your aim is 0, your depth does not change.
    down 5 adds 5 to your aim, resulting in a value of 5.
    forward 8 adds 8 to your horizontal position, a total of 13. 
    Because your aim is 5, your depth increases by 8*5=40.

    up 3 decreases your aim by 3, resulting in a value of 2.
    down 8 adds 8 to your aim, resulting in a value of 10.
    forward 2 adds 2 to your horizontal position, a total of 15. 
    Because your aim is 10, your depth increases by 2*10=20 to a total of 60.

After following these new instructions, you would have a horizontal position of
15 and a depth of 60. (Multiplying these produces 900.)
"""

MOVE_UP = "up"
MOVE_DOWN = "down"
MOVE_FORWARD = "forward"


def interpret(instruction: str) -> tuple:
    """
    Split and interpret a piloting instruction and return a tuple of action and
    units.

    Paramaters:
    instruction (str): Instruction to interpret

    Returns
    tuple: Tuple of action and units
    """
    action, units = instruction.split(" ", 1)
    units = int(units)
    return (action, units)


def process_simple(last: tuple, instruction: str) -> tuple:
    """
    Process instructions using simple mode (non-aim) and return the new tuple of
    horizontal and depth.

    Parameters:
    last (tuple): Last values of horizontal and depth
    instruction (str): Current instruction

    Returns:
    tuple: New values of horizontal and depth
    """
    # extract last values
    horiz, depth = last

    # interpret the instruction
    action, units = interpret(instruction)

    if action == MOVE_UP:
        depth -= units
    elif action == MOVE_DOWN:
        depth += units
    elif action == MOVE_FORWARD:
        horiz += units
    else:
        raise ValueError(f"Unknown pilot command: {action}")

    return (horiz, depth)


def process_advanced(last: tuple, instruction: str) -> tuple:
    """
    Process instructions using advanced mode (aim) and return the new tuple of
    horizontal, depth, and aim.

    Parameters:
    last (tuple): Last values of horizontal, depth, and aim
    instruction (str): Current instruction

    Returns:
    tuple: New values of horizontal, depth, and aim
    """

    # extract last values
    horiz, depth, aim = last

    # interpret the instruction
    action, units = interpret(instruction)

    if action == MOVE_UP:
        aim -= units
    elif action == MOVE_DOWN:
        aim += units
    elif action == MOVE_FORWARD:
        horiz += units
        depth += units * aim
    else:
        raise ValueError(f"Unknown pilot command: {action}")

    return (horiz, depth, aim)


def pilot(instructions: iter, advanced: bool = False) -> int:
    """
    Pilot a submarine using a list of instructions.

    Parameters:
    instructions (iter): Iterable list of piloting instructions
    advanced (bool): Use advanced (aim) mode as per part 2

    Returns:
    int: Value of (horizontal * depth) distance measurements
    """

    if advanced:
        horiz, depth, _ = reduce(process_advanced, instructions, (0, 0, 0))
    else:
        horiz, depth = reduce(process_simple, instructions, (0, 0))

    return (horiz * depth)


def main():
    """Command-line interface main function."""
    parser = ArgumentParser(prog="day02", description=__doc__)
    parser.add_argument("-c", "--challenge",
                        action="store_true", help="show the Advent of Code challenge and exit")
    parser.add_argument("-i", "--instructions", metavar="FILE", default=join(
        dirname(realpath(__file__)), "input.txt"), help="path to the instructions file")
    parser.add_argument("-a", "--advanced", action="store_true",
                        help="use advanced (aim) mode")
    args = parser.parse_args()

    if args.challenge:
        print(CHALLENGE)
        return

    with open(args.instructions, 'r') as lines:
        instructions = map(lambda line: line.strip(), lines)
        res = pilot(instructions, args.advanced)
        print(res)


if __name__ == "__main__":
    main()
