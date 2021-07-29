try:
    from gpiozero import Button
except:
    Button = None

class SensorAdaptor:

    def __init__(self, pin_number, is_inverting=False):
        assert Button, 'This adaptor requires gpiozero library to be installed'
        # using pull_up=True will fail for some sensors
        # if they are too weak to pull it down sufficiently
        self.sensor = Button(pin_number, pull_up=None, active_state=not is_inverting)

    @property
    def is_on(self):
        return bool(self.sensor.is_pressed)

    @property
    def on_active(self): 
        pass

    @on_active.setter
    def on_active(self, callback):
        self.sensor.when_pressed = callback

    @property
    def on_deactive(self): 
        pass

    @on_deactive.setter
    def on_deactive(self, callback):
        self.sensor.when_released = callback
