import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from piinput import SensorAdaptor


@pytest.mark.usefixtures('patch_timer')
class TestPiInputAdaptor:
    
    def test_assigns_correct_pin_number(self):
        fake_pin_constructor = MagicMock()
        fake_pin_constructor.initialized_with = lambda a: a in fake_pin_constructor.call_args.args
        pin_number = 1583
        with patch('piinput.main.Button', new=fake_pin_constructor):
            SensorAdaptor(pin_number)
            assert fake_pin_constructor.initialized_with(pin_number)

    def test_IS_ON_returns_TRUE_when_sensor_is_ACTIVE(self, fake_button, sensor):
        fake_button.is_pressed = True
        assert sensor.is_on == True

    def test_IS_ON_returns_FALSE_when_sensor_is_INACTIVE(self, fake_button, sensor):
        fake_button.is_pressed = False
        assert sensor.is_on == False

    def test_IS_ON_converts_sensor_value_to_BOOLEAN(self, fake_button, sensor):
        fake_button.is_pressed = 1
        assert sensor.is_on == True and type(sensor.is_on) is bool
        fake_button.is_pressed = 0
        assert sensor.is_on == False and type(sensor.is_on) is bool
    
    def test_triggers_ON_ACTIVE_when_sensor_is_ACTIVATED_once(self, fake_button, sensor):
        active_trigger = MagicMock()
        sensor.on_active = active_trigger
        fake_button.when_pressed()
        assert active_trigger.called

    def test_triggers_ON_INACTIVE_when_sensor_is_DEACTIVATED_once(self, fake_button, sensor):
        inactive_trigger = MagicMock()
        sensor.on_inactive = inactive_trigger
        fake_button.when_released()
        assert inactive_trigger.called

    def test_does_not_trigger_ON_ACTIVE_when_sensor_is_DEACTIVATED(self, fake_button, sensor):
        active_trigger = MagicMock()
        sensor.on_active = active_trigger
        fake_button.when_released()
        assert not active_trigger.called

    def test_does_not_trigger_ON_INACTIVE_when_sensor_is_ACTIVATED(self, fake_button, sensor):
        inactive_trigger = MagicMock()
        sensor.on_inactive = inactive_trigger
        fake_button.when_pressed()
        assert not inactive_trigger.called

    def test_triggers_appropriate_event_every_10_seconds(self, fake_button, fake_timer):
        with patch('piinput.main.Timer', new=fake_timer),\
                patch('piinput.main.Button', return_value=fake_button):
            fake_button.is_pressed = True
            mock_trigger = MagicMock()
            sensor = SensorAdaptor(5)
            sensor.on_active = mock_trigger
            assert mock_trigger.call_count == 0
            fake_timer.forward(seconds=20)
            assert mock_trigger.call_count == 2

    def test_using_adaptor_without_gpiozero_installed_throws_a_meaningful_exception(self):
        with pytest.raises(Exception) as e:
            SensorAdaptor(12)
        assert e.value.args[0] == 'This adaptor requires gpiozero library to be installed'

    def test_can_use_inverting_input(self, fake_button):
        with patch('piinput.main.Button', return_value=fake_button):
            sensor = SensorAdaptor(5, is_inverting=True)
            fake_button.is_pressed = True
            assert sensor.is_on == False
            fake_button.is_pressed = False
            assert sensor.is_on == True

# in gpiozero library a good pin reader is a button
# so we use button-like properties in this adaptor
@pytest.fixture
def fake_button():
    pin_reader = MagicMock()
    pin_reader.is_pressed = False
    pin_reader.when_pressed = MagicMock()
    pin_reader.when_released = MagicMock()
    yield pin_reader

@pytest.fixture
def sensor(fake_button):
    with patch('piinput.main.Button', return_value=fake_button):
        yield SensorAdaptor(5)

@pytest.fixture
def fake_timer():
    class FakeTimer:
        def __new__(cls, interval=0, function=lambda: None):
            cls.interval = interval
            cls.callback = function
            cls.__is_running = False
            return super(FakeTimer, cls).__new__(cls)
        @classmethod
        def start(cls):
            cls.__is_running = True
        @classmethod
        def cancel(cls):
            cls.__is_running = False
        @classmethod
        def forward(cls, seconds):
            if not cls.__is_running:
                raise Exception('Timer has to be running')
            while seconds >= cls.interval:
                cls.callback()
                seconds -= cls.interval
    return FakeTimer

@pytest.fixture
def patch_timer():
    with patch('piinput.main.Timer', new=MagicMock()):
        yield
