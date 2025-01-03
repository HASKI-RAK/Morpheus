import json
import os

import numpy as np
from pgmpy.factors.discrete import State
from pgmpy.models import MarkovChain as Mc

conversion_map = {
    0: "LG",
    1: "BO",
    2: "MS",
    3: "QU",
    4: "EX",
    5: "SU",
    6: "AAM",
    7: "TAM",
    8: "VAM",
}


def convert_keys_to_int(d):
    """
    convert the keys of a dictionary from type str to type int
    """
    if isinstance(d, dict):
        new_dict = {}
        for key, value in d.items():
            new_key = int(key) if isinstance(key, str) and key.isdigit() else key  # nopep8
            new_dict[new_key] = convert_keys_to_int(value)
        return new_dict
    else:
        return d


def sample_learning_paths(mc, initial_state_dist, data_size):
    """
    synthesize learning paths with a specified data size
    :param mc: Markov Chain
    :param initial_state_dist: probability distribution of initial states
    :param data_size: amount of data entries
    """
    synthetic_learning_paths = []
    for z in range(data_size):
        start_number = np.random.choice(
            np.arange(0, 9), p=list(initial_state_dist.values())
        )
        start_state = [State("Learning Paths", start_number)]
        learning_path = mc.sample(start_state, size=9)
        list_sample_lp = learning_path.to_numpy().tolist()
        list_sample_lp_cleaned = []
        for c in list_sample_lp:
            list_sample_lp_cleaned.append(c[0])
        learning_path_converted = [conversion_map[z] for z in list_sample_lp_cleaned]  # nopep8
        synthetic_learning_paths.append(learning_path_converted)
    return synthetic_learning_paths


def load_model(path):
    """
    load transition probabilities from json file and return model
    :param path: storage path of json file
    :return: Markov Chain model and probabilities of first learning element
    """
    with open(path, "r") as json_file:
        data = json.load(json_file)
    first_le_probabilities = convert_keys_to_int(data[0])
    le_transition_model = convert_keys_to_int(data[1])
    model = Mc()
    model.add_variable("Learning Paths", 9)
    model.add_transition_model("Learning Paths", le_transition_model)
    return model, first_le_probabilities


def synthesize_data(learning_style, data_size):
    """
    synthesize amount of learning paths for a given learning style
    """
    current_path = os.path.dirname(__file__)
    if learning_style == "Visual":
        path = current_path + r"\models\visual.json"
    else:
        path = current_path + r"\models\verbal.json"

    model, first_le_probabilities = load_model(path)
    synthetic_learning_paths = sample_learning_paths(
        model, first_le_probabilities, data_size
    )
    return synthetic_learning_paths
