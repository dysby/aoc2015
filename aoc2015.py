#!/usr/bin/env python3
import argparse
import sys
from answers import (
    day01,
    day02,
    day03,
    day04,
    day05,
    day06,
    day07,
    day08,
    day09,
    day10,
    day11,
    day12,
    day13,
    day14,
    day15,
    day16,
    day17,
    day18,
    day19,
    day20,
    day21,
    day22,
    day23,
    day24,
)


def main(day: int, infile):
    module_name = "day" + str(day).zfill(2)
    module = __import__("answers." + module_name)
    func = getattr(module, module_name)
    func.run(infile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("day", help="day to answer in range 1..25", type=int)
    parser.add_argument(
        "infile",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="input file or stdin",
    )
    args = parser.parse_args()
    if args.day <= 0 or args.day > 25:
        parser.error("Day not in valid range 1 .. 26")
    main(args.day, args.infile)
