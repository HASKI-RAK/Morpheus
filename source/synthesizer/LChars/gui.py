import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
from source.synthesizer.LChars import main


class DataSynthesizerLChars(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bayesian Network Data Synthesizer")
        self.geometry("700x300")

        self.num_students = tk.IntVar(value=100)
        self.file_name_var = tk.StringVar(
            value='synthesized_learning_path_data.csv')
        self.learning_style_info = {'Processing': None,
                                    'Perception': None,
                                    'Understanding': None,
                                    'Input': None}
        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        """Create and run the GUI application."""
        # Set window size and make it non-resizable
        self.geometry("700x300")
        self.resizable(False, False)

        # Configure grid layout
        self.columnconfigure(1, weight=1)

        # Labels and Entries
        # Model Path
        tk.Label(self, text="BN Model Path:", anchor='e').grid(row=0, column=0,
                                                               padx=10,
                                                               pady=10,
                                                               sticky='e')
        model_path_entry = tk.Entry(self, width=50)

        current_dir = os.path.dirname(__file__)
        default_model_path = current_dir + (r'\savedmodels\26-09'
                                            r'-2024_iceri_b_est_k2.xml')
        model_path_entry.insert(0, default_model_path)
        model_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        browse_button = tk.Button(self, text="Browse",
                                  command=lambda: self.browse_model_file(
                                      model_path_entry))
        browse_button.grid(row=0, column=2, padx=10, pady=10)

        # Number of Samples
        tk.Label(self, text="Number of Samples:", anchor='e').grid(row=1,
                                                                   column=0,
                                                                   padx=10,
                                                                   pady=10,
                                                                   sticky='e')
        n_samples_entry = tk.Entry(self, width=20)
        n_samples_entry.insert(0, "1000")
        n_samples_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Output Filename
        tk.Label(self, text="Output Filename:", anchor='e').grid(row=2,
                                                                 column=0,
                                                                 padx=10,
                                                                 pady=10,
                                                                 sticky='e')
        output_filename_entry = tk.Entry(self, width=50)
        output_filename_entry.insert(0, "simulated_data.csv")
        output_filename_entry.grid(row=2, column=1, padx=10, pady=10,
                                   sticky='w')

        # Run Button
        run_button = tk.Button(
            self, text="Run Simulation",
            bg="green", fg="white", font=('Helvetica', 12, 'bold'),
            command=lambda: self.run_simulation(
                model_path_entry.get(),
                n_samples_entry.get(),
                output_filename_entry.get(),
                status_label,
                progress_bar,
                run_button
            )
        )
        run_button.grid(row=3, column=1, padx=10, pady=20)

        # Progress Bar
        progress_bar = ttk.Progressbar(self, mode='determinate')
        progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=5,
                          sticky='we')

        # Status Label
        status_label = tk.Label(self, text="", fg="blue")
        status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def center_window(self, width=700, height=300):
        '''
        center GUI window in the screen
        :param width:
        :param height:
        :return:
        '''
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f'{width}x{height}+{x}+{y}')

    def browse_model_file(self, entry):
        """Open a file dialog to select the BN model file and set the entry
        value."""
        file_path = filedialog.askopenfilename(
            title="Select BN Model File",
            filetypes=(("XMLBIF Files", "*.xml"), ("All Files", "*.*"))
        )
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def run_simulation(self,
                       model_path, n_samples, output_filename,
                       status_label, progress_bar, run_button
                       ):
        """
        Run the simulation in a separate thread to keep the GUI responsive.

        Parameters:
        - model_path (str): Path to the BN model file.
        - n_samples (int): Number of samples to generate.
        - output_filename (str): Name of the output CSV file.
        - status_label (tk.Label): Label to display status messages.
        - progress_bar (ttk.Progressbar): Progress bar widget.
        - run_button (tk.Button): The Run button to disable during processing.
        """
        self.simulation_thread(model_path, n_samples, output_filename,
                               status_label, progress_bar, run_button
                               )

    def simulation_thread(self, model_path, n_samples, output_filename,
                          status_label, progress_bar, run_button
                          ):
        try:
            # Validate number of samples
            n_samples_int = int(n_samples)
            if n_samples_int <= 0:
                raise ValueError("Number of samples must be a positive "
                                 "integer.")
        except ValueError as ve:
            messagebox.showerror("Invalid Input", f"Number of samples "
                                                  f"error: {ve}")
            progress_bar.stop()
            run_button.config(state=tk.NORMAL)
            return

        # Update status
        status_label.config(text="Running simulation...", fg="blue")
        progress_bar["value"] = 0
        progress_bar.start()
        run_button.config(state=tk.DISABLED)

        try:
            # Call the main function from simulate_bn.py
            output_path = main.main(
                model_path=model_path,
                n_samples=n_samples_int,
                output_filename=output_filename
            )
            # If successful, update status
            status_label.config(text="Simulation completed successfully!",
                                fg="green")
            messagebox.showinfo("Success",
                                f"Simulated data saved to {output_path}")
        except Exception as e:
            # If there's an error, display it
            status_label.config(text="Simulation failed.", fg="red")
            messagebox.showerror("Error", f"An error occurred:\n{e}")
        finally:
            progress_bar.stop()
            progress_bar["value"] = 100
            run_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = DataSynthesizerLChars()
    app.mainloop()
