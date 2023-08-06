import struct
from datetime import datetime
from typing import Any

from fast_rpc.serialization.types import MethodCall, MethodResponse, FaultResponse
from fast_rpc.serialization.constants import ENDIAN


class FastRPCDecodeError(ValueError):
    pass


class View:
    """ To iterate over data we use special 'iterator' view object with variable moving size """
    def __init__(self, data: bytes):
        self._data = data
        self._offset = 0

    def __iter__(self):
        return self

    def __next__(self, size: int=1) -> bytes:
        if self._offset >= len(self._data):
            raise StopIteration()
        old_offset = self._offset
        self._offset += size
        return self._data[old_offset:self._offset]

    def next(self, size: int) -> bytes:
        return self.__next__(size)


def _get_data_type(i: bytes) -> int:
    return i[0] & 0b11111000


def _get_add_info(i: bytes) -> int:
    return i[0] & 0b00000111


class FastRPCDecoderV1:
    def __init__(self):
        self._decode_table = {
            0x08: self._decode_int,
            0x10: self._decode_bool,
            0x18: self._decode_float,
            0x20: self._decode_string,
            0x28: self._decode_datetime,
            0x30: self._decode_bytes,
            0x50: self._decode_dict,
            0x58: self._decode_array,
            0x68: self._decode_method_call,
            0x70: self._decode_method_response,
            0x78: self._decode_fault_response,
        }

    def decode(self, view: View) -> Any:
        i = next(view)
        type_ = _get_data_type(i)
        add_info = _get_add_info(i)

        if type_ not in self._decode_table:
            raise FastRPCDecodeError('Unrecognized object type: 0x{:02x}'.format(type_))

        return self._decode_table[type_](add_info, view)

    def _decode_int(self, add_info: int, view: View) -> int:
        """ Unsigned integer deserialization
        Bytes:       |         |        |        |        |        |
        value:        00001 xxx  data (1-4 octets)
        field name:  | Type|   | Data stored in little endian      |
                             Number of data octets
        """
        size = add_info + 1
        if size > 4:
            raise FastRPCDecodeError('Integer can be max 4 bytes long')

        return int.from_bytes(bytes=view.next(size=size), byteorder=ENDIAN)

    def _decode_bool(self, add_info: int, view: View) -> bool:
        """ Boolean deserialization
        Bytes:       |         |
        value:        00010 00x
        field name:  | Type|   |
                             Value is stored in least significant bit(x)
        """
        return bool(add_info)

    def _decode_float(self, add_info: int, view: View) -> float:
        """ Float serialisation
        Bytes:       |         |                                                      |
        value:        00011 000  data (8 octets)
        field name:  | Type|   | Floating point number in double precision(IEEE 754)  |
        """
        return struct.unpack('<d', view.next(8))[0]

    def _decode_string(self, add_info: int, view: View) -> str:
        """ String serialisation
        Bytes:       |         |        |        |        |        |                            |
        value:        00100 xxx     data-size (1-4 octets)           data (data-size octets)
        field name:  | Type|   | specifies length of data          | Utf-8, no null terminated, |
                             Length of data-size field               no escaping
        """
        size = add_info + 1
        data_size = int.from_bytes(view.next(size=size), byteorder=ENDIAN)
        if data_size == 0:
            return ''
        bytes_ = view.next(size=data_size)
        return bytes_.decode()

    def _decode_datetime(self, add_info: int, view: View) -> datetime:
        """ Datetime serialisation
        Bytes:       |        |        |        |        |        |        |         |          |         |          |     |
        value:        00101000                                              3b  6b      6b     5b     5b     4b   11b
        field name:  | type   | zone   |               timestamp           |   |  sec  | min  | hour | day  |    |    year |
                                                                             week day                         month
        """
        zone = next(view)  # TODO: implement
        timestamp = struct.unpack('<i', view.next(size=4))[0]
        return datetime.fromtimestamp(timestamp)  # we save some ops and simply use just timestamp

    def _decode_bytes(self, add_info: int, view: View) -> bytes:
        """ Serialize bytes(Binary)
        Bytes:       |         |        |        |        |        |                         |
        value:        00110 xxx      data-size (1-4 octets)          data (data-size octets)
        field name:  | Type|   |   Number of data octets           |   No encoded data       |
                             Length of data-size field
        """
        size = add_info + 1
        data_size = int.from_bytes(view.next(size=size), byteorder=ENDIAN)
        return view.next(size=data_size) if data_size > 0 else b''

    def _decode_dict(self, add_info: int, view: View) -> dict:
        """ Dict(Struct) serialisation
        Bytes:       |         |        |        |        |        |        |              |          |
        value:        01010 xxx      num-members (1-4 octets)                (1-255 octets)  DATATYPES
        field name:  | Type|   |  number of struct members         |        | Utf-8 name   |          |
                             Length of num-members field             name length
        DATATYPES - serialized items                               | num-members * structure above
        """
        size = add_info + 1
        num_of_members = int.from_bytes(view.next(size=size), byteorder=ENDIAN)
        o = {}
        for _ in range(num_of_members):
            try:
                key_size = int.from_bytes(next(view), byteorder=ENDIAN)
                key = view.next(size=key_size).decode()
                value = self.decode(view)
            except StopIteration:
                raise FastRPCDecodeError('Uncomplete data for structure deserialization')

            o[key] = value
        return o

    def _decode_array(self, add_info: int, view: View) -> list:
        """ Deserialize Array
        Bytes:       |         |        |        |        |        |           |
        value:        01011 xxx     num-items (1-4 octets)           DATATYPES
        field name:  | Type|   |    Number of array items          |           |
                             Length of num-items field             | num-items * structure above
        DATATYPES - serialized items
        """
        size = add_info + 1
        num_of_items = int.from_bytes(view.next(size=size), byteorder=ENDIAN)
        o = []
        for _ in range(num_of_items):
            item = self.decode(view)
            o.append(item)
        return o

    def _decode_method_call(self, add_info: int, view: View) -> MethodCall:
        """ Serialize method call non-data type object
        Bytes:       |        |        |               |            |
        value:        01101000           (1-255 octets)  PARAMETERS
        field name:  | Type   |        |  Utf-8 name   |            |
                                Name size
        """
        name_size = int.from_bytes(next(view), byteorder=ENDIAN)
        method_name = view.next(size=name_size).decode()
        params = []
        try:
            while True:
                o = self.decode(view)
                params.append(o)
        except StopIteration:
            pass

        return MethodCall(method_name, *params)

    def _decode_method_response(self, add_info: int, view: View) -> MethodResponse:
        """ Deserialize method response non-data type object
        Bytes:       |        |              |
        value:        01110000     VALUE
        field name:  | Type   | Return value |
        """
        try:
            value = self.decode(view)
        except StopIteration:
            value = MethodResponse.Empty()
        return MethodResponse(value)

    def _decode_fault_response(self, add_info: int, view: View) -> FaultResponse:
        """ Serialize fault response non-data type object
        Bytes:       |        |           |               |
        value:        01111000   INTEGER       STRING
        field name:  |  Type  | Fault Num | Fault message |
        """
        fault_number = self.decode(view)
        fault_message = self.decode(view)
        return FaultResponse(fault_number, fault_message)


