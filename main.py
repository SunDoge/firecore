from firecore._arguments import BaseArgument
from dataclasses import dataclass
import argparse


@dataclass
class Args(BaseArgument):
    num_workers: int = 8


parser = argparse.ArgumentParser()

Args.add_arguments(parser, "train")

ns = parser.parse_args()

args = Args.from_arguments(ns, "train")
print(args)
