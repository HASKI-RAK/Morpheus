import argparse
import unittest

from source.simulator.LPaths.utils import (
    convert_le_types,
    update_cat_probs,
    update_dist_infos,
)


class UnitTests(unittest.TestCase):

    def test_update_dist_infos(self):
        """
        test if command line argument about distribution is correctly
        transformed
        """
        args_dict = {
            "n_samples": 100,
            "output": "test_data.csv",
            "LE1_dist": "normal",
            "LE1_params": "5,2",
            "LE1_values": "LG,BO,MS,QU,EX,SU,AAM,TAM,VAM",
            "LE2_dist": "normal",
            "LE2_params": "5,2",
            "LE2_values": "LG,BO,MS,QU,EX,SU,AAM,TAM,VAM",
            "LE3_dist": "normal",
            "LE3_params": "5,2",
            "LE3_values": "LG,BO,MS,QU,EX,SU,AAM,TAM,VAM",
            "LE4_dist": "normal",
            "LE4_params": "5,2",
            "LE4_values": "LG,BO,MS,QU,EX,SU,AAM,TAM,VAM",
            "LE5_dist": "normal",
            "LE5_params": "5,2",
            "LE5_values": "LG,BO,MS,QU,EX,SU,AAM,TAM,VAM",
            "LE6_dist": "normal",
            "LE6_params": "5,2",
            "LE6_values": "LG,BO,MS,QU,EX,SU,AAM,TAM,VAM",
            "LE7_dist": "normal",
            "LE7_params": "5,2",
            "LE7_values": "LG,BO,MS,QU,EX,SU,AAM,TAM,VAM",
            "LE8_dist": "normal",
            "LE8_params": "5,2",
            "LE8_values": "LG,BO,MS,QU,EX,SU,AAM,TAM,VAM",
            "LE9_dist": "normal",
            "LE9_params": "5,2",
            "LE9_values": "LG,BO,MS,QU,EX,SU,AAM,TAM,VAM",
        }
        args = argparse.Namespace(**args_dict)
        test_dist_infos = {
            "LE1": ("normal", (5, 2), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            "LE2": ("normal", (5, 2), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            "LE3": ("normal", (5, 2), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            "LE4": ("normal", (5, 2), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            "LE5": ("normal", (5, 2), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            "LE6": ("normal", (5, 2), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            "LE7": ("normal", (5, 2), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            "LE8": ("normal", (5, 2), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            "LE9": ("normal", (5, 2), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
        }
        self.assertEqual(update_dist_infos(args), test_dist_infos)

    def test_update_cat_probs(self):
        """
        test if values for learning style probabilities are transformed
        correctly
        """
        args_dict = {
            "AR": [0.5, 0.5],
            "SI": [0.5, 0.5],
            "SG": [0.2, 0.8],
            "VV": [0.5, 0.5],
        }
        args = argparse.Namespace(**args_dict)
        self.assertEqual(update_cat_probs(args), args_dict)

    def test_convert_le_types(self):
        """
        test if learning element types are converted correctly from string
        to int
        """
        le_types_str = ["LG", "LG", "BO"]
        le_types_expected_int = [0, 0, 1]
        self.assertEqual(convert_le_types(le_types_str), le_types_expected_int)