class FastRPCDecoderV2(FastRPCDecoderV1):
    def __init__(self):
        super(FastRPCDecoderV2, self).__init__()
        del self._decode_table[0x08]  # remove unsupported v1 int
        self._decode_table.update({
            0x38: self._decode_positive_int,
            0x40: self._decode_negative_int,
        })

    def _decode_positive_int(self, add_info: int, view: View) -> int:
        """ Integer8 positive deserialization
        Bytes:       |          |        |        |        |        |        |        |        |        |
        value:        00111 xxx                          data (1-8 octets)
        field name:  | Type|   |            Data stored in little endian                                |
                             Number of data octets
        """
        size = add_info + 1
        if size > 8:
            raise FastRPCDecodeError('Integer can be max 8 bytes long')

        return int.from_bytes(bytes=view.next(size=size), byteorder=ENDIAN)

    def _decode_negative_int(self, add_info: int, view: View) -> int:
        """ Integer8 negative
        Bytes:       |          |        |        |        |        |        |        |        |        |
        value:        01000 xxx                          data (1-8 octets)
        field name:  | Type|   |            Data stored in little endian                                |
                             Number of data octets
        """
        return -self._decode_positive_int(add_info, view)


class FastRPCDecoderV3(FastRPCDecoderV2):
    def __init__(self):
        super(FastRPCDecoderV3, self).__init__()

        self._decode_table[0x08] = self._decode_int  # return of one int type

    @staticmethod
    def _unzigzag(number: int) -> int:
        """ ZigZag encoding uses LSB for sign storage,
        the value of the signed integer is shifted left by one bit,
        and bitwise negated in case of negative integers.
        """
        if number % 2:  # negative numbers are zigzagged as odd
            number = ~number  # don't forget to change sign ;)
        number >>= 1
        return number

    def _decode_int(self, add_info: int, view: View) -> int:
        """ Unsigned integer serialisation
        Bytes:       |         |        |        |        |        |
        value:        00001 xxx  data (1-4 octets)
        field name:  | Type|   |                                   |
                                   Data stored as ZigZag encoded unsigned integer in little endian
                             Number of data octets
        """
        size = add_info + 1
        if size > 8:
            raise FastRPCDecodeError('Integer can be max 8 bytes long')

        zigzagged_number = int.from_bytes(bytes=view.next(size=size), byteorder=ENDIAN)
        return self._unzigzag(zigzagged_number)


def get_deserializer(version: int) -> FastRPCDecoderV1:
    """ Return deserializer instance for protocol version """
    deserializers = {
        1: FastRPCDecoderV1,
        2: FastRPCDecoderV2,
        3: FastRPCDecoderV3
    }

    if version not in deserializers:
        raise ValueError('Unsupported protocol version')

    return deserializers[version]()


def decode(data: bytes, *, version: int = 1) -> Any:
    """ Decode fastrpc encoded data to python obj """
    view = View(data)
    if data.startswith(b'\xca\x11'):
        view.next(size=2)
        # TODO here we can get serializer version
        view.next(size=2)
    deserializer = get_deserializer(version)

    return deserializer.decode(view)
