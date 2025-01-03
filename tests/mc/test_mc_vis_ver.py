import os
import unittest

from source.synthesizer.LPaths.mc import mc_vis_ver


class UnitTests(unittest.TestCase):

    def test_model_load(self):
        """
        test if model is correctly loaded from json file
        """
        # get path to visual data json file
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\mc\models\visual.json"
        first_le_probabilities_expected = {
            0: 0.07352941176470588,
            1: 0.07352941176470588,
            2: 0.19117647058823528,
            3: 0.20588235294117646,
            4: 0.23529411764705882,
            5: 0.14705882352941177,
            6: 0.0,
            7: 0.0,
            8: 0.07352941176470588,
        }
        # load model and initial distribution matrix
        model, first_le_probabilities = mc_vis_ver.load_model(path)
        self.assertEqual(first_le_probabilities,
                         first_le_probabilities_expected)

    def test_dict_conversion(self):
        """
        test if dict keys are converted correctly from string to int
        """
        test_dict = {"1": None, "2": None}
        expected_dict = {1: None, 2: None}
        # check dict conversion method
        self.assertEqual(mc_vis_ver.convert_keys_to_int(test_dict),
                         expected_dict)

    def test_data_synthesis_amount(self):
        """
        test if the wished amount of learning paths is synthesized
        correctly
        """
        # get path to verbal data json file
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\mc\models\verbal.json"
        model, first_le_probs = mc_vis_ver.load_model(path)
        # synthesize learning paths
        synthetic_lps = mc_vis_ver.sample_learning_paths(model, first_le_probs,
                                                         50)
        self.assertEqual(len(synthetic_lps), 50)

    def test_data_synthesis_length(self):
        """
        test if a synthetic learning path equals to the wished length of 9
        """
        # get path to visual data json file
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\mc\models\visual.json"
        model, first_le_probs = mc_vis_ver.load_model(path)
        # synthesize learning paths
        synthetic_lps = mc_vis_ver.sample_learning_paths(model, first_le_probs,
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
        synthetic_lps = mc_vis_ver.synthesize_data("Visual", 10)
        # check for amount of learning paths
        self.assertEqual(len(synthetic_lps), 10)


if __name__ == "__main__":
    unittest.main()
