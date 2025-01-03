import os
import unittest

import pandas as pd

from source.synthesizer.LPaths.hmm.learn_hmm import learn_model


class UnitTests(unittest.TestCase):

    def test_learn_hmm(self):
        """
        test if model is trained and stored correctly
        """
        # get path to test learning path data
        current_path = os.getcwd()
        data = pd.read_csv(current_path + r"\test_learning_path_data.csv",
                           sep=";")
        file_name = "testmodel"
        learn_model(data, file_name, "Active")
        file_path_to_check = current_path + r"\models\testmodel_Active.pkl"
        self.assertTrue(os.path.isfile(file_path_to_check))


if __name__ == "__main__":
    unittest.main()
