import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from piinput import SensorAdaptor

class TestPiInputAdaptor:

    def test_assigns_correct_pin_number(self):
        fake_button_constructor = MagicMock()
        pin_number = 1583
        with patch('piinput.main.Button', new=fake_button_constructor):
            SensorAdaptor(pin_number)
            assert fake_button_constructor.call_args.args[0] == pin_number

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

    def test_triggers_ON_DEACTIVE_when_sensor_is_DEACTIVATED_once(self, fake_button, sensor):
        deactive_trigger = MagicMock()
        sensor.on_deactive = deactive_trigger
        fake_button.when_released()
        assert deactive_trigger.called

    def test_does_not_trigger_ON_ACTIVE_when_sensor_is_DEACTIVATED(self, fake_button, sensor):
        active_trigger = MagicMock()
        sensor.on_active = active_trigger
        fake_button.when_released()
        assert not active_trigger.called

    def test_does_not_trigger_ON_DEACTIVE_when_sensor_is_ACTIVATED(self, fake_button, sensor):
        deactive_trigger = MagicMock()
        sensor.on_deactive = deactive_trigger
        fake_button.when_pressed()
        assert not deactive_trigger.called
    
    def test_using_adaptor_without_gpiozero_installed_throws_a_meaningful_exception(self):
        with pytest.raises(Exception) as e:
            SensorAdaptor(12)
        assert e.value.args[0] == 'This adaptor requires gpiozero library to be installed'

    def test_can_use_inverting_input(self):
        fake_button_constructor = MagicMock()
        with patch('piinput.main.Button', new=fake_button_constructor):
            SensorAdaptor(5, is_inverting=True)
            assert fake_button_constructor.call_args.kwargs.get('active_state') == False

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
    with patch('piinput.main.Button', new=lambda *a, **kw: fake_button):
        yield SensorAdaptor(5)
