# data_generator.py
import random

import numpy as np
import pandas as pd

from source.simulator.LPaths.utils import convert_le_types


def map_to_closest(value, valid_values):
    """Map a value to the nearest value in a set of valid values."""
    valid_values_str = False
    for z in valid_values:
        if type(z) is str:
            valid_values_str = True

    if valid_values_str:
        # convert string elements to int values for comparison
        valid_values = convert_le_types(valid_values)
    valid_values = np.array(valid_values)
    index = np.argmin(np.abs(valid_values - value))
    return valid_values[index]


def generate_numerical_data(dist_type, params, size, possible_values):
    possible_values = sorted(possible_values)
    if dist_type == "uniform":
        return np.random.choice(possible_values, size=size)
    elif dist_type == "normal":
        mu, sigma = params
        generated = np.random.normal(mu, sigma, size)
        return np.array([map_to_closest(val, possible_values) for val in generated])
    elif dist_type == "binomial":
        n, p = params
        generated = np.random.binomial(n, p, size)
        return np.array([map_to_closest(val, possible_values) for val in generated])
    elif dist_type == "weibull":
        a, scale = params
        generated = scale * np.random.weibull(a, size)
        return np.array([map_to_closest(val, possible_values) for val in generated])
    else:
        # Default to uniform distribution if unknown distribution type
        return np.random.choice(possible_values, size=size)


def generate_learning_styles(num_students, cat_dist_probs):
    data = {}
    # Generate data for categorical attributes
    for column, probs in cat_dist_probs.items():
        if "AR" in column:
            categories = ["Active", "Reflective"]
            num_a = int(num_students * probs[0])
            num_b = num_students - num_a
            lst = [categories[0]] * num_a + [categories[1]] * num_b
        elif "SI" in column:
            categories = ["Sensory", "Intuitive"]
            num_a = int(num_students * probs[0])
            num_b = num_students - num_a
            lst = [categories[0]] * num_a + [categories[1]] * num_b
        elif "VV" in column:
            categories = ["Visual", "Verbal"]
            num_a = int(num_students * probs[0])
            num_b = num_students - num_a
            lst = [categories[0]] * num_a + [categories[1]] * num_b
        elif "SG" in column:
            categories = ["Sequential", "Global"]
            num_a = int(num_students * probs[0])
            num_b = num_students - num_a
            lst = [categories[0]] * num_a + [categories[1]] * num_b
        else:
            categories = []
            lst = categories
        random.shuffle(lst)
        data[column] = np.array(lst)
    return data


def generate_learning_paths(num_students, num_dist_info):
    data = {}
    for i in range(1, len(list(num_dist_info.keys())) + 1):
        column = f"LE{i}"
        dist_type, params, possible_values = num_dist_info[column]
        data[column] = generate_numerical_data(
            dist_type, params, num_students, possible_values
        )
    return data


def generate_student_data(num_students, num_dist_info, cat_dist_probs):
    learning_styles = generate_learning_styles(num_students, cat_dist_probs)
    learning_paths = generate_learning_paths(num_students, num_dist_info)

    data = {**learning_styles, **learning_paths}
    return pd.DataFrame(data)
