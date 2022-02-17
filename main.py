from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QAbstractItemView, QFileDialog, QListWidget, QListWidgetItem, QPushButton, QLabel, QCheckBox, QLineEdit, QApplication
from PyQt5.QtGui import QColor, QIntValidator, QPixmap
import os
import librosa
import sys
import threading
# Customized Library
import Plot
import Export
import Style
import Functions

ICON_PATH = Functions.resource_path('Icon.ico')


class Ui_ProcessWindow(QWidget):
    def setupUi(self, ProcessWindow):
        ProcessWindow.setObjectName("ProcessWindow")
        ProcessWindow.setStyleSheet("background-color: rgb(20, 20, 21);")
        ProcessWindow.setFixedWidth(687)
        ProcessWindow.setFixedHeight(600)
        ProcessWindow.setWindowFlag(Qt.FramelessWindowHint)
        ProcessWindow.setWindowIcon(QtGui.QIcon(ICON_PATH))
        self.topwidget = QWidget(ProcessWindow)
        self.topwidget.setObjectName("topwidget")
        self.topwidget.setStyleSheet(Style.get_style())

        # Process Header
        self.header = QLabel(self.topwidget)
        self.header.setGeometry(QtCore.QRect(100, 340, 600, 200))
        self.header.setStyleSheet(Style.fontProcessStyle())

        # Process Image
        self.imageLabel = QLabel(self.topwidget)
        pixmap = QPixmap(ICON_PATH)
        self.imageLabel.setGeometry(QtCore.QRect(200, 70, 300, 300))
        self.imageLabel.setPixmap(pixmap)

        ProcessWindow.setCentralWidget(self.topwidget)
        Style.retranslateProcessUi(self, ProcessWindow)
        QtCore.QMetaObject.connectSlotsByName(ProcessWindow)


