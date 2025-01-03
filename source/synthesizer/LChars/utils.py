import matplotlib

# Use a non-interactive backend
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from pgmpy.estimators import (
    PC,
    BayesianEstimator,
    BDeuScore,
    BicScore,
    ExpectationMaximization,
    HillClimbSearch,
    K2Score,
    MaximumLikelihoodEstimator,
    MmhcEstimator,
    TreeSearch,
)
from pgmpy.factors.discrete import TabularCPD
from pgmpy.metrics import log_likelihood_score
from pgmpy.models import BayesianNetwork
from sklearn.model_selection import KFold

np.seterr(divide="ignore")

import os
import sys

# Add the 'source' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import source.synthesizer.LChars.config as config


def visualize_bn(
    bn_model,
    filename,
    root,
    with_labels=True,
    arrowsize=30,
    node_size=800,
    alpha=0.3,
    font_weight="bold",
):
    """
    Visualizes a Bayesian Network using a hierarchical layout.

    Parameters:
    bn_model (BayesianNetwork): The Bayesian Network model to visualize.
    root (str): The root node for the hierarchical layout.
    with_labels (bool): Whether to display labels on the nodes.
    arrowsize (int): Size of the arrows in the visualization.
    node_size (int): Size of the nodes in the visualization.
    alpha (float): Transparency level of the nodes and edges.
    font_weight (str): Font weight of the node labels.
    """
    G = nx.DiGraph()
    G.add_edges_from(bn_model.edges())
    for node in bn_model.nodes():
        if not G.has_node(node):
            G.add_node(node)
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    nx.draw(
        G,
        pos,
        with_labels=with_labels,
        arrows=True,
        node_size=node_size,
        alpha=alpha,
        font_weight=font_weight,
    )
    plt.savefig(filename)
    plt.close()


def save_bn_to_file(
    bn_model,
    root,
    filename,
    with_labels=True,
    arrowsize=30,
    node_size=800,
    alpha=0.3,
    font_weight="bold",
):
    """
    Saves the visualization of a Bayesian Network to a file.

    Parameters:
    bn_model (BayesianNetwork): The Bayesian Network model to visualize.
    root (str): The root node for the hierarchical layout.
    filename (str): The path and name of the file to save the image.
    with_labels (bool): Whether to display labels on the nodes.
    arrowsize (int): Size of the arrows in the visualization.
    node_size (int): Size of the nodes in the visualization.
    alpha (float): Transparency level of the nodes and edges.
    font_weight (str): Font weight of the node labels.
    """
    G = nx.DiGraph()
    G.add_edges_from(bn_model.edges())
    for node in bn_model.nodes():
        if not G.has_node(node):
            G.add_node(node)
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    plt.figure(figsize=(12, 12))
    nx.draw(
        G,
        pos,
        with_labels=with_labels,
        arrows=True,
        node_size=node_size,
        alpha=alpha,
        font_weight=font_weight,
    )
    plt.savefig(filename)
    plt.close()


def ensure_all_states(df, state_names):
    for node, states in state_names.items():
        unique_states = df[node].unique()
        missing_states = [state for state in states if state not in unique_states]
        for state in missing_states:
            if isinstance(states[0], int):
                pseudo_row = {node: state}
                for col in df.columns:
                    if col != node:
                        if (
                            pd.api.types.is_categorical_dtype(df[col])
                            or df[col].dtype == object
                        ):
                            pseudo_row[col] = df[col].mode()[0]
                        else:
                            pseudo_row[col] = df[col].mean()
            else:
                pseudo_row = {node: state}
                for col in df.columns:
                    if col != node:
                        pseudo_row[col] = df[col].mode()[0]
            pseudo_df = pd.DataFrame([pseudo_row])
            df = pd.concat([df, pseudo_df], ignore_index=True)
    return df


