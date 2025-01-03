def update_dist_infos(args):
    """
    update information about numerical distributions
    :param args: command line input arguments
    :return: updated information about numerical distributions
    """
    # Update the distribution info based on command-line arguments
    num_dist_info_updated = {}
    for i in range(1, 10):
        dist_type = getattr(args, f"LE{i}_dist")
        params_str = getattr(args, f"LE{i}_params")
        if params_str:
            params = tuple(map(float, params_str.split(",")))
        else:
            params = ()
        possible_values = convert_le_types(getattr(args, f"LE{i}_values").split(","))
        num_dist_info_updated[f"LE{i}"] = (dist_type, params, possible_values)
    return num_dist_info_updated


def update_cat_probs(args):
    """
    store learning style probabilities correctly and return as a variable
    :param args: command line input arguments
    :return: updated information about learning style distributions
    """
    cat_dist_probs_updated = {}
    cat_dist_probs_updated["AR"] = args.AR
    cat_dist_probs_updated["SI"] = args.SI
    cat_dist_probs_updated["SG"] = args.SG
    cat_dist_probs_updated["VV"] = args.VV
    return cat_dist_probs_updated


def convert_le_types(le_types_str):
    """
    convert learning element types from string to int
    :param le_types_str: learning element types list as string
    :return: learning element types converted to ints
    """
    conversion_map = {
        "LG": 0,
        "BO": 1,
        "MS": 2,
        "QU": 3,
        "EX": 4,
        "SU": 5,
        "AAM": 6,
        "TAM": 7,
        "VAM": 8,
    }
    le_types_int = []
    for z in le_types_str:
        le_types_int.append(conversion_map[z])
    return le_types_int
