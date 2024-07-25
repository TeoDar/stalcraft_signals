# Для преобразования ui файла: python -m PyQt6.uic.pyuic -o ./app/interface.py -x ./app/interface.ui

from PyQt6.QtGui import QDialog
from ui_imagedialog import Ui_ImageDialog


def main():
    pass

if __name__ == "__main__":
    main()


class ImageDialog(QDialog, Ui_ImageDialog):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Make some local modifications.
        self.colorDepthCombo.addItem("2 colors (1 bit per pixel)")

        # Connect up the buttons.
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)