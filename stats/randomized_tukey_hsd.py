import itertools
import math
import random


def system_mean(arr, col):
    # Get the mean over a single system (column)
    return sum(arr[i][col] for i in range(len(arr))) / len(arr)


def randomized_tukey_hsd(arr, B):
    """Conducts randomized Tukey HSD over B iterations."""
    num_systems = len(arr[0])
    num_topics = len(arr)
    num_pairs = num_systems * (num_systems - 1) // 2 # number of system pairs

    count = [0] * num_pairs
    system_means = [system_mean(arr, i) for i in range(num_systems)]
    d = [i - j for i, j in itertools.combinations(system_means, 2)]

    for b in range(B):
        for j in range(num_topics):
            random.shuffle(arr[j])
        replicate_means = [0] * num_systems
        for i in range(num_systems):
            replicate_means[i] = system_mean(arr, i)
        largest_difference = max(replicate_means) - min(replicate_means)
        for idx, difference in enumerate(d):
            if largest_difference >= abs(difference):
                count[idx] += 1

    i, j = 1, 2
    p_vals = {}
    for pair_val in count:
        p_vals[(i, j)] = pair_val / B
        j += 1
        if j > num_systems:
            i += 1
            j = i + 1
    return p_vals


def print_p_vals(p_vals):
    for system_pair, p_val in p_vals.items():
        print(f'Systems {system_pair}: p value {p_val}')


if __name__ == '__main__':
    # Test randomized_tukey_hsd using example from Sakai's Laboratory Experiments in Information Retrieval.
    import csv
    with open('20topics3runs.mat.csv', 'r') as f:
        mat = csv.reader(f)
        next(mat)  # Skips the header
        system_array = [list(map(float, i)) for i in mat]

    print("For B=5000, we get:")
    p_values = randomized_tukey_hsd(system_array, 5000)
    print_p_vals(p_values)
    
    print("\np values provided by Sakai:")
    print_p_vals({(1,2): 0.4996, (1,3): 0, (2,3): 0.0024})
