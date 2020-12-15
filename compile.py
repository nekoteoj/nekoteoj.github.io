#! /usr/bin/env python3

from config import config
from generator.generator import Generator

def main():
    generator = Generator(config)
    generator.generate()


if __name__ == "__main__":
    main()
