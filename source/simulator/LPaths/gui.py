# gui.py
import os
import tkinter as tk
from tkinter import messagebox, ttk

from source.simulator.LPaths.config import cat_dist_probs as default_cat_dist_probs
from source.simulator.LPaths.config import num_dist_info as default_num_dist_info
from source.simulator.LPaths.generator import generate_student_data
from source.simulator.LPaths.utils import convert_le_types


class DataGeneratorGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Data Generator")
        self.geometry("1000x600")

        self.num_students = tk.IntVar(value=100)
        self.file_name_var = tk.StringVar(value="simulated_learning_path_data.csv")
        self.num_dist_info = {}
        self.cat_dist_probs = {}

        # Initialize numerical distributions
        for i in range(1, 10):
            col = f"LE{i}"
            dist_type, params, possible_values = default_num_dist_info[col]
            self.num_dist_info[col] = {
                "dist_type": tk.StringVar(value=dist_type),
                "params": tk.StringVar(value=",".join(map(str, params))),
                "possible_values": tk.StringVar(
                    value=", ".join(map(str, possible_values))
                ),
            }

        # Initialize categorical distributions
        for key, probs in default_cat_dist_probs.items():
            self.cat_dist_probs[key] = tk.StringVar(value=",".join(map(str, probs)))

        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        """
        create widgets for GUI and arrange them inside a grid
        """
        ttk.Label(self, text="Number of Students:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.num_students).grid(
            row=0, column=1, sticky=tk.W
        )

        ttk.Label(self, text="File Name to Save:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.file_name_var).grid(
            row=1, column=1, sticky=tk.W
        )

        ttk.Label(self, text="Distributions for Learning Elements:").grid(
            row=2, column=0, sticky=tk.W, pady=10
        )
        self.dist_frame = ttk.Frame(self)
        self.dist_frame.grid(row=3, column=0, columnspan=5, sticky=tk.W)

        # Add column headings
        headings = ["Type of Distribution", "Parameters", "Possible Values", "Info"]
        for col_num, heading in enumerate(headings):
            ttk.Label(self.dist_frame, text=heading, font=("Arial", 9)).grid(
                row=3, column=col_num + 1, sticky=tk.W
            )

        for i in range(1, 10):
            col = f"LE{i}"
            ttk.Label(self.dist_frame, text=f"{col}:").grid(
                row=i + 3, column=0, sticky=tk.W
            )
            self.add_dist_options(i + 3, col)

        ttk.Label(self, text="Probabilities for Categorical Data:").grid(
            row=13, column=0, sticky=tk.W, pady=10
        )
        self.cat_frame = ttk.Frame(self)
        self.cat_frame.grid(row=14, column=0, columnspan=5, sticky=tk.W)

        for i, col in enumerate(self.cat_dist_probs.keys()):
            ttk.Label(self.cat_frame, text=f"{col}:").grid(row=i, column=0, sticky=tk.W)
            self.add_cat_options(i, col)

        ttk.Button(self, text="Generate Data", command=self.generate_data).grid(
            row=20, column=0, pady=20
        )

    def center_window(self, width=1000, height=600):
        """
        center GUI window in the screen
        :param width: width of GUI
        :param height: height of GUI
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def add_dist_options(self, row, col):
        """
        get widget for entering information about learning path data
        distributions for modification when being updated
        :param row: row of widget
        :param col: column of widget
        """
        dist_types = ["uniform", "normal", "binomial", "weibull"]
        dist_type_var = self.num_dist_info[col]["dist_type"]
        params_var = self.num_dist_info[col]["params"]
        possible_values_var = self.num_dist_info[col]["possible_values"]

        def update_params(*args):
            """
            update text in widgets when chosen distribution type changes
            :param args: responsible widgets
            :return:
            """
            if dist_type_var.get() == "binomial":
                params_var.set("10,0.5")  # Set default values for binomial distribution
            elif dist_type_var.get() == "weibull":
                params_var.set("2,1")  # Set default values for Weibull
                # distribution
            elif dist_type_var.get() == "uniform":
                params_var.set("")  # No parameters needed for uniform distribution
            else:
                params_var.set("5,2")  # Set default values for normal distribution

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
            command=lambda: self.show_information(dist_type_var.get()),
        )
        info_button.grid(row=row, column=4, sticky=tk.W)

    def add_cat_options(self, row, col):
        """
        add widgets to enter learning style distributions
        :param row: row of widget
        :param col: column of widget
        """
        probs_var = self.cat_dist_probs[col]
        ttk.Entry(self.cat_frame, textvariable=probs_var).grid(
            row=row, column=1, sticky=tk.W
        )
        info_button = ttk.Button(
            self.cat_frame,
            text="Info",
            command=lambda: self.show_cat_information(probs_var.get()),
        )
        info_button.grid(row=row, column=2, sticky=tk.W)

    def generate_data(self):
        """
        get information from GUI widgets and use it to generate the desired
        learning path data
        """
        num_dist_info_updated = {}
        for col, vars in self.num_dist_info.items():
            dist_type = vars["dist_type"].get()
            params_str = vars["params"].get()
            if params_str:
                params_splitted = params_str.split(",")
                params = [float(z) for z in params_splitted]
            else:
                params = []
            possible_values = []
            possible_values_str = vars["possible_values"].get()
            if possible_values_str:
                possible_values_le_types = possible_values_str.split(", ")
            else:
                possible_values_le_types = []
            possible_values = convert_le_types(possible_values_le_types)
            num_dist_info_updated[col] = (dist_type, params, possible_values)

        cat_dist_probs_updated = {}
        for col, probs_var in self.cat_dist_probs.items():
            probs = list(map(float, probs_var.get().split(",")))
            cat_dist_probs_updated[col] = probs

        num_students = self.num_students.get()
        df_gen = generate_student_data(
            num_students, num_dist_info_updated, cat_dist_probs_updated
        )
        file_name = self.file_name_var.get() or "generated_data.csv"
        dir_name = os.path.dirname(__file__)
        root_dir = dir_name.replace(r"\source\simulator\LPaths", "")
        path = root_dir + r"\data\simulated" + r"\{}".format(file_name)
        df_gen.to_csv(path, index=False)
        messagebox.showinfo("Success", f"Data generated and saved to {file_name}")
        self.destroy()

    def show_information(self, dist_type):
        """
        provide the user with a messagebox showing information about the
        parameters of the chosen distribution
        :param dist_type: applied distribution
        :return:
        """
        if dist_type == "uniform":
            info_text = (
                "Uniform Distribution:\nNo parameters "
                "needed.\nPossible Values: The values to choose "
                "from."
            )
        elif dist_type == "normal":
            info_text = (
                "Normal Distribution:\nParameters: mean (mu), "
                "standard deviation (sigma)."
            )
        elif dist_type == "binomial":
            info_text = (
                "Binomial Distribution:\nParameters: number of "
                "trials (n), probability of success (p)."
            )
        elif dist_type == "weibull":
            info_text = "Weibull Distribution:\nParameters: shape (a), scale."
        else:
            info_text = "Select a distribution type to see more information."
        messagebox.showinfo("Distribution Information", info_text)

    def show_cat_information(self, probs):
        """
        provide the user with information about the applied learning style
        distribution
        :param probs: probabilities of learning style distribution
        :return:
        """
        info_text = (
            f"Categorical Distribution:\nProbabilities: {probs}\nExplanation: The values represent the probability "
            f"distribution for the categories."
        )
        messagebox.showinfo("Categorical Distribution Information", info_text)


if __name__ == "__main__":
    app = DataGeneratorGUI()
    app.mainloop()
