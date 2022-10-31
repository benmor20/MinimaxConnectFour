"""
Script to visualize the results of A/B pruning
"""
import json
import numpy as np
from matplotlib import pyplot as plt
from typing import *


def get_data(results: Dict[str, Dict[str, int]], key: str) -> np.ndarray:
    """
    Pulls the data from the results into a ndarray

    :param results: a dict of dicts, the data to pull from
    :param key: a string, the key in the second layer of dictionaries to pull from
    :return: an ndarray vector containing the values of the key for each dict
    """
    return np.array([v[key] for v in results.values()])


def main():
    """
    Plot the results of graph_results.py
    """
    # Get results
    folder = '\\'.join(__file__.split('\\')[:-1])
    print(__file__)
    with open('game_results.json', 'r') as file:
        results = json.load(file)

    # Pull the data
    depths = np.array([int(d) for d in results])
    reg_cnt = get_data(results, 'regular_count')
    reg_turns = get_data(results, 'regular_turns')
    reg_scaled = reg_cnt / reg_turns
    ab_cnt = get_data(results, 'ab_count')
    ab_turns = get_data(results, 'ab_turns')
    ab_scaled = ab_cnt / ab_turns

    # See if AB pruning changed the outcomes
    print(get_data(results, 'regular_board') == get_data(results, 'ab_board'))

    # Plot linear scale
    plt.plot(depths, reg_scaled)
    plt.plot(depths, ab_scaled)
    plt.legend(['Regular', 'Alpha-Beta Pruning'])
    plt.xticks(depths)
    plt.xlabel('Depth (turns)')
    plt.ylabel('Number of Recursive Calls')
    plt.title('Number of Calls with and without Alpha-Beta Pruning')
    plt.show()

    # Plot log scale
    plt.plot(depths, reg_scaled)
    plt.plot(depths, ab_scaled)
    plt.yscale('log')
    plt.legend(['Regular', 'Alpha-Beta Pruning'])
    plt.xticks(depths)
    plt.xlabel('Depth (turns)')
    plt.ylabel('Number of Recursive Calls (log scale)')
    plt.title('Number of Calls with and without Alpha-Beta Pruning')
    plt.show()

    # Calculate and plot percentage over time
    percentages = ab_scaled / reg_scaled * 100
    print(', '.join(f'{p:.3f}' for p in percentages))
    plt.plot(depths, np.ones(depths.shape) * 100)
    plt.plot(depths, percentages)
    plt.legend(['Regular', 'Alpha-Beta Pruning'])
    plt.xticks(depths)
    plt.xlabel('Depth (turns)')
    plt.ylabel('Percentage of Calls against Plain Minimax')
    plt.title('Alpha-Beta Pruning Improvement')
    plt.show()


if __name__ == '__main__':
    main()
