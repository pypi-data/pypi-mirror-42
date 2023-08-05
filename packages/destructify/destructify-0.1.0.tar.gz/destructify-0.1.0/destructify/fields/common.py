import io

from . import Field, StreamExhaustedError, Substream, ParsingContext, NOT_PROVIDED
from ..exceptions import DefinitionError, WriteError
from .base import _retrieve_property


class FixedLengthField(Field):
    """Field with a fixed length. It reads exactly the amount of bytes as specified in the length attribute.
    """

    def __init__(self, length, *args, strict=True, padding=None, **kwargs):
        self.length = length
        self.strict = strict
        self.padding = padding
        super().__init__(*args, **kwargs)

    def __len__(self):
        if isinstance(self.length, int):
            return self.length
        else:
            return super().__len__()

    @property
    def ctype(self):
        if self._ctype:
            return "{} {}".format(self._ctype, self.name)
        else:
            return "{} {}[{}]".format(self.__class__.__name__, self.name, "" if callable(self.length) else self.length)

    def initialize(self):
        """Overrides the content of the length field if possible."""

        if isinstance(self.length, str):
            related_field = self.bound_structure._meta.get_field_by_name(self.length)
            if not related_field.has_override:
                related_field.override = lambda s, v: len(s[self.name]) if v is None else v

    def get_length(self, context):
        return _retrieve_property(context, self.length)

    def from_stream(self, stream, context=None):
        length = self.get_length(context)
        read = context.read_stream(stream, length)
        if len(read) < length and self.strict:
            raise StreamExhaustedError("Could not parse field %s, trying to read %s bytes, but only %s read." %
                                       (self.full_name, length, len(read)))

        # Remove padding
        value = read
        if self.padding is not None:
            while value[-len(self.padding):] == self.padding:
                value = value[:-len(self.padding)]

        return self.from_bytes(value), len(read)

    def to_stream(self, stream, value, context=None):
        length = self.get_length(context)

        if length < 0:
            # For negative lengths, we just write to the stream
            return super().to_stream(stream, value, context)

        val = self.to_bytes(value)

        if len(val) < length:
            if self.padding is not None:
                remaining = length - len(val)

                if self.strict and remaining % len(self.padding) != 0:
                    raise WriteError("The field %s must be padded, but the remaining bytes %d are not a multiple of %d." %
                                     (self.full_name, remaining, len(self.padding)))

                # slicing for paddings longer than 1 byte
                val = (val + self.padding * remaining)[:length]
            elif self.strict:
                raise WriteError("The contents of %s are %d long, but expecting %d." %
                                 (self.full_name, len(val), length))
        elif len(val) > length:
            if self.strict:
                raise WriteError("The contents of %s are %d long, but expecting %d." %
                                 (self.full_name, len(val), length))

            val = val[:length]

        return context.write_stream(stream, val)


class BitField(FixedLengthField):
    """A subclass of :class:`FixedLengthField`, but does not use bytes as the basis, but bits. The field writes and
    reads integers.
    """

    def __init__(self, length, *args, realign=False, **kwargs):
        self.realign = realign
        super().__init__(length, *args, **kwargs)

    def __len__(self):
        if isinstance(self.length, int):
            return self.length / 8
        else:
            return super().__len__()

    @property
    def ctype(self):
        if self._ctype:
            return "{} {}".format(self._ctype, self.name)
        else:
            return "{} {}[{}]".format(self.__class__.__name__, self.name,
                                      "" if callable(self.length) else "{} bits".format(self.length))

    def initialize(self):
        """Overrides the content of the length field if possible."""

        if isinstance(self.length, str):
            related_field = self.bound_structure._meta.get_field_by_name(self.length)
            if not related_field.has_override:
                related_field.override = lambda s, v: s[self.name].bit_length() if v is None else v

    def from_stream(self, stream, context=None):
        result = context.read_stream_bits(stream, self.get_length(context))
        if self.realign:
            context.bits_remaining = None
        return result

    def to_stream(self, stream, value, context=None):
        return context.write_stream_bits(stream, value, self.get_length(context), force_write=self.realign)


