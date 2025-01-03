from source.synthesizer.LChars.gui import DataSynthesizerLChars
from source.synthesizer.LPaths.gui import DataSynthesizerLP


def start_gui():
    """
    call synthesizer GUIs for learning paths as well as learner
    characteristics
    """
    app = DataSynthesizerLP()
    app.mainloop()
    app = DataSynthesizerLChars()
    app.mainloop()


if __name__ == "__main__":
    start_gui()
