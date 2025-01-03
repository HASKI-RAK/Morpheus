import os
import unittest

import numpy as np

from source.synthesizer.LPaths.hmm import hmm_act_ref


class UnitTests(unittest.TestCase):

    def test_model_load(self):
        """
        test if model is loaded correctly by checking transition matrix
        """
        # get path to active hmm model
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\hmm\models\model_act.pkl"
        # load model
        model = hmm_act_ref.load_model(path)
        expected_trans_mat = np.array(
            [[0.84676703, 0.15323297], [0.03105931, 0.96894069]]
        )
        self.assertTrue(np.allclose(model.transmat_, expected_trans_mat))

    def test_data_synthesis_amount(self):
        """
        test if the wished amount of learning paths is synthesized
        correctly
        """
        # get path to reflective hmm model
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\hmm\models\model_ref.pkl"
        model = hmm_act_ref.load_model(path)
        # synthesize learning paths
        synthetic_lps = hmm_act_ref.sample_learning_paths(model, 50)
        self.assertEqual(len(synthetic_lps), 50)

    def test_data_synthesis_length(self):
        """
        test if a synthetic learning path equals to the wished length of 9
        """
        # get path to reflective hmm model
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\hmm\models\model_ref.pkl"
        model = hmm_act_ref.load_model(path)
        # synthesize learning paths
        synthetic_lps = hmm_act_ref.sample_learning_paths(model, 30)
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
        synthetic_lps = hmm_act_ref.synthesize_data("Active", 10)
        # check for amount of learning paths
        self.assertEqual(len(synthetic_lps), 10)


if __name__ == "__main__":
    unittest.main()
