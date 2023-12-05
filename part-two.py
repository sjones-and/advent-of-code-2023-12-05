#!/usr/bin/env python3

import os

def preprocess_lines(lines):
    lines = [tuple(map(int, line.split(' '))) for line in lines]
    return {line[1]: (line[0] - line[1], line[2]) for line in lines }

def get_map_values(input, lines):
    to_process = [i for i in input]
    output = []
    keys = sorted(lines.keys())
    while len(to_process) > 0:
        pair = to_process.pop()
        output_pair = None
        for key in keys:
            if key <= pair[0] and pair[0] < key + lines[key][1]:
                if key + lines[key][1] > pair[1]:
                    output_pair = (pair[0] + lines[key][0], pair[1] + lines[key][0])
                    break
                else:
                    output_pair = (pair[0] + lines[key][0], key + lines[key][1] + lines[key][0] - 1)
                    remainder_pair = (key + lines[key][1], pair[1])
                    to_process.append(remainder_pair)
                    break
            elif key <= pair[1] and pair[1] < key + lines[key][1]:
                output_pair = (key + lines[key][0], pair[1] + lines[key][0])
                remainder_pair = (pair[0], key - 1)
                to_process.append(remainder_pair)
                break

        output.append(output_pair or pair)
    return output

def get_mapping_data(mapping):
    lines = mapping.split('\n')
    title = lines[0].split(' ')[0]
    title_from, _, title_to = title.split('-')
    lines = preprocess_lines(lines[1:])
    fn = lambda input: get_map_values(input, lines)
    return [title_from, title_to, fn]

def answer(input_file):
    with open(input_file, "r") as input:
        data = input.read().split('\n\n')
    
    seeds = [int(seed) for seed in data[0][7:].split(' ')]
    seeds = [(seeds[index], seeds[index] + seeds[index + 1] - 1) for index in range(0, len(seeds), 2)]
    mappings = {mapping_data[0]: {
            'to': mapping_data[1],
            'fn': mapping_data[2]
        }
        for mapping_data in map(get_mapping_data, data[1:])
    }
    
    mapping_from = 'seed'
    current_values = seeds
    while mapping_from != 'location':
        mapping = mappings[mapping_from]
        mapping_from = mapping['to']
        current_values = mapping['fn'](current_values)

    answer = min([value[0] for value in current_values])

    print(f'The answer is: {answer}')

input_file = os.path.join(os.path.dirname(__file__), "input")
answer(input_file)
