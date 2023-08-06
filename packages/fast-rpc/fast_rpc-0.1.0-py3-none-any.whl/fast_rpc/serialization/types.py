from typing import Any


class MethodCall:
    def __init__(self, method_name, *params):
        self.method_name = method_name
        self.params = params

    def __eq__(self, other):
        return self.method_name == other.method_name and self.params == other.params


class MethodResponse:
    class Empty:
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, data: Any):
        if isinstance(data, (MethodCall, MethodResponse)):
            raise ValueError('Object {} can\'t be a response value'.format(type(data)))
        self._value = data

    def __init__(self, value: Any = Empty()):
        self._value = MethodResponse.Empty()
        self.value = value

    def __eq__(self, other):
        """ Two responses are equal if values are equal or both are empty """
        return self.value == other.value or (isinstance(self.value, MethodResponse.Empty) and isinstance(other.value, MethodResponse.Empty))


class FaultResponse:
    def __init__(self, fault_number: int, fault_message: str):
        self.fault_number = fault_number
        self.fault_message = fault_message

    def __eq__(self, other):
        return self.fault_number == other.fault_number and self.fault_message == other.fault_message
