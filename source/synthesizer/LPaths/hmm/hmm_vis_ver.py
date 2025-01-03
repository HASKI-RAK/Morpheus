import os
import pickle

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


def sample_learning_paths(model, data_size):
    """
    synthesize learning paths with a specified data size
    :param model: Hidden Markov Model
    :param data_size: amount of data entries
    """
    lps = []
    for z in range(data_size):
        lp = model.sample(9)
        lp_list = lp[0].tolist()
        lp_list_cleaned = [conversion_map[z[0]] for z in lp_list]
        lps.append(lp_list_cleaned)
    return lps


def load_model(path):
    """
    load model and return it
    :param path: storage path of pickled hidden markov model
    :return: Hidden Markov Model
    """
    with open(path, "rb") as file:
        model = pickle.load(file)
    return model


def synthesize_data(learning_style, data_size):
    """
    synthesize amount of learning paths for a given learning style
    """
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    if learning_style == "Visual":
        path = current_directory + r"\models\model_vis.pkl"
    else:
        path = current_directory + r"\models\model_ver.pkl"

    model = load_model(path)
    synthetic_learning_paths = sample_learning_paths(model, data_size)

    return synthetic_learning_paths


if __name__ == "__main__":
    synthetic_lps_visual = synthesize_data("Visual", 10)
