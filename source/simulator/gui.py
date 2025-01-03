import source.simulator.LChars.gui as guiLChars
import source.simulator.LPaths.gui as guiLPaths


def start_gui():
    """
    start both data generator guis after each other
    """
    app = guiLPaths.DataGeneratorGUI()
    app.mainloop()
    app = guiLChars.DataGeneratorGUI()
    app.mainloop()


if __name__ == "__main__":
    start_gui()
