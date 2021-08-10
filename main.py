from threading import Timer
from .interface import AbstractSensor
try:
    from gpiozero import Button
except:
    Button = None

class SensorAdaptor(AbstractSensor):

    def __init__(self, pin_number, is_inverting=False):
        assert Button, 'This adaptor requires gpiozero library to be installed'
        self.sensor = Button(pin_number, pull_up=False)
        self.__is_inverting = is_inverting
        self.__start_update_timer()

    @property
    def is_on(self):
        if self.__is_inverting:
            return not self.sensor.is_pressed
        return bool(self.sensor.is_pressed)

    @property
    def on_active(self): 
        pass

    @on_active.setter
    def on_active(self, callback):
        self.sensor.when_pressed = callback
        self.__on_active = callback

    @property
    def on_inactive(self): 
        pass

    @on_inactive.setter
    def on_inactive(self, callback):
        self.sensor.when_released = callback
        self.__on_inactive = callback
    
    def __start_update_timer(self):
        self.timer = Timer(10, self.__trigger_status_update)
        self.timer.start()

    def __trigger_status_update(self):
        if self.is_on:
            self.__on_active()
        else:
            self.__on_inactive()
        self.__start_update_timer()
