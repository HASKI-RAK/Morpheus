# config.py
import os
import time

file = time.strftime("%d-%m-%Y")
dir_name = os.path.dirname(__file__)
root_dir = dir_name.replace(r"\source\synthesizer\LChars", "")

save_path_htmlreport = os.path.join(dir_name, "plots", file + "_")
# save_path_htmlreport = os.path.join(
#     "source", "synthesizer", "LChars", "plots", file + "_"
# )
prefix_sim_data = os.path.join(root_dir, "data", "synthetic", file + "_")
# prefix_sim_data = os.path.join(
#     "data", "synthetic", file + "_"
#     )
prefix_bn_plots = os.path.join(dir_name, "plots", file + "_")
# prefix_bn_plots = os.path.join(
#     "source", "synthesizer", "LChars", "plots", file + "_"
#     )
prefix_bn_models = os.path.join(dir_name, "savedmodels", file + "_")
# prefix_bn_models = os.path.join(
#     "source", "synthesizer", "LChars", "savedmodels", file + "_"
# )
structure_learning_algorithms = ["pc"]  # use for testing the workflow
# structure_learning_algorithms = [
#     "iceri", "treesearch", "pc",
#     "hybrid", "knowledgehybrid"
#     ]
parameter_learning_algorithms = ["em", "mle"]  # use for testing the workflow
# parameter_learning_algorithms = [
#     "em", "b_est_bdeu",
#     "b_est_k2", "mle"
#     ]

undirected_edges_psy_models = [
    ("AR", "bfio"),
    ("AR", "bfia"),
    ("AR", "bfic"),
    ("AR", "bfie"),
    ("AR", "bfin"),
    ("SI", "bfio"),
    ("SI", "bfia"),
    ("SI", "bfic"),
    ("SI", "bfie"),
    ("SI", "bfin"),
    ("VV", "bfio"),
    ("VV", "bfia"),
    ("VV", "bfic"),
    ("VV", "bfie"),
    ("VV", "bfin"),
    ("SG", "bfio"),
    ("SG", "bfia"),
    ("SG", "bfic"),
    ("SG", "bfie"),
    ("SG", "bfin"),
    ("AR", "cs"),
    ("AR", "mcs"),
    ("AR", "smer"),
    ("AR", "smir"),
    ("SI", "cs"),
    ("SI", "mcs"),
    ("SI", "smer"),
    ("SI", "smir"),
    ("VV", "cs"),
    ("VV", "mcs"),
    ("VV", "smer"),
    ("VV", "smir"),
    ("SG", "cs"),
    ("SG", "mcs"),
    ("SG", "smer"),
    ("SG", "smir"),
    ("bfio", "cs"),
    ("bfio", "mcs"),
    ("bfio", "smer"),
    ("bfio", "smir"),
    ("bfia", "cs"),
    ("bfia", "mcs"),
    ("bfia", "smer"),
    ("bfia", "smir"),
    ("bfic", "cs"),
    ("bfic", "mcs"),
    ("bfic", "smer"),
    ("bfic", "smir"),
    ("bfie", "cs"),
    ("bfie", "mcs"),
    ("bfie", "smer"),
    ("bfie", "smir"),
    ("bfin", "cs"),
    ("bfin", "mcs"),
    ("bfin", "smer"),
    ("bfin", "smir"),
]

edges_iceri = [
    ("AR", "bfio"),
    ("AR", "bfie"),
    ("AR", "cs"),
    ("AR", "smer"),
    ("VV", "bfin"),
    ("SG", "mcs"),
    ("SI", "bfio"),
    ("SI", "cs"),
    ("bfio", "smer"),
    ("bfia", "smer"),
    ("bfic", "cs"),
    ("bfic", "smir"),
    ("bfie", "bfin"),
    ("bfie", "smer"),
    ("bfin", "cs"),
    ("cs", "mcs"),
    ("bfic", "smer"),
    ("bfie", "smer"),
    ("bfic", "smir"),
    ("smir", "smer"),
]

state_names_psy_models = {
    "AR": ["Active", "Reflective"],
    "SI": ["Sensory", "Intuitive"],
    "VV": ["Visual", "Verbal"],
    "SG": ["Sequential", "Global"],
    "cs": [1, 2, 3, 4, 5],
    "mcs": [1, 2, 3, 4, 5],
    "smir": [1, 2, 3, 4, 5],
    "smer": [1, 2, 3, 4, 5],
    "bfie": [1, 2, 3, 4, 5],
    "bfin": [1, 2, 3, 4, 5],
    "bfio": [1, 2, 3, 4, 5],
    "bfic": [1, 2, 3, 4, 5],
    "bfia": [1, 2, 3, 4, 5],
}

personalities_variables = ["bfie", "bfin", "bfio", "bfic", "bfia"]
