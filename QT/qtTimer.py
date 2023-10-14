from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget, QMenu, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer, Qt
from datetime import timedelta

# Create a font object that we will use for all widgets
defaultFont = QFont('Arial', 14)
timerFont = QFont('Arial', 36)

# Push button custom class
class CustomQPushButton(QPushButton):
    def __init__(self, text, font = defaultFont):
        super().__init__(text)
        self.setFont(font)

# Label custom class
class CustomQLabel(QLabel):
    def __init__(self, text, font = timerFont):
        super().__init__(text)
        self.setFont(font)

class MainWindow(QMainWindow):
    """Create our main window, sub-classed from the QMainWindow class"""
    def __init__(self, windowWidth = 400, windowHeight = 700):
        super().__init__()

        self.timerStatus = "Stopped"

        self.timerMsCount = 0
        self.origLabelString = "0:00:00.00"
        self.timerLabelString = self.origLabelString

        #Set the window sizes
        self.setMaximumHeight(windowHeight)
        self.setMaximumWidth(windowWidth)
        self.setMinimumHeight(windowHeight)
        self.setMinimumWidth(windowWidth)

        # Set the window's title
        self.setWindowTitle("Timer")

        # Create a vertical layout object to hold other widgets and layouts
        vLayout = QVBoxLayout()

        # Create a label to use for spacers
        spacerLabel = CustomQLabel("")

        # Create the required widgets for the timer
        self.timerLabel = CustomQLabel(self.origLabelString)
        self.timerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the widgets for the control buttons
        self.stopButton = CustomQPushButton("S&top")
        self.stopButton.setEnabled(False)
        pauseStartButton = CustomQPushButton("&Pause / Start")

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.stopButton)
        hLayout.addWidget(pauseStartButton)

        # Add the widgets and layouts to the main window
        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(self.timerLabel)
        vLayout.addWidget(spacerLabel)
        vLayout.addLayout(hLayout)
    
        # Create a widget, define the vLayout to it and then assign the widget to be the main widget of the main window
        widget = QWidget()
        widget.setLayout(vLayout)
        self.setCentralWidget(widget)

        self.show()

        # Use signals to link all buttons, sliders etc to functions (slots)
        self.stopButton.clicked.connect(self.stopTimer)
        pauseStartButton.clicked.connect(self.pauseTimer)

        # Setup a timer to update the millisecond counter
        self.updateTimer = QTimer(self)
        self.updateTimer.setInterval(1) #5 seconds
        self.updateTimer.timeout.connect(self.updateTimerValue)

        # Setup a timer to update the GUI
        self.updateLabelTimer = QTimer(self)
        self.updateLabelTimer.setInterval(100)
        self.updateLabelTimer.timeout.connect(self.updateTimerLabel)

    def stopTimer(self):
        self.updateTimer.stop()
        self.timerMsCount = 0
        self.timerLabel.setText(self.origLabelString)



    def pauseTimer(self):
        if self.timerStatus == "Stopped":
            self.updateTimer.start()
            self.updateLabelTimer.start()
            self.stopButton.setEnabled(False)
            self.timerStatus = "Started"
        elif self.timerStatus == "Started":
            self.updateTimer.stop()
            self.updateLabelTimer.stop()
            self.stopButton.setEnabled(True)
            self.timerStatus = "Stopped"
        print(self.timerStatus)

    def updateTimerValue(self):
        self.timerMsCount += self.updateTimer.interval()

    def formatTimerValue(self):
        delta = timedelta(milliseconds=self.timerMsCount)
        self.timerLabelString = str(delta)[0:-3]
    
    def updateTimerLabel(self):
        self.formatTimerValue()
        self.timerLabel.setText(self.timerLabelString)

class CustomQApplication(QApplication):
    """Create a class based on QApplication and define windows"""
    def __init__(self,args):
        super().__init__(args)

        # Create window
        mainWindow = MainWindow()

        self.exec()

# Only run this code when the file is run directly
if __name__ == "__main__":
    
    # Create an instance of the custom application class
    app = CustomQApplication([])