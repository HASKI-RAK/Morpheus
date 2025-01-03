"""
This file contains a function to learn transition probabilities
between learning elements for a Markov Chain model from learning path data.
The learned data is stored as a json file
"""

import argparse
import json
import os

import pandas as pd
from nltk.util import ngrams

conversion_map = {
    "LG": 0,
    "BO": 1,
    "MS": 2,
    "QU": 3,
    "EX": 4,
    "SU": 5,
    "AAM": 6,
    "TAM": 7,
    "VAM": 8,
}


def learn_transition_probs(learning_paths_csv_data, file_name, lstyle):
    """
    learn transition probabilites from learning path data
    :param learning_paths_csv_data: learning path data
    :param file_name: file name for storing the learned transition
    probabilities
    :param lstyle: learning style of model to be trained
    """
    data_np = learning_paths_csv_data.to_numpy()
    learning_paths = data_np.tolist()
    # dict to count each learning element being at first position
    first_le_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    # store all state transitions in dict (e.g. LG-> BO)
    le_permutations_dict = {
        0: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
        1: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
        2: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
        3: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
        4: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
        5: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
        6: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
        7: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
        8: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    }

    for z in learning_paths:
        # iterate over learning paths and count state combinations
        lp_converted = [conversion_map[y] for y in z]
        two_les_comb = list(ngrams(lp_converted, 2))
        for x in two_les_comb:
            le_permutations_dict[x[0]][x[1]] += 1
        first_le_dict[lp_converted[0]] += 1

    for a in list(le_permutations_dict.keys()):
        # count over all transitions from one state and normalize
        # to get transition probabilities
        sub_dict = le_permutations_dict[a]
        counter = 0
        for b in list(sub_dict.keys()):
            counter += sub_dict[b]
        for b in list(sub_dict.keys()):
            sub_dict[b] = sub_dict[b] / counter

    for z in first_le_dict.keys():
        # calculate initial state distribution probabilities
        first_le_dict[z] = first_le_dict[z] / len(learning_paths)

    # store transition probabilities and initial distribution matrix
    data = [first_le_dict, le_permutations_dict]
    path = os.getcwd() + r"\models\{}_{}.json".format(file_name, lstyle)
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train Markov Chains Command Line Interface"
    )
    parser.add_argument(
        "--path", type=str, default="test", help="Path to input data csv file"
    )
    parser.add_argument(
        "--output_filename", type=str, default="test",
        help="File name of trained model"
    )
    parser.add_argument(
        "--target_lstyle",
        type=str,
        default="Active",
        help="Learning style of input data csv file",
    )
    args = parser.parse_args()

    try:
        data = pd.read_csv(args.path, sep=";")
        file_name = args.output_filename
        learn_transition_probs(data, file_name, args.target_lstyle)

    except Exception as e:
        print(f"Error: {e}")
