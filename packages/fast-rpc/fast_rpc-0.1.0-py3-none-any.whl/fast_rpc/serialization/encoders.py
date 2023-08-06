import struct
from collections.abc import Iterable
from datetime import datetime
from typing import Any, Dict, Callable

from fast_rpc.serialization.types import MethodCall, MethodResponse, FaultResponse
from fast_rpc.serialization.constants import ENDIAN, YEAR_OFFSET


class FastRPCEncodeError(Exception):
    pass


def get_mem_size_bytes(num: int) -> int:
    """ Compute memory size of bytes taken by integer """
    return 1 if num == 0 else (num.bit_length() + 7) // 8


class FastRPCEncoderV1:
    _version = 1

    @property
    def _magic(self) -> bytes:
        return b'\xca\x11\x01\x00'

    def __init__(self):
        self._encode_table: Dict[Any, Callable] = {
            int: self._encode_int,
            bool: self._encode_bool,
            float: self._encode_float,
            str: self._encode_str,
            datetime: self._encode_datetime,
            bytes: self._encode_bytes,
            dict: self._encode_struct,
            tuple: self._encode_array,
            list: self._encode_array,
            Iterable: self._encode_array,
            MethodCall: self._encode_method_call,
            MethodResponse: self._encode_method_response,
            FaultResponse: self._encode_fault_response
        }

    def encode(self, o: Any) -> bytes:
        """ Default function called for all unknown functions
        First byte of all fastrpc serialized objects is divided to two sections:
            +-----+---+
            |  5b | 3b|
            +-----+---+
            Type  Add

        Type: code of serialized object type
        Add: additional info, usualy number of octets contain user data (for v1: 0-4 means 1-4 octets)
        """
        type_ = type(o)
        method = self._encode_table.get(type_)

        # second chance to hit function
        if method is None:
            for type_ in self._encode_table:
                if isinstance(o, type_):
                    method = self._encode_table[type_]
                    break

        if method is None:
            raise FastRPCEncodeError("Object of type '{}' is not FastRPC serializable".format(type(o)))
        return method(o)

    @staticmethod
    def _encode_int(number: int) -> bytes:
        """ Unsigned integer serialisation
        Bytes:       |         |        |        |        |        |
        value:        00001 xxx  data (1-4 octets)
        field name:  | Type|   | Data stored in little endian      |
                             Number of data octets
        """
        type_ = 0b00001000  # 0x08
        mem_size_bytes = get_mem_size_bytes(number)
        code_size_bytes = mem_size_bytes - 1  # in fast-rpc protocol 0b000 add mean 1 B of data
        type_add = type_ ^ code_size_bytes
        return type_add.to_bytes(length=1, byteorder=ENDIAN) + \
            number.to_bytes(length=mem_size_bytes, byteorder=ENDIAN)

    @staticmethod
    def _encode_bool(boolean: bool) -> bytes:
        """ Boolean serialisation
        Bytes:       |         |
        value:        00010 00x
        field name:  | Type|   |
                             Value is stored in least significant bit(x)
        """
        type_ = 0b00010000  # 0x10
        type_add = type_ | boolean
        return type_add.to_bytes(length=1, byteorder=ENDIAN)

    @staticmethod
    def _encode_float(number: float) -> bytes:
        """ Float serialisation
        Bytes:       |         |                                                      |
        value:        00011 000  data (8 octets)
        field name:  | Type|   | Floating point number in double precision(IEEE 754)  |
        """
        type_add = 0b00011000  # 0x18
        return type_add.to_bytes(length=1, byteorder=ENDIAN) + struct.pack('<d', number)

    @staticmethod
    def _encode_str(s: str) -> bytes:
        """ String serialisation
        Bytes:       |         |        |        |        |        |                            |
        value:        00100 xxx     data-size (1-4 octets)           data (data-size octets)
        field name:  | Type|   | specifies length of data          | Utf-8, no null terminated, |
                             Length of data-size field               no escaping
        """
        type_ = 0b00100000  # 0x20
        encoded = s.encode()
        mem_size_bytes = get_mem_size_bytes(len(encoded))
        code_size_bytes = mem_size_bytes - 1  # in fast-rpc protocol 0b000 add mean 1 B of data
        type_add = type_ ^ code_size_bytes

        return type_add.to_bytes(length=1, byteorder=ENDIAN) + \
            len(encoded).to_bytes(length=mem_size_bytes, byteorder=ENDIAN) + \
            encoded

    @staticmethod
    def _encode_datetime(d: datetime) -> bytes:
        """ Datetime serialisation
        Bytes:       |        |        |        |        |        |        |         |          |         |          |     |
        value:        00101000                                              3b  6b      6b     5b     5b     4b   11b
        field name:  | type   | zone   |               timestamp           |   |  sec  | min  | hour | day  |    |    year |
                                                                             week day                         month
        """
        type_add = 0b00101000  # 0x28
        zone = 0x00  # TODO implement
        timestamp = int(d.timestamp())
        weekday = (d.weekday()) % 6  # fast-rpc week start with sunday, not monday ( WTF! )
        encoded_date_time = weekday
        encoded_date_time |= (d.second << 3)
        encoded_date_time |= (d.minute << 9)
        encoded_date_time |= (d.hour << 15)
        encoded_date_time |= (d.day << 20)
        encoded_date_time |= (d.month << 25)
        encoded_date_time |= ((d.year - YEAR_OFFSET) << 29)

        # TODO not sure about zone endian, spec is not exact about this
        return type_add.to_bytes(length=1, byteorder=ENDIAN) + \
            zone.to_bytes(length=1, byteorder=ENDIAN) + \
            struct.pack('<i', timestamp) + \
            encoded_date_time.to_bytes(length=5, byteorder=ENDIAN)

    @staticmethod
    def _encode_bytes(o: bytes) -> bytes:
        """ Serialize bytes(Binary)
        Bytes:       |         |        |        |        |        |                         |
        value:        00110 xxx      data-size (1-4 octets)          data (data-size octets)
        field name:  | Type|   |   Number of data octets           |   No encoded data       |
                             Length of data-size field
        """
        type_ = 0b00110000  # 0x30
        mem_size_bytes = get_mem_size_bytes(len(o))
        code_size_bytes = mem_size_bytes - 1
        type_add = type_ | code_size_bytes

        return type_add.to_bytes(length=1, byteorder=ENDIAN) + \
            len(o).to_bytes(length=mem_size_bytes, byteorder=ENDIAN) + o

    def _encode_struct(self, o: Dict[Any, Any]) -> bytes:
        """ Dict(Struct) serialisation
        Bytes:       |         |        |        |        |        |        |              |          |
        value:        01010 xxx      num-members (1-4 octets)                (1-255 octets)  DATATYPES
        field name:  | Type|   |  number of struct members         |        | Utf-8 name   |          |
                             Length of num-members field             name length
        DATATYPES - serialized items                               | num-members * structure above
        """
        type_ = 0b01010000  # 0x50

        # first we get struct size metainfo and meta_metainfo for storing metainfo ;D
        mem_size_bytes = get_mem_size_bytes(len(o))
        code_size_bytes = mem_size_bytes - 1
        type_add = type_ | code_size_bytes

        encoded = type_add.to_bytes(length=1, byteorder=ENDIAN) + \
            len(o).to_bytes(length=mem_size_bytes, byteorder=ENDIAN)

        for key, value in o.items():
            if key is None:
                raise TypeError("Key in Dictionary must be a string.")
            encoded_key = str(key).encode()
            if len(encoded_key) == 0:
                raise TypeError("Lenght of member name is 0 not in interval (1-255)")
            encoded += len(encoded_key).to_bytes(length=1, byteorder=ENDIAN) + encoded_key + self.encode(value)

        return encoded

    def _encode_array(self, o: Iterable) -> bytes:
        """ Serialize Iterable(Array)
        Bytes:       |         |        |        |        |        |           |
        value:        01011 xxx     num-items (1-4 octets)           DATATYPES
        field name:  | Type|   |    Number of array items          |           |
                             Length of num-items field             | num-items * structure above
        DATATYPES - serialized items
        """
        type_ = 0b01011000  # 0x58
        o = tuple(o)
        mem_size_bytes = get_mem_size_bytes(len(o))
        code_size_bytes = mem_size_bytes - 1
        type_add = type_ | code_size_bytes

        encoded = type_add.to_bytes(length=1, byteorder=ENDIAN) + \
            len(o).to_bytes(length=mem_size_bytes, byteorder=ENDIAN)

        for i in o:
            encoded += self.encode(i)

        return encoded

    def _encode_method_call(self, o: MethodCall) -> bytes:
        """ Serialize method call non-data type object
        Bytes:       |        |        |               |            |
        value:        01101000           (1-255 octets)  PARAMETERS
        field name:  | Type   |        |  Utf-8 name   |            |
                                Name size
        """
        type_ = 0b01101000  # 0x68
        encoded_method_name = str(o.method_name).encode()

        if len(encoded_method_name) > 255 or len(encoded_method_name) == 0:
            raise ValueError('Method name is not in interval (1-255)')

        encoded = self._magic + \
            type_.to_bytes(length=1, byteorder=ENDIAN) + \
            len(encoded_method_name).to_bytes(length=1, byteorder=ENDIAN) + \
            encoded_method_name

        for param in o.params:
            encoded += self.encode(param)

        return encoded

    def _encode_method_response(self, o: MethodResponse) -> bytes:
        """ Serialize method response non-data type object
        Bytes:       |        |              |
        value:        01110000     VALUE
        field name:  | Type   | Return value |
        """
        type_ = 0b01110000  # 0x70
        encoded = self._magic + type_.to_bytes(length=1, byteorder=ENDIAN)
        if not isinstance(o.value, MethodResponse.Empty):
            encoded += self.encode(o.value)

        return encoded

    def _encode_fault_response(self, o: FaultResponse) -> bytes:
        """ Serialize fault response non-data type object
        Bytes:       |        |           |               |
        value:        01111000   INTEGER       STRING
        field name:  |  Type  | Fault Num | Fault message |
        """
        type_ = 0b01111000  # 0x78
        encoded = self._magic + \
            type_.to_bytes(length=1, byteorder=ENDIAN) + \
            self.encode(o.fault_number) + \
            self.encode(o.fault_message)

        return encoded


