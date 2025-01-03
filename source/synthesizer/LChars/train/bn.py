import argparse as arg
import os
import sys

import pandas as pd
from pgmpy.readwrite import XMLBIFWriter

# Add the 'source' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
import source.synthesizer.LChars.config as config  # nopep8
import source.synthesizer.LChars.utils as utils  # nopep8


def load_data(path: str):
    """
    load the data
    """
    # load the data
    df_data = pd.read_csv(path)
    return df_data


def extract_lchars(df, columns):
    """
    extract the required chars
    """
    # extract the LChars coolumns
    df_data = df[columns]
    return df_data


def run_experiments(df, n_samples):
    """
    run the experiments
    """
    # empty list to log experiments
    experiments = []

    # root nodes for BN visualization
    root = config.personalities_variables[0]

    # call all the methods to compare
    structure_methods = config.structure_learning_algorithms
    parameter_methods = config.parameter_learning_algorithms

    # create BN run the experiment for each BN based on methods
    for structure_method in structure_methods:
        for parameter_method in parameter_methods:
            bn = utils.build_bn(
                edges_list=config.undirected_edges_psy_models,
                topology=structure_method,
                df=df,
            )
            if bn is not None:
                bn = utils.train_bn(df, bn, parameter_method)
                experiment_name = f"{structure_method}_{parameter_method}"

                # writing the trained BN to local
                XMLBIFWriter(bn).write_xmlbif(
                    filename=config.prefix_bn_models + str(experiment_name) + ".xml"
                )

                # writing the BN plots to local
                # utils.save_bn_to_file(
                #     bn_model=bn,
                #     root=root,
                #     filename=config.prefix_bn_plots + str(
                #         experiment_name) + ".png",
                # )

                # saving the sampled data to local folder
                bn.simulate(n_samples).to_csv(
                    config.prefix_sim_data + str(experiment_name) + ".csv"
                )
                scores_ = utils.evaluate_bn(bn, df)
                k2_score = scores_["k2_score"]
                bic_score = scores_["bic_score"]
                bdeu_score = scores_["bdeu_score"]
                likelihood_score = scores_["log_likelihood"]
                if parameter_method == "b_est_bdeu":
                    # Perform cross-validation and calculate the average score
                    cross_val_scores = utils.cross_validate_bn_best_bdeu(
                        bn, df, n_splits=10
                    )
                elif parameter_method == "b_est_k2":
                    # Perform cross-validation and calculate the average score
                    cross_val_scores = utils.cross_validate_bn_best_k2(
                        bn, df, n_splits=10
                    )
                elif parameter_method == "em":
                    # Perform cross-validation and calculate the average score
                    cross_val_scores = utils.cross_validate_bn_em(bn, df, n_splits=10)
                elif parameter_method == "mle":
                    # Perform cross-validation and calculate the average score
                    cross_val_scores = utils.cross_validate_bn_mle(bn, df, n_splits=10)
                try:
                    avg_cross_val_score = sum(
                        score for score in cross_val_scores if score is not None
                    ) / len([score for score in cross_val_scores if score is not None])
                except Exception as e:
                    print(f"Error with cross-validation, {e}")
                    avg_cross_val_score = None
                finally:
                    experiments.append(
                        {
                            "name": experiment_name,
                            "K2 Score": k2_score,
                            "BIC Score": bic_score,
                            "BDeu Score": bdeu_score,
                            "Log-Likelihood": likelihood_score,
                            "Average Cross-Validation Score": avg_cross_val_score,
                        }
                    )
    return experiments


def main(data_file_path, n_samples):
    """
    call the functions and workflow
    """
    # load the data
    df_data = load_data(data_file_path)
    # extract the required columns
    df_data = extract_lchars(
        df=df_data,
        columns=[
            "AR",
            "SI",
            "VV",
            "SG",
            "cs",
            "mcs",
            "smir",
            "smer",
            "bfio",
            "bfin",
            "bfie",
            "bfia",
            "bfic",
        ],
    )
    # run the experiments (train+write)
    exp_res = run_experiments(df=df_data, n_samples=n_samples)
    # generate reports
    utils.generate_html_report(exp_res)

    return exp_res


if __name__ == "__main__":
    parser = arg.ArgumentParser(
        description="Train and evaluate Bayesian Networks\
            with various configurations."
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default=os.path.join("data", "real", "LChars_FullManualImputed.csv"),
        help="Path to real data csv file.\
            Default: data/real/LChars_FullManualImputed.csv",
    )
    parser.add_argument(
        "--n_samples",
        type=int,
        default=1000,
        help="Number of samples to synthesize using Bayesian Network.\
            Default:1000",
    )
    args = parser.parse_args()
    main(data_file_path=args.data_path, n_samples=args.n_samples)
