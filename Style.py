def get_style():
    style = '''
        QPushButton {
            color: white;
            font: 75 16pt Alef;
            border: 2px solid;
            border-color: white;
            border-radius: 10px;
        }

        QPushButton:hover {
            color: #000000;
            background-color:white;
        }

        QWidget#waveformWidget {
            border : 2px solid;
            border-color: white;
        }

        QLabel {
            color: white;
            font: 75 16pt Alef;
        }

        QListWidget {
            border: 2px solid;
            border-color: white;
            border-radius: 10px;
        }

        QListWidget::item:selected {
            background-color:green;
            color: white;
            border-radius: 2px;
        }

        QScrollBar:vertical {
            width: 10px;
            background: none;
        }

        QCheckBox::indicator:checked {background-color : lightgreen;}
    '''
    return style


def fontProcessStyle():
    return "font-weight: bold; font-size: 54pt;"


def fontButtonStyle():
    return "font-weight: bold; font-size: 12pt;"


def fontCheckStyle():
    return "color: white; font-weight: bold; font-size: 14pt;"


def fontListStyle():
    return "font: 75 16pt Alef; color: white; font-weight: bold;"


def fontTextboxStyle():
    return "color: white; font-weight: bold;"


def retranslateUi(self, MainWindow):
    MainWindow.setWindowTitle("Audio Signal Processing")
    self.uploadButton.setText("Upload")
    self.plotButton.setText("Plot")
    self.exportButton.setText("Export")
    self.audioListLabel.setText(
        "<html><head/><body><p><span style=\" font-weight:600;\">Audio List </span></p></body></html>"
    )
    self.removeButton.setText("Remove All")
    self.selectButton.setText("Select All")
    self.unselectButton.setText("Unselect All")
    self.removeCompareButton.setText("Remove All")
    self.plotCompareButton.setText("Plot")
    self.exportCompareButton.setText("Export")
    self.addCompareButton.setText("Compare Average List")
    self.compareLabel.setText(
        "<html><head/><body><p><span style=\" font-weight:600;\">Average Compare List </span></p></body></html>"
    )


def retranslateProcessUi(self, ProcessWindow):
    ProcessWindow.setWindowTitle("Audio Signal Processing")
    self.header.setText(
        "<html><head/><body><p><span style=\" font-weight:600;\">PROCESSING...</span></p></body></html>"
    )