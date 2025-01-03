# main.py
import argparse

from .config import (
    ACT_REF_DEFAULT,
    MODELS,
    SEN_INT_DEFAULT,
    SEQ_GLO_DEFAULT,
    VIS_VER_DEFAULT,
)
from .synthesizer import synthesize_learning_paths
from .utils import store_data_in_csv


def main(
    act_ref=ACT_REF_DEFAULT,
    sen_int=SEN_INT_DEFAULT,
    seq_glo=SEQ_GLO_DEFAULT,
    vis_ver=VIS_VER_DEFAULT,
    amount=100,
    output="synthesized_learning_path_data",
):
    """
    :param act_ref: active or reflective learning style
    :param sen_int: sensory or intuitive learning style
    :param seq_glo: sequential or global learning style
    :param vis_ver: visual or verbal learning style
    :param amount: amount of entries in the data set
    :param output: output file name
    """
    # Generate data
    data_dict = synthesize_learning_paths(
        act_ref, sen_int, seq_glo, vis_ver, amount, output, MODELS
    )
    # Save the data to CSV
    store_data_in_csv(data_dict, output)
    print(f"Data generated and saved to {output}.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthesize student "
                                                 "learning data.")
    parser.add_argument(
        "--act_ref", type=str, default="Active", help="Active or Reflective"
    )
    parser.add_argument(
        "--sen_int", type=str, default="Sensory", help="Sensory or Intuitive"
    )
    parser.add_argument(
        "--seq_glo", type=str, default="Sequential", help="Sequential or "
                                                          "Global"
    )
    parser.add_argument(
        "--vis_ver", type=str, default="Visual", help="Visual or Verbal"
    )
    parser.add_argument(
        "--amount", type=int, default=100, help="Number of students to "
                                                "generate."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="synthesized_learning_path_data",
        help="Output CSV file name.",
    )
    args = parser.parse_args()
    main(
        args.act_ref, args.sen_int, args.seq_glo, args.vis_ver, args.amount,
        args.output
    )
