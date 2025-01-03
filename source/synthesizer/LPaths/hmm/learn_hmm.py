import argparse
import os
import pickle

import hmmlearn.hmm as hmm
import pandas as pd

conversion_map_datadriven = {
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


def learn_model(data, file_name, learning_style):
    """
    learn model for learning path data and store the amount of hidden states
    leading to the lowest bic value
    :param data: learning path data
    :param file_name: file name of stored model
    :param learning_style: learning style for that the learning path data
    is given
    """
    # convert data to a list of learning paths
    data_list = data.to_numpy().tolist()
    data_cleaned = []
    for z in data_list:
        # convert string values to corresponding ints
        lp_converted = [conversion_map_datadriven[x] for x in z]
        data_cleaned.append(lp_converted)

    bics = []
    models = []
    for n in range(1, 20):
        # calculate bic scores for models for various number of hidden states
        model = hmm.CategoricalHMM(n_components=n)
        model.fit(data_cleaned)
        score = model.bic(data_cleaned)
        bics.append(score)
        models.append(model)

    # get lowest bic value and therefore best fitting model
    lowest_bic_idx = bics.index(min(bics))
    best_model = models[lowest_bic_idx]

    storage_path = os.getcwd() + r"\models\{}_{}.pkl".format(file_name,
                                                             learning_style)

    with open(storage_path, "wb") as file:
        # store best model as pkl file
        pickle.dump(best_model, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train Hidden Markov Command Line Interface"
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
        learn_model(data, file_name, args.target_lstyle)

    except Exception as e:
        print(f"Error: {e}")