class TerminatedField(Field):
    """A field that reads until the :attr:`TerminatedField.terminator` is hit. It directly returns the bytes as read,
     without the terminator.
    """

    def __init__(self, terminator=b'\0', *args, step=1, **kwargs):
        self.terminator = terminator
        self.step = step
        super().__init__(*args, **kwargs)

    def from_stream(self, stream, context=None):
        length = 0
        read = b""
        while True:
            c = context.read_stream(stream, self.step)
            if len(c) != self.step:
                raise StreamExhaustedError("Could not parse field %s; did not find terminator %s" %
                                           (self.name, self.terminator))
            read += c
            length += self.step
            if read.endswith(self.terminator):
                break

        return self.from_bytes(read[:-len(self.terminator)]), length

    def to_bytes(self, value):
        return value + self.terminator


class StringFieldMixin:
    def __init__(self, *args, encoding='utf-8', errors='strict', **kwargs):
        self.encoding = encoding
        self.errors = errors
        super().__init__(*args, **kwargs)

    def from_bytes(self, value):
        return super().from_bytes(value).decode(self.encoding, self.errors)

    def to_bytes(self, value):
        return super().to_bytes(value.encode(self.encoding, self.errors))


class FixedLengthStringField(StringFieldMixin, FixedLengthField):
    pass


class TerminatedStringField(StringFieldMixin, TerminatedField):
    pass


class IntegerField(FixedLengthField):
    def __init__(self, length, byte_order=None, *args, signed=False, **kwargs):
        self.byte_order = byte_order
        self.signed = signed
        super().__init__(length=length, *args, **kwargs)

    def from_bytes(self, value):
        val = super().from_bytes(value)
        return int.from_bytes(val,
                              byteorder='big' if not self.byte_order and len(val) == 1 else self.byte_order,
                              signed=self.signed)

    def to_stream(self, stream, value, context=None):
        # We can't use to_bytes here as we need the field's length.
        length = self.get_length(context)
        val = self.to_bytes(value.to_bytes(length,
                                           byteorder='big' if not self.byte_order and length == 1 else self.byte_order,
                                           signed=self.signed))
        return context.write_stream(stream, val)

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)

        # If byte_order is specified in the meta of the structure, we change our own default byte order (if not set)
        if self.bound_structure._meta.byte_order and not self.byte_order:
            self.byte_order = self.bound_structure._meta.byte_order

        if self.byte_order is None:
            if not isinstance(self.length, int) or not self.length == 1:
                raise DefinitionError("No byte_order for %s provided" % self.full_name)


class StructureField(Field):
    """A field that contains a :class:`Structure` in itself. If a default is not defined on the field, the default
    is an empty structure.
    """

    def __init__(self, structure, *args, length=None, **kwargs):
        self.structure = structure
        self.length = length

        super().__init__(*args, **kwargs)

        if not self.has_default:
            self.default = lambda: self.structure()

    def __len__(self):
        if isinstance(self.length, int):
            return self.length
        else:
            return len(self.structure)

    @property
    def ctype(self):
        ctype = self._ctype or self.structure._meta.object_name
        return "{} {}".format(ctype, self.name)

    def get_length(self, context):
        return _retrieve_property(context, self.length)

    def from_stream(self, stream, context):
        length = None
        if self.length is not None:
            length = self.get_length(context)

        with Substream(stream,
                       start=stream.tell(),
                       stop=stream.tell() + length if length is not None else None) as substream:
            res, consumed = self.structure.from_stream(substream, context=ParsingContext(parent=context))

        if length is not None and consumed < length:
            stream.seek(length - consumed, io.SEEK_CUR)
            consumed = length
        return res, consumed

    def to_stream(self, stream, value, context=None):
        if value is None:
            value = self.structure()
        return value.to_stream(stream)