class FastRPCEncoderV2(FastRPCEncoderV1):
    _version = 2

    @property
    def _magic(self) -> bytes:
        return b'\xca\x11\x02\x00'

    def __init__(self):
        super(FastRPCEncoderV2, self).__init__()

        # update table with new type
        self._encode_table[type(None)] = self._encode_null

    @staticmethod
    def _encode_int(number: int) -> bytes:
        """ Integer serialisation
        Integer8 positive
        Bytes:       |          |        |        |        |        |        |        |        |        |
        value:        00111 xxx                          data (1-8 octets)
        field name:  | Type|   |            Data stored in little endian                                |
                             Number of data octets

        Integer8 negative
        Bytes:       |          |        |        |        |        |        |        |        |        |
        value:        01000 xxx                          data (1-8 octets)
        field name:  | Type|   |            Data stored in little endian                                |
                             Number of data octets
        """
        type_ = 0b01000000 if number < 0 else 0b00111000  # 0x40 0x38
        mem_size_bytes = get_mem_size_bytes(number)
        code_size_bytes = mem_size_bytes - 1
        type_add = type_ ^ code_size_bytes
        return type_add.to_bytes(length=1, byteorder=ENDIAN) + \
            abs(number).to_bytes(length=mem_size_bytes, byteorder=ENDIAN)

    @staticmethod
    def _encode_null(o: None) -> bytes:
        """ Serialize None object
        Bytes:       |        |
        value:        01100000
        field name:  |  Type  |
        """
        return 0b01100000.to_bytes(length=1, byteorder=ENDIAN)