def build_bn(edges_list, df, topology="treesearch"):
    """
    Builds a Bayesian Network based on the specified topology.

    Parameters:
    - edges_list (list): List of edges for the Bayesian Network.
    - df (DataFrame): DataFrame containing the data.
    - topology (str): The structure learning method to use.
    Default is "treesearch".

    Returns:
    - BayesianNetwork: The built Bayesian Network or
    None if an error occurs.
    """
    try:
        if topology == "iceri":
            model = _build_bn_iceri(edges_list)
        elif topology == "treesearch":
            model = _build_bn_treesearch(df)
        elif topology == "pc":
            model = _build_bn_pc(df)
        elif topology == "hybrid":
            model = _build_bn_hybrid(df)
        elif topology == "knowledgehybrid":
            model = _build_bn_knowledgehybrid(edges_list, df)
        else:
            print("Error: Invalid topology for Bayesian Network")
            return None

        # Add CPDs for isolated nodes
        _add_isolated_nodes_cpds(model, df)

        return model
    except Exception as e:
        print(f"An error occurred in build_bn: {e}")
        return None


def _build_bn_iceri(edges_list):
    """
    Builds a Bayesian Network using the ICERI topology.
    """
    bn = BayesianNetwork()
    # TODO: Update the edges_list from iceri23
    edges_list_iceri = config.edges_iceri
    bn.add_edges_from(edges_list_iceri)
    return bn


def _build_bn_treesearch(df):
    """
    Builds a Bayesian Network using the TreeSearch topology.
    """
    est = TreeSearch(data=df)
    bn = est.estimate(estimator_type="chow-liu")
    return BayesianNetwork(bn.edges())


def _build_bn_pc(df):
    """
    Builds a Bayesian Network using the PC algorithm.
    """
    est = PC(data=df)
    bn = est.estimate(
        return_type="dag", independence_test="pearsonr", significance_level=0.1
    )
    return BayesianNetwork(bn.edges())


def _build_bn_hybrid(df):
    """
    Builds a Bayesian Network using the hybrid MMHC algorithm.
    """
    mmhc = MmhcEstimator(data=df)
    skeleton = mmhc.mmpc()
    hc = HillClimbSearch(data=df)
    bn = hc.estimate(
        tabu_length=10,
        white_list=skeleton.to_directed().edges(),
        scoring_method=BDeuScore(data=df),
    )
    return BayesianNetwork(bn.edges())


def _build_bn_knowledgehybrid(edges_list, df):
    """
    Builds a Bayesian Network using the knowledge hybrid method.
    """
    bn = BayesianNetwork()
    bn.add_edges_from(edges_list)
    bn_skeleton = bn.moralize()
    hc = HillClimbSearch(data=df)
    bn_final = hc.estimate(
        tabu_length=100,
        white_list=bn_skeleton.to_directed().edges(),
        scoring_method=K2Score(data=df, state_names=config.state_names_psy_models),
    )
    return BayesianNetwork(bn_final.edges())


def _add_isolated_nodes_cpds(model, df):
    """
    Adds CPDs for isolated nodes based on their marginal probabilities
    in the observed data.

    Parameters:
    - model (BayesianNetwork): The Bayesian Network model.
    - df (DataFrame): DataFrame containing the data.
    """
    all_nodes = set(df.columns)
    connected_nodes = set(model.nodes())
    isolated_nodes = all_nodes - connected_nodes

    for node in isolated_nodes:
        # Add isolated nodes to the model
        model.add_node(node)

    for node in isolated_nodes:
        # Calculate marginal probabilities
        value_counts = df[node].value_counts(normalize=True).sort_index()
        # Ensure values are a column vector
        values = value_counts.values.reshape(-1, 1)
        cpd = TabularCPD(variable=node, variable_card=len(value_counts), values=values)
        model.add_cpds(cpd)
        print(f"Added CPD for isolated node {node}: {values}")


