from abc import ABC, abstractmethod
class AbstractSensor(ABC):

    def __new__(cls, *a, **kw):
        # this is a hack because apparently python can't enforce setters
        props_requiring_setters = ['on_active', 'on_inactive']
        class_setters = [prop for prop, impl in vars(cls).items() 
                            if isinstance(impl, property) and impl.fset]
        for prop in props_requiring_setters:
            if prop not in class_setters:
                raise NotImplementedError(f'Must implement "{prop}" setter in order to use this interface')
        return super(AbstractSensor, cls).__new__(cls)
    
    @property
    def is_on(self):
        pass
    
    @property
    def on_active(self):
        pass
    
    @on_active.setter
    def on_active(self, callback):
        pass
    
    @property
    def on_inactive(self):
        pass
    
    @on_inactive.setter
    @abstractmethod
    def on_inactive(self, callback):
        pass
