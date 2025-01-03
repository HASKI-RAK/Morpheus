import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pgmpy.readwrite import XMLBIFReader

import source.synthesizer.LChars.train.bn as train_bn
from source.synthesizer.LChars import main as main_bn


class UnitTests(unittest.TestCase):

    def test_mainscript(self):
        """
        Targets to check if loading the BN from a XML file,
        generating synthetic data and saving it locally works or not
        """
        # test for output file name and path
        # out = bn_main.main(output_filename="testing.csv")
        # exp_path = os.path.join('data', 'synthetic', "testing.csv")
        # self.assertEqual(out, exp_path)

        # test for default model path
        bn_path = os.path.join(
            "..",
            "source",
            "synthesizer",
            "LChars",
            "savedmodels",
            "26-09-2024_iceri_b_est_k2.xml",
        )
        act_df = main_bn.main(bn_path)

        bn = XMLBIFReader(bn_path).get_model()
        exp_df = bn.simulate(1000)
        self.assertEqual(act_df.shape[0], exp_df.shape[0])

    # test if all desired experiements are run and logged
    def test_run_experiments(self):

        test_path = os.path.join("..", "data", "real", "tests_sampleLChars.csv")
        actual_exps = train_bn.main(data_file_path=test_path, n_samples=10)
        print(actual_exps)
        expected_exps = {
            "name",
            "K2 Score",
            "BIC Score",
            "BDeu Score",
            "Log-Likelihood",
            "Average Cross-Validation Score",
        }
        self.assertEqual(actual_exps[0].keys(), expected_exps)

    def test_main_with_default_path(self):
        """
        this functions aims to test if the BN works when no reference path
        is given to load the model or not
        AND
        test the exception if the model path doesnot exist
        """
        bn_path = os.path.join(
            "..",
            "source",
            "synthesizer",
            "LChars",
            "savedmodels",
            "26-09-2024_iceri_b_est_k2.xml",
        )
        # test if the default model is correctly loaded
        act_df = main_bn.main(model_path=None)
        bn = XMLBIFReader(bn_path).get_model()
        exp_df = bn.simulate(1000)
        self.assertEqual(act_df.shape[0], exp_df.shape[0])

        dummy_model_path = "dummy/blabla.xml"
        # test if model path does not exist
        with self.assertRaises(FileNotFoundError):
            main_bn.main(model_path=dummy_model_path)
        # # test the errors for loading the BN
        # dir_name = os.path.dirname(__file__)
        # test_save_path = "blabla"
        # with self.assertRaises(RuntimeError):
        #     main_bn.main(output_filename=dir_name+test_save_path)


if __name__ == "__main__":
    unittest.main()
