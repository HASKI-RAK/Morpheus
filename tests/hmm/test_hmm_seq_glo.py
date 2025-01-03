import os
import unittest

import numpy as np

from source.synthesizer.LPaths.hmm import hmm_seq_glo


class UnitTests(unittest.TestCase):

    def test_model_load(self):
        """
        test if model is loaded correctly by checking transition matrix
        """
        # get path to sequential hmm model
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\hmm\models\model_seq.pkl"
        # load model
        model = hmm_seq_glo.load_model(path)
        expected_trans_mat = np.array([[1]])
        self.assertTrue(np.allclose(model.transmat_, expected_trans_mat))

    def test_data_synthesis_amount(self):
        """
        test if the wished amount of learning paths is synthesized
        correctly
        """
        # get path to global hmm model
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\hmm\models\model_glo.pkl"
        model = hmm_seq_glo.load_model(path)
        # synthesize learning paths
        synthetic_lps = hmm_seq_glo.sample_learning_paths(model, 50)
        self.assertEqual(len(synthetic_lps), 50)

    def test_data_synthesis_length(self):
        """
        test if a synthetic learning path equals to the wished length of 9
        """
        # get path to global hmm model
        current_path = os.getcwd()
        path_parent = current_path.replace(r"\tests", r"\source")
        path = path_parent + r"\synthesizer\LPaths\hmm\models\model_glo.pkl"
        model = hmm_seq_glo.load_model(path)
        # synthesize learning paths
        synthetic_lps = hmm_seq_glo.sample_learning_paths(model, 30)
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
        synthetic_lps = hmm_seq_glo.synthesize_data("Sequential", 10)
        # check for amount of learning paths
        self.assertEqual(len(synthetic_lps), 10)


if __name__ == "__main__":
    unittest.main()