class FastRPCEncoderV3(FastRPCEncoderV2):
    _version = 3

    @property
    def _magic(self) -> bytes:
        return b'\xca\x11\x03\x00'

    def __init__(self):
        super(FastRPCEncoderV3, self).__init__()

    @staticmethod
    def _zigzag(number: int) -> int:
        """ ZigZag encoding uses LSB for sign storage,
        the value of the signed integer is shifted left by one bit,
        and bitwise negated in case of negative integers.
        """
        number <<= 1
        return ~number if number < 0 else number

    def _encode_int(self, number: int) -> bytes:
        """ Unsigned integer serialisation
        Bytes:       |         |        |        |        |        |
        value:        00001 xxx  data (1-4 octets)
        field name:  | Type|   |                                   |
                                   Data stored as ZigZag encoded unsigned integer in little endian
                             Number of data octets
        """
        type_ = 0b00001000  # 0x08
        number = self._zigzag(number)
        mem_size_bytes = get_mem_size_bytes(number)
        code_size_bytes = mem_size_bytes - 1  # in fast-rpc protocol 0b000 add mean 1 B of data
        type_add = type_ ^ code_size_bytes
        return type_add.to_bytes(length=1, byteorder=ENDIAN) + \
            number.to_bytes(length=mem_size_bytes, byteorder=ENDIAN)

    @staticmethod
    def _encode_datetime(d: datetime) -> bytes:
        """ Datetime serialisation
        Bytes:       |        |        |        |        |        |        |        |        |        |        |         |          |         |          |     |
        value:        00101000                                                                                   3b  6b      6b     5b     5b     4b   11b
        field name:  | type   | zone   |               timestamp (64b)                                         |   |  sec  | min  | hour | day  |    |    year |
                                                                                                                 week day                         month
        """
        type_add = 0b00101000  # 0x28
        zone = 0x00  # TODO implement
        timestamp = int(d.timestamp())
        weekday = (d.weekday()) % 6  # fast-rpc week start with sunday, not monday ( WTF! )
        encoded_date_time = weekday
        encoded_date_time |= (d.second << 3)
        encoded_date_time |= (d.minute << 9)
        encoded_date_time |= (d.hour << 15)
        encoded_date_time |= (d.day << 20)
        encoded_date_time |= (d.month << 25)
        encoded_date_time |= ((d.year - YEAR_OFFSET) << 29)

        # TODO not sure about zone endian, spec is not exact about this
        return type_add.to_bytes(length=1, byteorder=ENDIAN) + \
            zone.to_bytes(length=1, byteorder=ENDIAN) + \
            struct.pack('<Q', timestamp) + \
            encoded_date_time.to_bytes(length=5, byteorder=ENDIAN)


def get_serializer(version: int) -> FastRPCEncoderV1:
    """ Return serializer instance for protocol version """
    serializers = {
        1: FastRPCEncoderV1,
        2: FastRPCEncoderV2,
        3: FastRPCEncoderV3
    }

    if version not in serializers:
        raise ValueError('Unsupported protocol version')
    return serializers[version]()


def encode(obj: Any, *, version: int = 1) -> bytes:
    """ Encode obj to FastRPC binary format """
    # we store used protocol version
    serializer = get_serializer(version)

    return serializer.encode(obj)
