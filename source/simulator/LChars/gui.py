import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

from source.simulator.LChars.config import Config
from source.simulator.LChars.generator import DataGenerator
from source.simulator.LChars.utils import decode_categorical, encode_categorical

# Add the 'source' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


class DataGeneratorGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Data Generator")
        self.geometry("1000x600")

        self.config = Config()
        self.data_generator = DataGenerator(self.config)

        self.num_students = tk.IntVar(value=100)
        self.file_name_var = tk.StringVar(value="generated_data.csv")
        self.alpha_value = tk.DoubleVar(value=0.0)
        self.reference_file_path = tk.StringVar(value="")

        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        ttk.Label(self, text="Number of Students:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.num_students).grid(
            row=0, column=1, sticky=tk.W
        )

        ttk.Label(self, text="Alpha (Euclidean distance):").grid(
            row=1, column=0, sticky=tk.W
        )
        ttk.Entry(self, textvariable=self.alpha_value).grid(
            row=1, column=1, sticky=tk.W
        )

        ttk.Label(self, text="Reference Dataset:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.reference_file_path, state="readonly").grid(
            row=2, column=1, sticky=tk.W
        )
        ttk.Button(self, text="Browse", command=self.load_reference_file).grid(
            row=2, column=2, sticky=tk.W
        )

        ttk.Label(self, text="File name to save:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.file_name_var).grid(
            row=3, column=1, sticky=tk.W
        )

        ttk.Label(self, text="Distributions for Numerical Data:").grid(
            row=4, column=0, sticky=tk.W, pady=10
        )
        self.dist_frame = ttk.Frame(self)
        self.dist_frame.grid(row=5, column=0, columnspan=6, sticky=tk.W)

        bold_font = ("TkDefaultFont", 9, "bold")

        ttk.Label(self.dist_frame, text="Type of Distribution").grid(
            row=0, column=1, sticky=tk.W
        )
        ttk.Label(self.dist_frame, text="Parameters").grid(row=0, column=2, sticky=tk.W)
        ttk.Label(self.dist_frame, text="Possible Values").grid(
            row=0, column=3, sticky=tk.W
        )
        ttk.Label(self.dist_frame, text="Info").grid(row=0, column=4, sticky=tk.W)

        self.dist_type_vars = {}
        self.params_vars = {}
        self.possible_values_vars = {}

        numerical_columns = [
            "cs",
            "mcs",
            "smir",
            "smer",
            "bfie",
            "bfin",
            "bfio",
            "bfic",
            "bfia",
        ]

        for i, col in enumerate(numerical_columns):
            ttk.Label(self.dist_frame, text=f"{col}:").grid(
                row=i + 1, column=0, sticky=tk.W
            )
            self.add_dist_options(i + 1, col)

        ttk.Label(self, text="Probabilities for Categorical Data:").grid(
            row=20, column=0, sticky=tk.W, pady=10
        )
        self.cat_frame = ttk.Frame(self)
        self.cat_frame.grid(row=21, column=0, columnspan=6, sticky=tk.W)

        ttk.Label(self.cat_frame, text="Column").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.cat_frame, text="Probabilities").grid(
            row=0, column=1, sticky=tk.W
        )
        ttk.Label(self.cat_frame, text="Info").grid(row=0, column=2, sticky=tk.W)

        self.probs_vars = {}

        for i, col in enumerate(self.config.cat_dist_probs.keys()):
            ttk.Label(self.cat_frame, text=f"{col}:").grid(
                row=i + 1, column=0, sticky=tk.W
            )
            self.add_cat_options(i + 1, col)

        ttk.Button(self, text="Generate Data", command=self.generate_data).grid(
            row=41, column=0, pady=20
        )

    def center_window(self, width=1000, height=600):
        """
        center GUI window in the screen
        :param width:
        :param height:
        :return:
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def add_dist_options(self, row, col):
        dist_types = ["uniform", "normal", "binomial", "weibull"]
        dist_type_var = tk.StringVar(value="normal")
        params_var = tk.StringVar(value="5, 2")
        possible_values_var = tk.StringVar(value="1, 3, 5, 7, 9, 11")

        def update_params(*args):
            if dist_type_var.get() == "binomial":
                params_var.set("10, 0.5")  # default values for binomial distribution
            elif dist_type_var.get() == "weibull":
                params_var.set("2, 1")  # default values for Weibull distribution
            elif dist_type_var.get() == "uniform":
                params_var.set("")  # No parameters for uniform distribution
            else:
                params_var.set("5, 2")  # default values for normal distribution

        dist_type_var.trace("w", update_params)

        ttk.Combobox(
            self.dist_frame, textvariable=dist_type_var, values=dist_types
        ).grid(row=row, column=1, sticky=tk.W)
        ttk.Entry(self.dist_frame, textvariable=params_var).grid(
            row=row, column=2, sticky=tk.W
        )
        ttk.Entry(self.dist_frame, textvariable=possible_values_var).grid(
            row=row, column=3, sticky=tk.W
        )

        info_button = ttk.Button(
            self.dist_frame,
            text="Info",
            command=lambda: self.show_info(
                dist_type_var.get(), params_var.get(), possible_values_var.get()
            ),
        )
        info_button.grid(row=row, column=4, sticky=tk.W)

        self.dist_type_vars[col] = dist_type_var
        self.params_vars[col] = params_var
        self.possible_values_vars[col] = possible_values_var

    def add_cat_options(self, row, col):
        probs_var = tk.StringVar(value="0.5, 0.5")
        ttk.Entry(self.cat_frame, textvariable=probs_var).grid(
            row=row, column=1, sticky=tk.W
        )

        info_button = ttk.Button(
            self.cat_frame,
            text="Info",
            command=lambda: self.show_cat_info(probs_var.get()),
        )
        info_button.grid(row=row, column=2, sticky=tk.W)

        self.probs_vars[col] = probs_var

    def show_info(self, dist_type, params, possible_values):
        if dist_type == "uniform":
            info_text = (
                "Uniform distribution. No parameters needed. "
                "Possible values: Choose from the list."
            )
        elif dist_type == "normal":
            info_text = (
                f"Normal distribution with mean (mu) and standard "
                f"deviation (sigma). Parameters: {params}. Poss"
                f"ible values: {possible_values}"
            )
        elif dist_type == "binomial":
            info_text = (
                f"Binomial distribution with number of trials (n) "
                f"and probability of success (p). Parameters: {params}. Possible values:{possible_values}"
            )
        elif dist_type == "weibull":
            info_text = (
                f"Weibull distribution with shape parameter (a) and "
                f"scale parameter. Parameters: {params}. Poss"
                f"ible values: {possible_values}"
            )
        else:
            info_text = "Unknown distribution type."

        info_window = tk.Toplevel(self)
        info_window.title("Distribution Information")
        ttk.Label(info_window, text=info_text).pack(pady=10, padx=10)

    def show_cat_info(self, probs):
        info_text = (
            f"Categorical distribution with probabilities for each "
            f"category. Probabilities: {probs}. 0.5, 0.5 indicates "
            f"a 50-50% distribution."
        )

        info_window = tk.Toplevel(self)
        info_window.title("Categorical Information")
        ttk.Label(info_window, text=info_text).pack(pady=10, padx=10)

    def load_reference_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.reference_file_path.set(file_path)

    def generate_data(self):
        alpha = self.alpha_value.get()
        num_students = self.num_students.get()
        file_name = self.file_name_var.get()

        if alpha > 0:
            reference_file = self.reference_file_path.get()
            if not reference_file:
                messagebox.showerror("Error", "Please select a reference dataset.")
                return

            try:
                reference_df = pd.read_csv(reference_file)
                reference_df_encoded, ohe = encode_categorical(reference_df)
                new_data_encoded = self.data_generator.generate_data_with_alpha(
                    reference_df_encoded, alpha, num_students
                )
                new_data = decode_categorical(new_data_encoded, ohe, reference_df)
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to generate data with alpha: " f"{e}"
                )
                return
        else:
            # Convert StringVar entries to actual data structures for
            # numerical distribution information
            num_dist_info = {}
            for col in self.dist_type_vars.keys():
                dist_type = self.dist_type_vars[col].get()
                params_str = self.params_vars[col].get()
                possible_values_str = self.possible_values_vars[col].get()
                params = tuple(map(float, params_str.split(","))) if params_str else ()
                possible_values = (
                    list(map(float, possible_values_str.split(",")))
                    if possible_values_str
                    else []
                )
                num_dist_info[col] = {
                    "dist_type": dist_type,
                    "params": params,
                    "possible_values": possible_values,
                }
            self.config.num_dist_info = num_dist_info

            # Convert StringVar entries to actual lists for categorical
            # probabilities
            cat_dist_probs = {}
            for col in self.probs_vars.keys():
                probs = list(map(float, self.probs_vars[col].get().split(",")))
                cat_dist_probs[col] = probs
            self.config.cat_dist_probs = cat_dist_probs

            new_data = self.data_generator.generate_student_data(num_students)

        dir_name = os.path.dirname(__file__)
        root_dir = dir_name.replace(r"\source\simulator\LChars", "")
        path = root_dir + r"\data\simulated" + r"\{}".format(file_name)
        new_data.to_csv(path, index=False)
        messagebox.showinfo("Success", f"Data generated and saved to {file_name}")
        self.destroy()


if __name__ == "__main__":
    app = DataGeneratorGUI()
    app.mainloop()
