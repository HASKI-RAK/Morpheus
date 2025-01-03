from source.synthesizer.LPaths.hmm import (
    hmm_act_ref,
    hmm_sen_int,
    hmm_seq_glo,
    hmm_vis_ver,
)
from source.synthesizer.LPaths.mc import mc_act_ref, mc_sen_int, mc_seq_glo, mc_vis_ver  # nopep8


def synthesize_learning_paths(
    ls_act_ref, ls_sen_int, ls_seq_glo, ls_vis_ver, amount, file_name, models
):
    """
    synthesize specified amount of learning styles for given learning
    styles
    :param ls_act_ref: Active or Reflective
    :param ls_sen_int: Sensory or Intuitive
    :param ls_seq_glo: Sequential or Global
    :param ls_vis_ver: Visual or Verbal
    :param amount: synthetic data size
    :param file_name: name of the csv file
    :param models: info about configuration: use MCs or HMMs
    :return: dict with synthetic learning path data
    """
    data_dict = {}
    if models == "Markov Chain":
        # use markov chains to synthesize learning path data
        if ls_act_ref == "Active":
            data_dict["Active"] = mc_act_ref.synthesize_data("Active", amount)
        else:
            data_dict["Reflective"] = mc_act_ref.synthesize_data("Reflective",
                                                                 amount)
        if ls_sen_int == "Sensory":
            data_dict["Sensory"] = mc_sen_int.synthesize_data("Sensory",
                                                              amount)
        else:
            data_dict["Intuitive"] = mc_sen_int.synthesize_data("Intuitive",
                                                                amount)
        if ls_seq_glo == "Sequential":
            data_dict["Sequential"] = mc_seq_glo.synthesize_data("Sequential",
                                                                 amount)
        else:
            data_dict["Global"] = mc_seq_glo.synthesize_data("Global", amount)
        if ls_vis_ver == "Visual":
            data_dict["Visual"] = mc_vis_ver.synthesize_data("Visual", amount)
        else:
            data_dict["Verbal"] = mc_vis_ver.synthesize_data("Verbal", amount)
    else:
        # use hidden markov models to synthesize learning path data
        if ls_act_ref == "Active":
            data_dict["Active"] = hmm_act_ref.synthesize_data("Active", amount)
        else:
            data_dict["Reflective"] = hmm_act_ref.synthesize_data("Reflective",
                                                                  amount)
        if ls_sen_int == "Sensory":
            data_dict["Sensory"] = hmm_sen_int.synthesize_data("Sensory",
                                                               amount)
        else:
            data_dict["Intuitive"] = hmm_sen_int.synthesize_data("Intuitive",
                                                                 amount)
        if ls_seq_glo == "Sequential":
            data_dict["Sequential"] = hmm_seq_glo.synthesize_data("Sequential",
                                                                  amount)
        else:
            data_dict["Global"] = hmm_seq_glo.synthesize_data("Global", amount)
        if ls_vis_ver == "Visual":
            data_dict["Visual"] = hmm_vis_ver.synthesize_data("Visual", amount)
        else:
            data_dict["Verbal"] = hmm_vis_ver.synthesize_data("Verbal", amount)
    return data_dict
