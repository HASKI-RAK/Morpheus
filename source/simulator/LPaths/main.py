import argparse
import os

from source.simulator.LPaths.config import FILE_NAME_SIM_LPATHS, N_SAMPLES
from source.simulator.LPaths.config import cat_dist_probs as default_cat_dist_probs
from source.simulator.LPaths.config import num_dist_info as default_num_dist_info
from source.simulator.LPaths.generator import generate_student_data
from source.simulator.LPaths.utils import update_cat_probs, update_dist_infos


def create_command_line_args():
    """
    provide user with command line options when simulating learning path
    data
    """
    parser = argparse.ArgumentParser(description="Generate student learning data.")
    parser.add_argument(
        "--n_samples", type=int, default=100, help="Number of students to generate."
    )
    parser.add_argument(
        "--output", type=str, default="generated_data.csv", help="Output CSV file name."
    )

    # command line arguments for learning element distribution
    for i in range(1, 10):
        parser.add_argument(
            f"--LE{i}_dist",
            type=str,
            default=default_num_dist_info[f"LE{i}"][0],
            help=f"Distribution type for LE{i}. Options: "
            f"uniform, normal, binomial, weibull.",
        )
        params_default = ",".join(map(str, default_num_dist_info[f"LE{i}"][1]))
        parser.add_argument(
            f"--LE{i}_params",
            type=str,
            default=params_default,
            help=f"Parameters for LE{i} distribution. " f"Example for normal: '5,2'.",
        )
        values_default = ",".join(map(str, default_num_dist_info[f"LE{i}"][2]))
        parser.add_argument(
            f"--LE{i}_values",
            type=str,
            default=values_default,
            help=f"Possible values for LE{i}. Example: '0,1," f"2,3'.",
        )

    # command line arguments for learning style distribution
    cat_probs_default = [0.5, 0.5]
    parser.add_argument(f"--AR", type=str, default=cat_probs_default)
    parser.add_argument(f"--SI", type=str, default=cat_probs_default)
    parser.add_argument(f"--SG", type=str, default=cat_probs_default)
    parser.add_argument(f"--VV", type=str, default=cat_probs_default)
    return parser.parse_args()


def main(
    n_samples=N_SAMPLES,
    file_name=FILE_NAME_SIM_LPATHS,
    num_dist_info=None,
    cat_dist_probs=None,
):
    """
    generate learning path data with given distributions
    :param n_samples: amount of data entries to generate
    :param file_name: name of the generated file
    :param num_dist_info: info about distribution of learning path data
    :param cat_dist_probs: info about distribution of learning styles data
    :return:
    """
    # use default settings if there is no information given
    if num_dist_info is None:
        num_dist_info = default_num_dist_info
    if cat_dist_probs is None:
        cat_dist_probs = default_cat_dist_probs

    # Generate data
    df_gen = generate_student_data(n_samples, num_dist_info, cat_dist_probs)

    current_path = os.path.dirname(os.path.abspath(__file__))
    storage_path = current_path.replace(
        r"source\simulator\LPaths", r"data\simulated\{}.csv".format(file_name)
    )

    # Save the data to CSV
    df_gen.to_csv(storage_path, index=False)
    print(f"Data generated and saved to {file_name}.csv")


if __name__ == "__main__":
    args = create_command_line_args()
    num_dist_info_updated = update_dist_infos(args)
    cat_dist_probs_updated = update_cat_probs(args)
    main(args.n_samples, args.output, num_dist_info_updated, cat_dist_probs_updated)
