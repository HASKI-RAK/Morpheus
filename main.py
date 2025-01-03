import os

import source.simulator.LChars.main as simulate_lchars
import source.simulator.LPaths.main as simulate_lpaths
import source.synthesizer.LChars.main as synthesize_lchars
import source.synthesizer.LPaths.main as synthesize_lpaths
from utils.config import (
    BN_MODEL_NAME,
    FILE_NAME_SIM_LCHARS,
    FILE_NAME_SIM_LPATHS,
    FILE_NAME_SYN_LCHARS,
    FILE_NAME_SYN_LPATHS,
    MODE,
    N_SAMPLES,
)

if __name__ == "__main__":
    if MODE == "Simulation":
        # simulate data
        simulate_lpaths.main(N_SAMPLES, FILE_NAME_SIM_LPATHS, None, None)
        simulate_lchars.main(N_SAMPLES, output_file=FILE_NAME_SIM_LCHARS)
    else:
        # synthesize data
        synthesize_lpaths.main(
            "Active", "Sensory", "Sequential", "Visual", N_SAMPLES, FILE_NAME_SYN_LPATHS
        )
        current_path = os.path.dirname(os.path.abspath(__file__))
        storage_path = (
            current_path + r"\source\synthesizer\LChars\savedmodels" + r"\{"
            r"}".format(BN_MODEL_NAME)
        )
        synthesize_lchars.main(storage_path, N_SAMPLES, FILE_NAME_SYN_LCHARS)
