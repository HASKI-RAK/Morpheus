import os

import pandas as pd


def store_data_in_csv(data, file_name):
    """
    store data in csv files
    :param data: dictionary of data
    :param file_name: name of the csv file (prefix)
    """
    path = os.path.dirname(__file__)
    path = path.replace(r"\source\synthesizer\LPaths", "")
    columns = ["LE1", "LE2", "LE3", "LE4", "LE5", "LE6", "LE7", "LE8", "LE9"]
    for z in data.keys():
        storage_path = path + r"\data\synthetic\{}_{}.csv".format(file_name, z)
        synthesized_data_lists = data[z]
        synthesized_data_df = pd.DataFrame(synthesized_data_lists,
                                           columns=columns)
        synthesized_data_df.to_csv(storage_path)