def train_bn(data, model_bn, estimator):
    """
    Trains a Bayesian Network using the specified estimator.

    Parameters:
    - data (DataFrame): DataFrame containing the data.
    - model_bn (BayesianNetwork): The Bayesian Network to train.
    - estimator (str): The parameter learning method to use.

    Returns:
    - BayesianNetwork: The trained Bayesian Network or None if an error occurs.
    """
    try:
        if estimator == "em":
            model_bn.fit(data=data, estimator=ExpectationMaximization)
        elif estimator == "b_est_bdeu":
            model_bn.fit(
                data,
                estimator=BayesianEstimator,
                prior_type="BDeu",
                equivalent_sample_size=5,
            )
        elif estimator == "b_est_k2":
            model_bn.fit(data, estimator=BayesianEstimator, prior_type="K2")
        elif estimator == "mle":
            model_bn.fit(data=data, estimator=MaximumLikelihoodEstimator)
        else:
            print("Error: Invalid estimator for training")
            return None
        return model_bn
    except Exception as e:
        print(f"An error occurred during training: {e}")
        return None


def apply_smoothing(model, alpha=1):
    """
    Apply Laplace smoothing to the CPTs of the Bayesian Network.
    """
    smoothed_model = BayesianNetwork(model.edges())
    smoothed_model.add_nodes_from(model.nodes())

    for node in model.nodes():
        cpd = model.get_cpds(node)
        values = cpd.values

        # Debugging: Print shapes and node information
        print(f"Node: {node}")
        print(f"Original values shape: {values.shape}")
        print(f"Original values: {values}")

        # Calculate the smoothed values
        smoothed_values = (values + alpha) / (
            values.sum(axis=0) + alpha * values.shape[0]
        )

        # Ensure smoothed_values is in the correct format
        if smoothed_values.ndim == 1:
            smoothed_values = smoothed_values.reshape(1, -1)
        else:
            smoothed_values = np.atleast_2d(smoothed_values)

        # Debugging: Print shapes after smoothing
        print(f"Smoothed values shape: {smoothed_values.shape}")
        print(f"Smoothed values: {smoothed_values}")

        try:
            smoothed_cpd = TabularCPD(
                variable=node,
                variable_card=cpd.variable_card,
                values=smoothed_values.tolist(),
                evidence=cpd.variables[:0:-1],
                evidence_card=cpd.cardinality[1:],
            )
            smoothed_model.add_cpds(smoothed_cpd)
        except ValueError as e:
            print(f"Error adding CPD for node {node}: {e}")
            print(f"Node: {node}")
            print(f"Original values shape: {values.shape}")
            print(f"Original values: {values}")
            print(f"Smoothed values shape: {smoothed_values.shape}")
            print(f"Smoothed values: {smoothed_values}")

    return smoothed_model


def evaluate_bn(model, data):
    """
    K2, BIC, BDeu Scores are used to score the structure of the model.
    The log-likelihood measure can be used to check how well the
    specified model describes the data.
    """
    k2 = K2Score(data)
    bic = BicScore(data)
    bdeu = BDeuScore(data)
    scores = {
        "k2_score": None,
        "bic_score": None,
        "bdeu_score": None,
        "log_likelihood": None,
    }

    try:
        scores["k2_score"] = k2.score(model)
        print(f"K2 Score: {scores['k2_score']}")
    except Exception as e:
        print(f"Error calculating K2 score: {e}")

    try:
        scores["bic_score"] = bic.score(model)
        print(f"BIC Score: {scores['bic_score']}")
    except Exception as e:
        print(f"Error calculating BIC score: {e}")

    try:
        scores["bdeu_score"] = bdeu.score(model)
        print(f"BDeu Score: {scores['bdeu_score']}")
    except Exception as e:
        print(f"Error calculating BDeu score: {e}")

    try:
        log_likelihood = log_likelihood_score(model, data)
        # debug the node causing -inf value.
        if np.isneginf(log_likelihood):
            print(
                "Warning: Log-likelihood contains -inf values.\
                    Some probabilities may be zero."
            )
            # Additional logging to identify problematic nodes
            for node in model.nodes():
                try:
                    prob = model.predict(data[[node]])
                    # Proper check for zero probabilities
                    if (prob == 0).any().any():
                        print(f"Zero probability encountered in node: {node}")
                except Exception as e:
                    print(f"Error querying node {node}: {e}")
        scores["log_likelihood"] = log_likelihood
        print(f"Log-Likelihood: {scores['log_likelihood']}")
    except RuntimeWarning as rw:
        print(f"Runtime warning during log-likelihood calculation: {rw}")
    except Exception as e:
        print(f"Error calculating log-likelihood score: {e}")

    return scores


