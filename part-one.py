#!/usr/bin/env python3

import os
from time import perf_counter_ns

def preprocess_lines(lines):
    lines = [tuple(map(int, line.split(' '))) for line in lines]
    return {line[1]: (line[0] - line[1], line[2]) for line in lines }

def get_map_value(input, lines):
    for key in sorted(lines.keys()):
        if key <= input and input < key + lines[key][1]:
            return input + lines[key][0]
    return input

def get_mapping_data(mapping):
    lines = mapping.split('\n')
    title = lines[0].split(' ')[0]
    title_from, _, title_to = title.split('-')
    lines = preprocess_lines(lines[1:])
    fn = lambda input: get_map_value(input, lines)
    return [title_from, title_to, fn]

def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, "r") as input:
        data = input.read().split('\n\n')
    
    seeds = [int(seed) for seed in data[0][7:].split(' ')]
    mappings = {mapping_data[0]: {
            'to': mapping_data[1],
            'fn': mapping_data[2]
        }
        for mapping_data in map(get_mapping_data, data[1:])
    }
    
    seed_locations = {}

    for seed in seeds:
        mapping_from = 'seed'
        current_value = seed
        while mapping_from != 'location':
            mapping = mappings[mapping_from]
            mapping_from = mapping['to']
            current_value = mapping['fn'](current_value)
        seed_locations[seed] = current_value

    answer = min(seed_locations.values())
    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), "input")
answer(input_file)
