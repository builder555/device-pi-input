### Pi Input adaptor

This package reads a specified pin and provides its status.

_Installation_

```bash
$ PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
```

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

sensor.on_active = activated
sensor.on_inactive = deactivated
```

_Tests_

```bash
$ pipenv shell
$ pytest -v
```