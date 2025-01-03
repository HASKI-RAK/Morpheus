# simulated_lchars_main.py

import argparse
import json
import os

import pandas as pd

from source.simulator.LChars.config import Config
from source.simulator.LChars.generator import DataGenerator
from source.simulator.LChars.utils import decode_categorical, encode_categorical


def main(
    num_students=100,
    alpha=0.0,
    reference_file="",
    output_file="simulated_learning_characteristics_data",
    num_dist_info="",
    cat_dist_probs="",
):
    """
    Generate synthetic student data based on specified parameters and save
    it to a CSV file.

    Parameters:
    - num_students (int): Number of students to generate. Defaults to 100.
    - alpha (float): Alpha value for Euclidean distance from reference
    dataset. Defaults to 0.0.
    - reference_file (str): Path to reference dataset CSV file. Required if
    alpha > 0.
                              Defaults to an empty string.
    - output_file (str): File name to save generated data. Defaults to
    'generated_data.csv'.
    - num_dist_info (str): File path to JSON file containing numerical
    distributions info.
                            Defaults to an empty string.
    - cat_dist_probs (str): File path to JSON file containing categorical
    distributions probabilities.
                             Defaults to an empty string.

    Returns:
    - str: Path to the saved generated data CSV file.

    Raises:
    - FileNotFoundError: If required files are not found.
    - ValueError: If alpha > 0 but reference_file is not provided.
    - RuntimeError: If data generation fails.
    """
    config = Config()

    # If num_dist_info is specified, load it
    if num_dist_info:
        if not os.path.exists(num_dist_info):
            raise FileNotFoundError(
                f"Numerical distribution info file not found at " f"{num_dist_info}"
            )
        with open(num_dist_info, "r") as f:
            config.num_dist_info = json.load(f)

    # If cat_dist_probs is specified, load it
    if cat_dist_probs:
        if not os.path.exists(cat_dist_probs):
            raise FileNotFoundError(
                f"Categorical distribution probabilities file not found at "
                f"{cat_dist_probs}"
            )
        with open(cat_dist_probs, "r") as f:
            config.cat_dist_probs = json.load(f)

    data_generator = DataGenerator(config)

    try:
        if alpha > 0:
            if not reference_file:
                raise ValueError("Reference file must be specified when alpha > 0")

            if not os.path.exists(reference_file):
                raise FileNotFoundError(f"Reference file not found at {reference_file}")

            reference_df = pd.read_csv(reference_file)
            reference_df_encoded, ohe = encode_categorical(reference_df)
            new_data_encoded = data_generator.generate_data_with_alpha(
                reference_df_encoded, alpha, num_students
            )
            new_data = decode_categorical(new_data_encoded, ohe, reference_df)
        else:
            # Use default or loaded configurations
            new_data = data_generator.generate_student_data(num_students)

        current_path = os.path.dirname(os.path.abspath(__file__))
        storage_path = current_path.replace(
            r"source\simulator\LChars", r"data\simulated\{}.csv".format(output_file)
        )

        new_data.to_csv(storage_path, index=False)
        print(f"Data generated and saved to {output_file}.csv")
        return output_file

    except Exception as e:
        raise RuntimeError(f"Failed to generate data: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Data Generator Command Line Interface"
    )

    parser.add_argument(
        "--num_students", type=int, default=100, help="Number of students to generate"
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.0,
        help="Alpha value for Euclidean distance from " "reference dataset",
    )
    parser.add_argument(
        "--reference_file",
        type=str,
        default="",
        help="Path to reference dataset CSV file",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="generated_data.csv",
        help="File name to save generated data",
    )
    parser.add_argument(
        "--num_dist_info",
        type=str,
        default="",
        help="File path to JSON file containing numerical " "distributions info",
    )
    parser.add_argument(
        "--cat_dist_probs",
        type=str,
        default="",
        help="File path to JSON file containing categorical "
        "distributions probabilities",
    )

    args = parser.parse_args()

    try:
        main(
            num_students=args.num_students,
            alpha=args.alpha,
            reference_file=args.reference_file,
            output_file=args.output_file,
            num_dist_info=args.num_dist_info,
            cat_dist_probs=args.cat_dist_probs,
        )
    except Exception as e:
        print(f"Error: {e}")
