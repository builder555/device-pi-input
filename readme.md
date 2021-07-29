### Pi Input adaptor

This package reads a specified pin and provides its status.

_Usage_

```python
from piinput import SensorAdaptor

# reading a value of a pin
sensor = SensorAdaptor(pin=3)
print(sensor.is_on)

# monitoring a pin
def activated():
    print('pin is activated')

def deactivated():
    print('pin is deactivated')

sensor.on_activate = activated
sensor.on_deactivate = deactivated
```