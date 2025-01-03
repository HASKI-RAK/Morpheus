import os
import unittest

import pandas as pd

from source.synthesizer.LPaths.mc.learn_transition_probs import learn_transition_probs  # nopep8


class UnitTests(unittest.TestCase):

    def test_learn_transition_probs(self):
        """
        test if model is trained and stored correctly
        """
        # get path to test learning path data
        current_path = os.getcwd()
        data = pd.read_csv(current_path + r"\test_learning_path_data.csv",
                           sep=";")
        file_name = "test_model"
        learn_transition_probs(data, file_name, "Active")
        file_path_to_check = current_path + r"\models\test_model_Active.json"
        self.assertTrue(os.path.isfile(file_path_to_check))


if __name__ == "__main__":
    unittest.main()
