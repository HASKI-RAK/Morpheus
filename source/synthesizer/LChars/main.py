import argparse
import os

from pgmpy.readwrite import XMLBIFReader


def main(
    model_path=None,
    n_samples=1000,
    output_filename="synthesized_learning_characteristics_data.csv",
):
    """
    Load a Bayesian Network from a saved model, simulate data, and save it
    to a CSV file.

    Parameters:
    - model_path (str): Path to the saved BN model in XMLBIF format.
                        Defaults to
                        "source/synthesizer/LChars/savedmodels/26-09
                        -2024_iceri_b_est_k2.xml".
    - n_samples (int): Number of samples to generate. Defaults to 1000.
    - output_filename (str): Name of the output CSV file (without path).
                             Defaults to 'simulated_data.csv'.

    Returns:
    - str: Full path to the saved CSV file.
    """

    # Set default model_path if not provided
    if model_path is None:
        current_dir = os.path.dirname(__file__)
        print(current_dir)
        model_path = current_dir + (r"\savedmodels\26-09" r"-2024_iceri_b_est_k2.xml")
    # Define the output directory
    output_directory = os.path.join("data", "synthetic")
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Full path to the output file
    output_path = os.path.join(output_directory, output_filename)

    # Check if the model file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    # Load the Bayesian Network model
    try:
        bn = XMLBIFReader(model_path).get_model()
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")

    # Simulate data
    try:
        df = bn.simulate(n_samples=n_samples)
    except Exception as e:
        raise RuntimeError(f"Error simulating data: {e}")

    # Save the simulated data to CSV
    try:
        df.to_csv(path_or_buf=output_path, index=False)
        print(f"Simulated data saved to {output_filename}")
    except Exception as e:
        raise RuntimeError(f"Error saving data to CSV: {e}")

    return df


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Load a Bayesian Network from a saved model and "
        "synthesize data with a given sample size."
    )
    parser.add_argument(
        "--model_path",
        type=str,
        default=os.path.join(
            os.path.dirname(__file__), "savedmodels", "26-09-2024_iceri_b_est_k2.xml"
        ),
        help="Path to the saved BN model in XMLBIF format.",
    )
    parser.add_argument(
        "--n_samples", type=int, default=1000, help="Number of samples to generate."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="synthesized_learner_characteristics.csv",
        help="Name of the output CSV file (without path). The file will be "
        "saved in data/synthetic/.",
    )

    args = parser.parse_args()

    try:
        main(
            model_path=args.model_path,
            n_samples=args.n_samples,
            output_filename=args.output,
        )
    except Exception as e:
        print(f"Error: {e}")
