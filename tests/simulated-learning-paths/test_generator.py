import unittest

import pandas as pd

from source.simulator.LPaths.generator import (
    generate_learning_paths,
    generate_learning_styles,
    generate_numerical_data,
    map_to_closest,
)


class UnitTests(unittest.TestCase):

    def test_generate_numerical_data_uniform(self):
        """
        test if uniformly distributed numerical data is correctly generated
        """
        # get path to test learning path data
        test_data = generate_numerical_data(
            "uniform", (2, 5), 10, [0, 1, 2, 3, 4, 5, 6, 7, 8]
        )
        test_data_list = [int(z) for z in list(test_data)]
        self.assertEqual(len(test_data_list), 10)

    def test_generate_numerical_data_normal(self):
        """
        test if normally distributed numerical data is correctly generated
        """
        # get path to test learning path data
        test_data = generate_numerical_data(
            "normal", (2, 5), 10, [0, 1, 2, 3, 4, 5, 6, 7, 8]
        )
        test_data_list = [int(z) for z in list(test_data)]
        self.assertEqual(len(test_data_list), 10)

    def test_generate_numerical_data_binomial(self):
        """
        test if binomially distributed numerical data is correctly generated
        """
        # get path to test learning path data
        test_data = generate_numerical_data(
            "binomial", (10, 0.5), 10, [0, 1, 2, 3, 4, 5, 6, 7, 8]
        )
        test_data_list = [int(z) for z in list(test_data)]
        self.assertEqual(len(test_data_list), 10)

    def test_generate_numerical_data_weibull(self):
        """
        test if weibull-like distributed numerical data is correctly generated
        """
        # get path to test learning path data
        test_data = generate_numerical_data(
            "weibull", (2, 51), 10, [0, 1, 2, 3, 4, 5, 6, 7, 8]
        )
        test_data_list = [int(z) for z in list(test_data)]
        self.assertEqual(len(test_data_list), 10)

    def test_generate_learning_styles(self):
        """
        test if learning styles are generated correctly in accordance to
        given probabilities
        """
        cat_dist_probs = {
            "AR": [0.5, 0.5],
            "SI": [0.7, 0.3],
            "VV": [0.2, 0.8],
            "SG": [0.5, 0.5],
        }

        test_data = generate_learning_styles(10, cat_dist_probs)
        test_data_df = pd.DataFrame(test_data)
        test_data_df_vv = test_data_df["VV"]
        counts_verbal = int(test_data_df_vv.value_counts()["Verbal"])
        self.assertEqual(counts_verbal, 8)

    def test_map_to_closest(self):
        """
        test if correct index is returned
        """
        value = float(8.1)
        valid_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(int(map_to_closest(value, valid_values)), 8)

    def test_generate_learning_paths(self):
        """
        test if learning path data is generated correctly
        """
        num_dist_info = {"LE1": ("normal", (5, 2), [0, 1, 2, 3, 4])}
        learning_path_data = generate_learning_paths(10, num_dist_info)
        learning_paths = learning_path_data["LE1"]
        self.assertEqual(len(learning_paths), 10)


if __name__ == "__main__":
    unittest.main()