class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setStyleSheet("background-color: rgb(20, 20, 21);")
        MainWindow.setFixedWidth(687)
        MainWindow.setFixedHeight(600)
        MainWindow.setWindowIcon(QtGui.QIcon(ICON_PATH))
        self.topwidget = QWidget(MainWindow)
        self.topwidget.setObjectName("topwidget")
        self.topwidget.setStyleSheet(Style.get_style())

        # Upload Button
        self.uploadButton = QPushButton(self.topwidget)
        self.uploadButton.setGeometry(QtCore.QRect(20, 10, 210, 50))
        self.uploadButton.clicked.connect(self.uploadButton_handler)

        # Plot Button
        self.plotButton = QPushButton(self.topwidget)
        self.plotButton.setGeometry(QtCore.QRect(240, 10, 210, 50))
        self.plotButton.setEnabled(False)
        self.plotButton.clicked.connect(self.plotButton_handler)

        # Export Button
        self.exportButton = QPushButton(self.topwidget)
        self.exportButton.setGeometry(QtCore.QRect(460, 10, 210, 50))
        self.exportButton.setEnabled(False)
        self.exportButton.clicked.connect(self.exportButton_handler)

        # Average Checkbox
        self.averageCheckbox = QCheckBox("Average", self.topwidget)
        self.averageCheckbox.setGeometry(QtCore.QRect(150, 80, 100, 31))
        self.averageCheckbox.setStyleSheet(Style.fontCheckStyle())
        self.averageCheckbox.setChecked(False)
        self.averageCheckbox.setEnabled(False)
        self.averageCheckbox.stateChanged.connect(self.averageCheckbox_handler)

        # Compare Checkbox
        self.compareCheckbox = QCheckBox("Compare", self.topwidget)
        self.compareCheckbox.setGeometry(QtCore.QRect(280, 80, 110, 31))
        self.compareCheckbox.setStyleSheet(Style.fontCheckStyle())
        self.compareCheckbox.setChecked(False)
        self.compareCheckbox.setEnabled(False)
        self.compareCheckbox.stateChanged.connect(self.compareCheckbox_handler)

        # Standard Deviation Checkbox
        self.sdCheckbox = QCheckBox("Standard Deviation", self.topwidget)
        self.sdCheckbox.setGeometry(QtCore.QRect(410, 80, 200, 31))
        self.sdCheckbox.setStyleSheet(Style.fontCheckStyle())
        self.sdCheckbox.setChecked(False)
        self.sdCheckbox.setEnabled(False)

        # Source Checkbox
        self.sourceCheckbox = QCheckBox("Source", self.topwidget)
        self.sourceCheckbox.setGeometry(QtCore.QRect(150, 110, 110, 31))
        self.sourceCheckbox.setStyleSheet(Style.fontCheckStyle())
        self.sourceCheckbox.setChecked(False)
        self.sourceCheckbox.setEnabled(False)
        self.sourceCheckbox.stateChanged.connect(self.sourceCheckbox_handler)

        # Receiver Checkbox
        self.receiverCheckbox = QCheckBox("Receiver", self.topwidget)
        self.receiverCheckbox.setGeometry(QtCore.QRect(280, 110, 110, 31))
        self.receiverCheckbox.setStyleSheet(Style.fontCheckStyle())
        self.receiverCheckbox.setChecked(False)
        self.receiverCheckbox.setEnabled(False)
        self.receiverCheckbox.stateChanged.connect(
            self.receiverCheckbox_handler)

        # Int Validator
        self.onlyInt = QIntValidator()

        # Min Frequency Input
        self.minTextbox = QLineEdit(self.topwidget)
        self.minTextbox.setGeometry(QtCore.QRect(20, 150, 90, 30))
        self.minTextbox.setPlaceholderText(" Min [Hz]")
        self.minTextbox.setStyleSheet(Style.fontTextboxStyle())
        self.minTextbox.setValidator(self.onlyInt)

        # Max Frequency Input
        self.maxTextbox = QLineEdit(self.topwidget)
        self.maxTextbox.setGeometry(QtCore.QRect(120, 150, 90, 30))
        self.maxTextbox.setPlaceholderText(" Max [Hz]")
        self.maxTextbox.setStyleSheet(Style.fontTextboxStyle())
        self.maxTextbox.setValidator(self.onlyInt)

        # Average Export File Name Input
        self.fileNameTextbox = QLineEdit(self.topwidget)
        self.fileNameTextbox.setGeometry(QtCore.QRect(220, 150, 190, 30))
        self.fileNameTextbox.setPlaceholderText(" Average Export File Name")
        self.fileNameTextbox.setStyleSheet(Style.fontTextboxStyle())

        # Average Legend Name Name Input
        self.legendNameTextbox = QLineEdit(self.topwidget)
        self.legendNameTextbox.setMaxLength(31)
        self.legendNameTextbox.setGeometry(QtCore.QRect(420, 150, 190, 30))
        self.legendNameTextbox.setPlaceholderText(" Average Legend Name")
        self.legendNameTextbox.setStyleSheet(Style.fontTextboxStyle())

        # Audio List Heading
        self.audioListLabel = QLabel(self.topwidget)
        self.audioListLabel.setGeometry(QtCore.QRect(20, 80, 130, 31))

        # Remove Files Button
        self.removeButton = QPushButton(self.topwidget)
        self.removeButton.setGeometry(QtCore.QRect(20, 195, 130, 25))
        self.removeButton.clicked.connect(self.removeButton_handler)
        self.removeButton.setStyleSheet(Style.fontButtonStyle())
        self.removeButton.setEnabled(False)

        # Select All Button
        self.selectButton = QPushButton(self.topwidget)
        self.selectButton.setGeometry(QtCore.QRect(160, 195, 130, 25))
        self.selectButton.clicked.connect(self.selectButton_handler)
        self.selectButton.setStyleSheet(Style.fontButtonStyle())
        self.selectButton.setEnabled(False)

        # Unselect All Button
        self.unselectButton = QPushButton(self.topwidget)
        self.unselectButton.setGeometry(QtCore.QRect(300, 195, 130, 25))
        self.unselectButton.clicked.connect(self.unselectButton_handler)
        self.unselectButton.setStyleSheet(Style.fontButtonStyle())
        self.unselectButton.setEnabled(False)

        # Add to Compare Button
        self.addCompareButton = QPushButton(self.topwidget)
        self.addCompareButton.setGeometry(QtCore.QRect(440, 195, 210, 25))
        self.addCompareButton.clicked.connect(self.addCompareButton_handler)
        self.addCompareButton.setStyleSheet(Style.fontButtonStyle())
        self.addCompareButton.setEnabled(False)

        # File List
        self.fileList = QListWidget(self.topwidget)
        self.fileList.setGeometry(QtCore.QRect(20, 230, 650, 170))
        self.fileList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.fileList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.fileList.setStyleSheet(Style.fontListStyle())
        self.fileList.itemClicked.connect(self.listSelect_Handler)

        # Compare List
        self.compareList = QListWidget(self.topwidget)
        self.compareList.setGeometry(QtCore.QRect(20, 410, 360, 170))
        self.compareList.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.compareList.setStyleSheet(Style.fontListStyle())

        # Compare List Heading
        self.compareLabel = QLabel(self.topwidget)
        self.compareLabel.setGeometry(QtCore.QRect(400, 410, 230, 31))

        # Remove Compare Files Button
        self.removeCompareButton = QPushButton(self.topwidget)
        self.removeCompareButton.setGeometry(QtCore.QRect(400, 450, 240, 35))
        self.removeCompareButton.clicked.connect(
            self.removeCompareButton_handler)
        self.removeCompareButton.setStyleSheet(Style.fontButtonStyle())
        self.removeCompareButton.setEnabled(False)

        # Plot Compare All Button
        self.plotCompareButton = QPushButton(self.topwidget)
        self.plotCompareButton.setGeometry(QtCore.QRect(400, 495, 240, 35))
        self.plotCompareButton.clicked.connect(self.plotCompareButton_handler)
        self.plotCompareButton.setStyleSheet(Style.fontButtonStyle())
        self.plotCompareButton.setEnabled(False)

        # Plot Compare Export Button
        self.exportCompareButton = QPushButton(self.topwidget)
        self.exportCompareButton.setGeometry(QtCore.QRect(400, 540, 240, 35))
        self.exportCompareButton.clicked.connect(
            self.exportCompareButton_handler)
        self.exportCompareButton.setStyleSheet(Style.fontButtonStyle())
        self.exportCompareButton.setEnabled(False)

        MainWindow.setCentralWidget(self.topwidget)
        Style.retranslateUi(self, MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Checking Functions
    def check_freqrange(self):
        global minFreq, maxFreq
        if self.minTextbox.text() == "" or self.minTextbox.text() == "0":
            minFreq = "1"
        else:
            minFreq = self.minTextbox.text()
        if self.maxTextbox.text() == "":
            maxFreq = ""
        else:
            maxFreq = self.maxTextbox.text()

    def filter_paths(self):
        return [
            path for path in pathList
            if any(path for file in selectedFileList if str(file) in path)
        ]

    # Multiple Average Plot Comparison
    def exportCompareButton_handler(self):
        def process():
            if self.fileNameTextbox.text() == "":
                filename = "Multiple_Average_Result"
            else:
                filename = self.fileNameTextbox.text()
            if exportDirectory:
                Export.export_multiple_average(compareFileList, legendList,
                                               exportDirectory, filename)
            MainWindow.show()
            ProcessWindow.hide()

        """ Run """
        exportDirectory = str(
            QFileDialog.getExistingDirectory(self, "Select Export Directory"))

        ProcessWindow.show()
        MainWindow.hide()

        if ProcessWindow.isActiveWindow() and MainWindow.isHidden():
            QTimer.singleShot(
                1, process)  #waits for this to finish until gui displayed

    def removeCompareButton_handler(self):
        compareFileList.clear()
        legendList.clear()
        colourList.clear()
        self.compareList.clear()
        self.removeCompareButton.setEnabled(False)
        self.plotCompareButton.setEnabled(False)
        self.exportCompareButton.setEnabled(False)
        self.addCompareButton.setEnabled(False)

    def plotCompareButton_handler(self):
        def process():
            self.check_freqrange()
            Plot.plot_compare_average(compareFileList, minFreq, maxFreq,
                                      colourList, legendList,
                                      self.sourceCheckbox.isChecked(),
                                      self.receiverCheckbox.isChecked(),
                                      self.sdCheckbox.isChecked())
            MainWindow.show()
            ProcessWindow.hide()

        """ Run """
        ProcessWindow.show()
        MainWindow.hide()

        if ProcessWindow.isActiveWindow() and MainWindow.isHidden():
            QTimer.singleShot(
                1, process)  #waits for this to finish until gui displayed

    def addCompareButton_handler(self):
        filteredPathList = self.filter_paths()
        legendName = self.legendNameTextbox.text()

        if len(legendName) > 1:
            if filteredPathList not in compareFileList and legendName not in legendList:
                compareFileList.append(filteredPathList)
                color = Functions.random_colour()
                colourList.append(color[0])
                legendList.append(legendName)
                legendItem = QListWidgetItem(legendName)
                self.compareList.addItem(legendItem)
                legendItem.setFlags(Qt.NoItemFlags)

                for path in filteredPathList:
                    url = QtCore.QUrl.fromLocalFile(path)
                    item = QListWidgetItem(url.fileName())
                    self.compareList.addItem(item)
                    item.setFlags(Qt.NoItemFlags)
                    item.setBackground(QColor(color[0]))

                self.removeCompareButton.setEnabled(True)
                self.plotCompareButton.setEnabled(True)
                self.exportCompareButton.setEnabled(True)
                self.plotButton.setEnabled(False)
                self.exportButton.setEnabled(False)
                self.averageCheckbox.setChecked(False)
                self.averageCheckbox.setEnabled(False)
                self.compareCheckbox.setChecked(False)
                self.compareCheckbox.setEnabled(False)
                self.fileList.clearSelection()
                self.legendNameTextbox.clear()
                selectedFileList.clear()
        else:
            self.legendNameTextbox.setFocus(True)

    # Checkbox Handlers
    def averageCheckbox_handler(self, state):
        if state == QtCore.Qt.Checked: self.compareCheckbox.setChecked(False)

    def compareCheckbox_handler(self, state):
        if state == QtCore.Qt.Checked: self.averageCheckbox.setChecked(False)

    def sourceCheckbox_handler(self, state):
        if state != QtCore.Qt.Checked: self.receiverCheckbox.setChecked(True)

    def receiverCheckbox_handler(self, state):
        if state != QtCore.Qt.Checked: self.sourceCheckbox.setChecked(True)

    # Audio List Selection
    def removeButton_handler(self):
        self.fileList.clear()
        self.compareList.clear()
        selectedFileList.clear()
        compareFileList.clear()
        pathList.clear()
        legendList.clear()
        colourList.clear()
        self.plotButton.setEnabled(False)
        self.exportButton.setEnabled(False)
        self.averageCheckbox.setChecked(False)
        self.averageCheckbox.setEnabled(False)
        self.compareCheckbox.setChecked(False)
        self.compareCheckbox.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.selectButton.setEnabled(False)
        self.unselectButton.setEnabled(False)
        self.addCompareButton.setEnabled(False)
        self.removeCompareButton.setEnabled(False)
        self.plotCompareButton.setEnabled(False)
        self.exportCompareButton.setEnabled(False)
        self.sourceCheckbox.setEnabled(False)
        self.sourceCheckbox.setChecked(False)
        self.receiverCheckbox.setEnabled(False)
        self.receiverCheckbox.setChecked(False)
        self.sdCheckbox.setEnabled(False)
        self.sdCheckbox.setChecked(False)

    def selectButton_handler(self):
        selectedFileList.clear()
        self.plotButton.setEnabled(True)
        self.exportButton.setEnabled(True)

        for i in range(len(pathList)):
            self.fileList.item(i).setSelected(True)
        for file in range(len(self.fileList.selectedItems())):
            selectedFileList.append(
                str(self.fileList.selectedItems()[file].text()))

        if len(selectedFileList) < 2:
            self.averageCheckbox.setChecked(False)
            self.averageCheckbox.setEnabled(False)
            self.compareCheckbox.setChecked(False)
            self.compareCheckbox.setEnabled(False)
            self.addCompareButton.setEnabled(False)
            self.sdCheckbox.setEnabled(False)
            self.sdCheckbox.setChecked(False)
        else:
            self.averageCheckbox.setEnabled(True)
            self.compareCheckbox.setEnabled(True)
            self.addCompareButton.setEnabled(True)
            self.sdCheckbox.setEnabled(True)

    def unselectButton_handler(self):
        self.fileList.clearSelection()
        selectedFileList.clear()
        self.plotButton.setEnabled(False)
        self.exportButton.setEnabled(False)
        self.averageCheckbox.setChecked(False)
        self.averageCheckbox.setEnabled(False)
        self.compareCheckbox.setChecked(False)
        self.compareCheckbox.setEnabled(False)
        self.addCompareButton.setEnabled(False)
        self.sdCheckbox.setEnabled(False)
        self.sdCheckbox.setChecked(False)

    def listSelect_Handler(self):
        selectedFileList.clear()  # Clear existing selected files

        for file in range(len(self.fileList.selectedItems())):
            selectedFileList.append(
                str(self.fileList.selectedItems()[file].text()))

        if len(selectedFileList) == 0:
            self.plotButton.setEnabled(False)
            self.exportButton.setEnabled(False)
            self.averageCheckbox.setEnabled(False)
            self.compareCheckbox.setEnabled(False)
            self.addCompareButton.setEnabled(False)
        else:
            self.plotButton.setEnabled(True)
            self.exportButton.setEnabled(True)
            self.addCompareButton.setEnabled(True)

            if len(selectedFileList) < 2:
                self.averageCheckbox.setChecked(False)
                self.averageCheckbox.setEnabled(False)
                self.compareCheckbox.setChecked(False)
                self.compareCheckbox.setEnabled(False)
                self.addCompareButton.setEnabled(False)
                self.sdCheckbox.setEnabled(False)
                self.sdCheckbox.setChecked(False)
            else:
                self.averageCheckbox.setEnabled(True)
                self.compareCheckbox.setEnabled(True)
                self.addCompareButton.setEnabled(True)
                self.sdCheckbox.setEnabled(True)

    # Main Buttons Handler
    def uploadButton_handler(self):
        global pathList, audioNames, selectedFileList, compareFileList, colourList, legendList
        selectedFileList, compareFileList, colourList, legendList = [], [], [], []
        filename = QFileDialog.getOpenFileNames(parent=self,
                                                caption="Select Audio Files",
                                                filter="*.wav ",
                                                directory=os.getcwd())
        pathList = filename[0]  # Set List of Audio File Directory
        self.fileList.clear()  # Clear File List
        self.compareList.clear()
        selectedFileList.clear()
        compareFileList.clear()
        legendList.clear()
        colourList.clear()

        if pathList:
            self.plotButton.setEnabled(True)
            self.exportButton.setEnabled(True)
            self.removeButton.setEnabled(True)
            self.selectButton.setEnabled(True)
            self.unselectButton.setEnabled(True)
            self.sourceCheckbox.setEnabled(True)
            self.sourceCheckbox.setChecked(True)
            self.receiverCheckbox.setEnabled(True)
            self.receiverCheckbox.setChecked(True)

            if len(pathList) > 1:
                self.averageCheckbox.setEnabled(True)
                self.compareCheckbox.setEnabled(True)
                self.addCompareButton.setEnabled(True)
                self.sdCheckbox.setEnabled(True)
            else:
                self.averageCheckbox.setEnabled(False)
                self.compareCheckbox.setEnabled(False)
                self.addCompareButton.setEnabled(False)
                self.sdCheckbox.setEnabled(False)
                self.sdCheckbox.setChecked(False)

            for path in pathList:
                url = QtCore.QUrl.fromLocalFile(path)
                item = QListWidgetItem(url.fileName())
                self.fileList.addItem(item)
                item.setSelected(True)

            for file in range(len(self.fileList.selectedItems())):
                selectedFileList.append(
                    str(self.fileList.selectedItems()[file].text()))
        else:
            self.fileList.clear()
            self.plotButton.setEnabled(False)
            self.exportButton.setEnabled(False)
            self.averageCheckbox.setChecked(False)
            self.averageCheckbox.setEnabled(False)
            self.compareCheckbox.setChecked(False)
            self.compareCheckbox.setEnabled(False)
            self.removeButton.setEnabled(False)
            self.selectButton.setEnabled(False)
            self.unselectButton.setEnabled(False)
            self.sourceCheckbox.setEnabled(False)
            self.sourceCheckbox.setChecked(False)
            self.receiverCheckbox.setEnabled(False)
            self.receiverCheckbox.setChecked(False)
            self.sdCheckbox.setEnabled(False)
            self.sdCheckbox.setChecked(False)

    def plotButton_handler(self):
        def process():
            self.check_freqrange()
            filteredPathList = self.filter_paths()

            if self.averageCheckbox.isChecked():
                Plot.plot_average(filteredPathList, minFreq, maxFreq,
                                  self.sourceCheckbox.isChecked(),
                                  self.receiverCheckbox.isChecked(),
                                  self.sdCheckbox.isChecked())
            elif self.compareCheckbox.isChecked():
                Plot.plot_compare(filteredPathList, minFreq, maxFreq,
                                  self.sourceCheckbox.isChecked(),
                                  self.receiverCheckbox.isChecked())
            else:
                for path in filteredPathList:
                    url = QtCore.QUrl.fromLocalFile(path)
                    signal, sr = librosa.load(path, sr=None,
                                              mono=False)  #Load audio file
                    Plot.plot_waveform(signal, sr, url.fileName(),
                                       minFreq, maxFreq,
                                       self.sourceCheckbox.isChecked(),
                                       self.receiverCheckbox.isChecked())
            MainWindow.show()
            ProcessWindow.hide()

        """ Run """
        ProcessWindow.show()
        MainWindow.hide()

        if ProcessWindow.isActiveWindow() and MainWindow.isHidden():
            QTimer.singleShot(
                1, process)  #waits for this to finish until gui displayed

    def exportButton_handler(self):
        def exportProcess(path):
            url = QtCore.QUrl.fromLocalFile(path)
            signal, sr = librosa.load(path, sr=None,
                                      mono=False)  #Load audio file
            Export.export_data(signal, sr, url, exportDirectory)

        def process():
            threads = []
            if exportDirectory:
                filteredPathList = self.filter_paths()
                if self.fileNameTextbox.text() == "":
                    filename = "Average_Result"
                else:
                    filename = self.fileNameTextbox.text()

                if self.averageCheckbox.isChecked():
                    Export.export_average(filteredPathList, exportDirectory,
                                          filename)
                else:
                    for path in filteredPathList:
                        t = threading.Thread(target=exportProcess,
                                             args=(path, ))
                        t.start()
                        threads.append(t)
                    for t in threads:
                        t.join()

            MainWindow.show()
            ProcessWindow.hide()

        """ Run """
        exportDirectory = str(
            QFileDialog.getExistingDirectory(self, "Select Export Directory"))

        ProcessWindow.show()
        MainWindow.hide()

        if ProcessWindow.isActiveWindow() and MainWindow.isHidden():
            QTimer.singleShot(
                1, process)  #waits for this to finish until gui displayed


if __name__ == "__main__":
    Functions.suppress_qt_warnings()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    main_ui = Ui_MainWindow()
    main_ui.setupUi(MainWindow)
    MainWindow.show()
    ProcessWindow = QMainWindow()
    process_ui = Ui_ProcessWindow()
    process_ui.setupUi(ProcessWindow)
    ProcessWindow.hide()
    sys.exit(app.exec_())
