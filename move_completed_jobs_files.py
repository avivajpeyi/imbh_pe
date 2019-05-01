#!/usr/bin/env python3
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("--cur", "-c", type=str, help="current path with jobs data")
    parser.add_argument(
        "--new", "-n", type=str, help="new path to place completed jobs"
    )
    args = parser.parse_args()

    assert os.path.isdir(args.cur)

    copy_files(curr_dir=args.cur, new_dir=args.new)


def copy_files(curr_dir, new_dir):
    pass


if __name__ == "__main__":
    main()
