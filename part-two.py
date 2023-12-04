#!/usr/bin/env python3

import os

def answer(input_file):
    with open(input_file, "r") as input:
        data = input.read().split('\n')

    answer = None

    print(f'The answer is: {answer}')

input_file = os.path.join(os.path.dirname(__file__), "input")
answer(input_file)
