import os
import unittest

import source.simulator.LChars.generator as lchars_generator
import source.simulator.LChars.main as lchars_main
from source.simulator.LChars.config import Config


class UnitTests(unittest.TestCase):

    # check brief working of main script
    def test_mainscript(self):
        """
        Targets to check if main scripts returns the value as expected
        """
        test_string = "test_data"
        expected_name = lchars_main.main(output_file=test_string)
        actual_name = test_string
        self.assertEqual(expected_name, actual_name)

    # test if all desired experiements are run and logged
    # def test_run_experiments(self):
    #     '''
    #     Goal of this unit test
    #     '''
    #     self.assertEqual(actual_exps[0].keys(), expected_exps)

    # test alpha
    def test_alpha(self):
        test_val = 1.0
        with self.assertRaises(RuntimeError):
            lchars_main.main(alpha=test_val)

    def test_config_simulation(self):
        test_path = os.path.join("..", "source", "simulator", "LChars", "config")
        with self.assertRaises(FileNotFoundError):
            lchars_main.main(num_dist_info=test_path)
        with self.assertRaises(FileNotFoundError):
            lchars_main.main(cat_dist_probs=test_path)

    def test_alpha_with_reference(self):
        test_val = 1.0
        test_path = os.path.join("..", "data", "real", "tests_sampleLChars.csv")
        df_ = lchars_main.main(alpha=test_val, reference_file=test_path)
        self.assertEqual("simulated_learning_characteristics_data", df_)


if __name__ == "__main__":
    unittest.main()
