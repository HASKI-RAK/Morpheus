import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


class DataGenerator:
    def __init__(self, config, random_seed=42):
        self.config = config
        self.random_seed = random_seed
        np.random.seed(self.random_seed)  # Set the random seed

    def generate_data_with_alpha(self, reference_df, alpha, num_students):
        # Standardize the reference data
        scaler = StandardScaler()
        reference_df_scaled = scaler.fit_transform(reference_df)

        # Calculate the centroid of the reference dataset
        ref_centroid = reference_df_scaled.mean(axis=0)

        # Generate a random direction vector
        direction_vector = np.random.normal(size=reference_df_scaled.shape[1])
        # Normalize the direction vector
        direction_vector = direction_vector / np.linalg.norm(direction_vector)

        # Calculate the new centroid
        new_centroid = ref_centroid + alpha * direction_vector

        # Generate new data around the new centroid
        new_data = np.random.normal(
            loc=new_centroid,
            scale=reference_df_scaled.std(axis=0),
            size=(num_students, reference_df_scaled.shape[1]),
        )

        # Inverse transform to original scale
        new_data_df = pd.DataFrame(
            scaler.inverse_transform(new_data), columns=reference_df.columns
        )
        return new_data_df

    def map_to_closest(self, value, valid_values):
        """Map a value to the nearest value in a set of valid values."""
        return valid_values[np.argmin(np.abs(np.array(valid_values) - value))]

    def generate_numerical_data(self, dist_type, params, size, possible_values):
        if dist_type == "uniform":
            return np.random.choice(possible_values, size=size)
        elif dist_type == "normal":
            mu, sigma = params
            generated = np.random.normal(mu, sigma, size)
            return np.array(
                [self.map_to_closest(val, possible_values) for val in generated]
            )
        elif dist_type == "binomial":
            n, p = params
            generated = np.random.binomial(n, p, size)
            return np.array(
                [self.map_to_closest(val, possible_values) for val in generated]
            )
        elif dist_type == "weibull":
            a, scale = params
            generated = scale * np.random.weibull(a, size)
            return np.array(
                [self.map_to_closest(val, possible_values) for val in generated]
            )
        else:
            return np.random.choice(possible_values, size=size)

    def generate_student_data(self, num_students):
        data = {}
        # Generate data for categorical attributes
        for column, probs in self.config.cat_dist_probs.items():
            categories = (
                ["Active", "Reflective"]
                if "AR" in column
                else (
                    ["Sensory", "Intuitive"]
                    if "SI" in column
                    else (
                        ["Visual", "Verbal"]
                        if "VV" in column
                        else ["Sequential", "Global"]
                    )
                )
            )
            data[column] = np.random.choice(categories, num_students, p=probs)

        # Generate data for numerical attributes
        for column, dist_info in self.config.num_dist_info.items():
            dist_type = dist_info["dist_type"]
            params = dist_info["params"]
            possible_values = dist_info["possible_values"]
            data[column] = self.generate_numerical_data(
                dist_type, params, num_students, possible_values
            )

        return pd.DataFrame(data)
