from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.clock import Clock
from datetime import timedelta
from kivy.core.window import Window
from plyer import vibrator

class TimerWindow(Widget):
    def __init__(self):
        super().__init__()

        self.zeroCountString = "0:00:00.000"
        self.timerLabel.text = self.zeroCountString
#        self.screenSize.text = str(Window.size)

        # Create a timer to update the stopwatch
        timer = Clock.schedule_interval(self.increaseTimer, 0.001)

        # Create a timer to update the display
        guiUpdateTimer = Clock.schedule_interval(self.updateWindow, 0.1)

        self.startCount = False
        self.msCount = 0
    
#        Window.bind(on_resize=self.on_window_resize)


    def increaseTimer(self,dt):
        if self.startCount:
            self.msCount += dt*1000
    
    def startTimer(self):
        try:
            vibrator.vibrate(0.1)  # vibrate for 0.1 seconds
        except NotImplementedError:
            print("Cannot call the vibrate function as it is not supported on this platform")
        if self.startCount:
            self.startCount = False
            self.stopButton.disabled = False
        else:
            self.startCount = True
            self.stopButton.disabled = True

    def stopTimer(self):
        try:
            vibrator.vibrate(0.1)  # vibrate for 0.1 seconds
        except NotImplementedError:
            print("Cannot call the vibrate function as it is not supported on this platform")
        if not self.startCount:
            self.msCount = 0
            self.timerLabel.text = self.zeroCountString
    
    def updateWindow(self,dt):
        if self.startCount:
            delta = timedelta(milliseconds=self.msCount)
            self.timerLabel.text = str(delta)[0:-3]

#    def on_window_resize(self,window,width,height):
#        print(width)
#        print(height)
#        self.screenSize.text = f"({width},{height})"

class TimerApp(App):
    def on_resize(self):
        print (Window.size)
    def build(self):
        return TimerWindow()

if __name__ == '__main__':
    Config.set('graphics', 'resizable', True)
    TimerApp().run()