def cross_validate_bn_best_bdeu(model, data, n_splits=10):
    kf = KFold(n_splits=n_splits)
    cross_val_scores = []

    for train_index, test_index in kf.split(data):
        train_data, test_data = data.iloc[train_index], data.iloc[test_index]
        model_copy = model.copy()
        try:
            model_copy.fit(
                train_data,
                estimator=BayesianEstimator,
                prior_type="BDeu",
                equivalent_sample_size=5,
            )
            log_likelihood = log_likelihood_score(model_copy, test_data)
            cross_val_scores.append(log_likelihood)
        except Exception as e:
            print(f"Error scoring model in cross-validation: {e}")
            cross_val_scores.append(None)

    return cross_val_scores


def cross_validate_bn_best_k2(model, data, n_splits=10):
    kf = KFold(n_splits=n_splits)
    cross_val_scores = []

    for train_index, test_index in kf.split(data):
        train_data, test_data = data.iloc[train_index], data.iloc[test_index]
        model_copy = model.copy()
        try:
            model_copy.fit(train_data, estimator=BayesianEstimator, prior_type="K2")
            log_likelihood = log_likelihood_score(model_copy, test_data)
            cross_val_scores.append(log_likelihood)
        except Exception as e:
            print(f"Error scoring model in cross-validation: {e}")
            cross_val_scores.append(None)

    return cross_val_scores


def cross_validate_bn_em(model, data, n_splits=10):
    kf = KFold(n_splits=n_splits)
    cross_val_scores = []

    for train_index, test_index in kf.split(data):
        train_data, test_data = data.iloc[train_index], data.iloc[test_index]
        model_copy = model.copy()
        try:
            model_copy.fit(data=train_data, estimator=ExpectationMaximization)
            log_likelihood = log_likelihood_score(model_copy, test_data)
            cross_val_scores.append(log_likelihood)
        except Exception as e:
            print(f"Error scoring model in cross-validation: {e}")
            cross_val_scores.append(None)
    return cross_val_scores


def cross_validate_bn_mle(model, data, n_splits=10):
    kf = KFold(n_splits=n_splits)
    cross_val_scores = []

    for train_index, test_index in kf.split(data):
        train_data, test_data = data.iloc[train_index], data.iloc[test_index]
        model_copy = model.copy()
        try:
            model_copy.fit(data=train_data, estimator=MaximumLikelihoodEstimator)
            log_likelihood = log_likelihood_score(model_copy, test_data)
            cross_val_scores.append(log_likelihood)
        except Exception as e:
            print(f"Error scoring model in cross-validation: {e}")
            cross_val_scores.append(None)
    return cross_val_scores


def generate_html_report(experiments):
    html_content = (
        "<html><head><title>Bayesian Network Experiments Report</title></head><body>"
    )
    html_content += "<h1>Bayesian Network Experiments Report</h1>"
    html_content += "<table border='1'><tr><th>Experiment Name</th><th>K2 Score</th><th>BIC Score</th><th>BDeu Score</th><th>Log-Likelihood</th><th>Average Cross-Validation Score</th></tr>"

    for experiment in experiments:
        html_content += f"<tr><td>{experiment['name']}</td><td>{experiment['K2 Score']}</td><td>{experiment['BIC Score']}</td><td>{experiment['BDeu Score']}</td><td>{experiment['Log-Likelihood']}</td><td>{experiment['Average Cross-Validation Score']}</td></tr>"

    html_content += "</table></body></html>"

    with open(config.save_path_htmlreport + ".html", "w") as file:
        file.write(html_content)
        print("HTML report generated successfully.")
