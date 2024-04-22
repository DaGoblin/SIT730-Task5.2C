from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import RPi.GPIO as GPIO
from functools import partial

redLEDPin = 5
greenLEDPin = 6
blueLEDPin = 26

duytCycle = 100
GPIO.setmode(GPIO.BCM)
GPIO.setup(redLEDPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(greenLEDPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(blueLEDPin, GPIO.OUT, initial=GPIO.LOW)


pwmRedLEDPin = GPIO.PWM(redLEDPin, duytCycle)
pwmRedLEDPin.start(0)

pwmGreenLEDPin = GPIO.PWM(greenLEDPin, duytCycle)
pwmGreenLEDPin.start(0)

pwmBlueLEDPin = GPIO.PWM(blueLEDPin, duytCycle)
pwmBlueLEDPin.start(0)



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(20, 20, 600, 600)
        self.setWindowTitle("Task 5.2C")
        self.initUI()
        # allLEDsOff()
    
    def initUI(self):
        
        self.timeRemainingDict = {
            'red': 0,
            'green': 0,
            'blue': 0
        }

       
        self.slider1 = QtWidgets.QSlider(self)
        self.slider1.setOrientation(1)
        self.slider1.move(50, 200)
        self.slider1.resize(200, 40)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(100)
        self.slider1.valueChanged.connect(lambda value: self.sliderChanged(pwmRedLEDPin, self.slider1))

        self.slider2 = QtWidgets.QSlider(self)
        self.slider2.setOrientation(1)
        self.slider2.move(50, 300)
        self.slider2.resize(200, 40)
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(100)
        self.slider2.valueChanged.connect(lambda value: self.sliderChanged(pwmGreenLEDPin, self.slider2))

        self.slider3 = QtWidgets.QSlider(self)
        self.slider3.setOrientation(1)
        self.slider3.move(50, 400)
        self.slider3.resize(200, 40)
        self.slider3.setMinimum(0)
        self.slider3.setMaximum(100)
        self.slider3.valueChanged.connect(lambda value: self.sliderChanged(pwmBlueLEDPin, self.slider3))

        self.numberField1 = QtWidgets.QSpinBox(self)
        self.numberField1.move(300, 200)
        self.numberField1.resize(100, 30)
        self.numberField1.setMinimum(0)
        self.numberField1.setMaximum(120)

        self.numberField2 = QtWidgets.QSpinBox(self)
        self.numberField2.move(300, 300)
        self.numberField2.resize(100, 30)
        self.numberField2.setMinimum(0)
        self.numberField2.setMaximum(120)

        self.numberField3 = QtWidgets.QSpinBox(self)
        self.numberField3.move(300, 400)
        self.numberField3.resize(100, 30)
        self.numberField3.setMinimum(0)
        self.numberField3.setMaximum(120)




        self.redTimer = QtCore.QTimer(self)
        self.redTimer.timeout.connect(lambda: self.timerCountdown('red', self.slider1, self.redTimer, self.numberField1))

        self.greenTimer = QtCore.QTimer(self)
        self.greenTimer.timeout.connect(lambda: self.timerCountdown('green', self.slider2, self.greenTimer, self.numberField2))

        self.blueTimer = QtCore.QTimer(self)
        self.blueTimer.timeout.connect(lambda: self.timerCountdown('blue', self.slider3, self.blueTimer, self.numberField3))


        self.timerButton1 = QtWidgets.QPushButton(self)
        self.timerButton1.move(420, 200)
        self.timerButton1.setText("Start Timer")       
        self.timerButton1.clicked.connect(partial(self.startTimer, 'red', self.redTimer, self.numberField1))
       
        self.timerButton2 = QtWidgets.QPushButton(self) 
        self.timerButton2.move(420, 300)
        self.timerButton2.setText("Start Timer")
        self.timerButton2.clicked.connect(partial(self.startTimer, 'green', self.greenTimer, self.numberField2))

        self.timerButton3 = QtWidgets.QPushButton(self)
        self.timerButton3.move(420, 400)
        self.timerButton3.setText("Start Timer")
        self.timerButton3.clicked.connect(partial(self.startTimer, 'blue', self.blueTimer, self.numberField3))

        self.instructionsLabel = QtWidgets.QLabel(self)
        self.instructionsLabel.move(50,50)
        self.instructionsLabel.resize(500,40)
        self.instructionsLabel.setText("Use the sliders to adjust the brightness of the LEDs and the spin boxes to set times in seconds. Max 120 seconds")
        self.instructionsLabel.setWordWrap(True)    

        self.redLabel = QtWidgets.QLabel(self)
        self.redLabel.move(50,170)
        self.redLabel.resize(200,40)
        self.redLabel.setText("Red LED")

        self.greenLabel = QtWidgets.QLabel(self)
        self.greenLabel.move(50,270)
        self.greenLabel.resize(200,40)
        self.greenLabel.setText("Green LED")

        self.blueLabel = QtWidgets.QLabel(self)
        self.blueLabel.move(50,370)
        self.blueLabel.resize(200,40)
        self.blueLabel.setText("Blue LED")

    def startTimer(self, colour, timer, spinBox):
        timer.start(1000)
        timeRemaing = spinBox.value()
        self.timeRemainingDict[colour] = timeRemaing
        print(self.timeRemainingDict)
        

    def timerCountdown(self, colour, slider, timer, spinBox):
        timeRemaing = self.timeRemainingDict.get(colour)
        
        if timeRemaing > 0:
            dimRate = slider.value() / timeRemaing
            timeRemaing -= 1
            newSliderValue = slider.value() - dimRate
            slider.setValue(int(newSliderValue)) 
            spinBox.setValue(timeRemaing)
            self.timeRemainingDict[colour] = timeRemaing     
        else:
            timer.stop()
    


    def sliderChanged(self, LEDPin, slider):
        LEDPin.ChangeDutyCycle(slider.value())

 

    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        allLEDsOff()


def window():
    app = QApplication(sys.argv)
    win = MainWindow()

    win.show()
    sys.exit(app.exec_())

def allLEDsOff():
    pwmBlueLEDPin.stop()
    pwmGreenLEDPin.stop()
    pwmRedLEDPin.stop()


window()