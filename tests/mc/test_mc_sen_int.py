import os
import unittest

from source.synthesizer.LPaths.mc import mc_sen_int


class UnitTests(unittest.TestCase):

    def test_model_load(self):
        """
        test if model is correctly loaded from json file
        """
        # get path to sensory data json file
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\mc\models\sensory.json"
        first_le_probabilities_expected = {
            0: 0.13793103448275862,
            1: 0.1896551724137931,
            2: 0.1724137931034483,
            3: 0.05172413793103448,
            4: 0.27586206896551724,
            5: 0.15517241379310345,
            6: 0.0,
            7: 0.0,
            8: 0.017241379310344827,
        }
        # load model and initial distribution matrix
        model, first_le_probabilities = mc_sen_int.load_model(path)
        self.assertEqual(first_le_probabilities,
                         first_le_probabilities_expected)

    def test_dict_conversion(self):
        """
        test if dict keys are converted correctly from string to int
        """
        test_dict = {"1": None, "2": None}
        expected_dict = {1: None, 2: None}
        # check dict conversion method
        self.assertEqual(mc_sen_int.convert_keys_to_int(test_dict),
                         expected_dict)

    def test_data_synthesis_amount(self):
        """
        test if the wished amount of learning paths is synthesized
        correctly
        """
        # get path to intuitive data json file
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\mc\models\intuitive.json"
        model, first_le_probs = mc_sen_int.load_model(path)
        # synthesize learning paths
        synthetic_lps = mc_sen_int.sample_learning_paths(model, first_le_probs,
                                                         50)
        self.assertEqual(len(synthetic_lps), 50)

    def test_data_synthesis_length(self):
        """
        test if a synthetic learning path equals to the wished length of 9
        """
        # get path to sensory data json file
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\mc\models\sensory.json"
        model, first_le_probs = mc_sen_int.load_model(path)
        # synthesize learning paths
        synthetic_lps = mc_sen_int.sample_learning_paths(model, first_le_probs,
                                                         30)
        # take one learning path out of data
        one_synthetic_lp = synthetic_lps[25]
        # check learning path length
        self.assertEqual(len(one_synthetic_lp), 9)

    def test_synthesize_data(self):
        """
        test if the wished amount of learning paths is synthesized
        correctly by using the outer method for data synthesis
        """
        # synthesize learning paths
        synthetic_lps = mc_sen_int.synthesize_data("Sensory", 10)
        # check for amount of learning paths
        self.assertEqual(len(synthetic_lps), 10)


if __name__ == "__main__":
    unittest.main()