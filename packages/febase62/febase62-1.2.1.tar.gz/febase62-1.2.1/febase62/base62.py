__version__ = '1.2.1'
import sys
from febase62.charset import base62


class Base62:
    """
    Encoder and decoder for Base62 integers.
    """

    def __init__(self, charset=base62):
        """
        Constructor.

        :param charset: Definition of charset. Defaults to base62.
        """
        self.charset = charset

    def encode(self, number):
        """
        Encode a number to base62 format.
        :param number:
        :return:
        >>> b = Base62()
        >>> b.encode(34441886726)
        'base62'
        >>> b.encode(1337)
        'LZ'
        >>> b = Base62('01')
        >>> b.encode(4)
        '100'
        """
        # Check if the number is provided as byte object.
        if isinstance(number, bytes):
            # Convert byte object to integer.
            number = int.from_bytes(number, sys.byteorder)

        if number == 0:
            return '0'
        s = list()
        while number > 0:
            n = number % len(self.charset)
            s.append(self.charset[n])
            number //= len(self.charset)
        s.reverse()
        return ''.join(s)

    def decode(self, text):
        """
        Decode a base62 string to an integer.
        :param text:
        :return:
        >>> b = Base62()
        >>> b.decode("base62")
        34441886726
        >>> b.decode('LZ')
        1337
        >>> b = Base62('01')
        >>> b.decode('100')
        4
        """
        result = 0
        for i in range(0, len(text)):
            result += self.charset.index(text[i]) * len(self.charset) ** (len(text) - 1 - i)
        return result
