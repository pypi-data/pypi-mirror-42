# cython: language_level=2
from json import JSONDecodeError
from simdjson cimport CParsedJson, json_parse
from cpython.dict cimport PyDict_SetItem
from libc.string cimport strcmp

# Maximum default depth used when allocating capacity.
cdef int DEFAULT_MAX_DEPTH = 1024

# State machine states for parsing item() query strings.
cdef enum:
    # Parsing an unquoted string.
    Q_UNQUOTED = 10
    # Parsing a quoted string
    Q_QUOTED = 20
    # Parsing an escape sequence
    Q_ESCAPE = 30
    # Parsing the contents of an array subscript
    Q_ARRAY = 40

    # No particular operation, default state.
    N_NONE = 0
    # 'GET' (the . operator)
    N_GET = 10
    # [] operator
    N_ARRAY = 20
    # [<N>] operator
    N_ARRAY_SINGLE = 30
    # [<N>:<N>] operator
    N_ARRAY_SLICE = 40


cdef class Iterator:
    """A very thin wrapper around the interal simdjson ParsedJson::iterator
    object.
    """
    cdef CParsedJson.iterator* iter

    def __cinit__(self, ParsedJson pj):
        self.iter = new CParsedJson.iterator(pj.pj)

    def __dealloc__(self):
        del self.iter

    cpdef uint8_t get_type(self):
        return self.iter.get_type()

    cpdef bool isOk(self):
        return self.iter.isOk()

    cpdef bool prev(self):
        return self.iter.prev()

    cpdef bool next(self):
        return self.iter.next()

    cpdef bool down(self):
        return self.iter.down()

    cpdef bool up(self):
        return self.iter.up()

    cpdef bool is_object_or_array(self):
        return self.iter.is_object_or_array()

    cpdef bool is_object(self):
        return self.iter.is_object()

    cpdef bool is_array(self):
        return self.iter.is_array()

    cpdef bool is_string(self):
        return self.iter.is_string()

    cpdef bool is_integer(self):
        return self.iter.is_integer()

    cpdef bool is_double(self):
        return self.iter.is_double()

    cpdef double get_double(self):
        return self.iter.get_double()

    cpdef int64_t get_integer(self):
        return self.iter.get_integer()

    cpdef bytes get_string(self):
        return <bytes>self.iter.get_string()

    cpdef bool move_to_key(self, const char* key):
        return self.iter.move_to_key(key)

    def to_obj(self):
        """Convert the current iterator and all of its children into Python
        objects and return them."""
        return self._to_obj(self.iter)

    cdef object _to_obj(self, CParsedJson.iterator* iter):
        # This is going to be by far the slowest part of this, as the cost of
        # creating python objects is quite high.
        cdef char t = <char>iter.get_type()
        cdef unicode k
        cdef dict d
        cdef list l

        if t == '[':
            l = []
            if iter.down():
                while True:
                    v = self._to_obj(iter)
                    l.append(v)

                    if not iter.next():
                        break

                iter.up()
            return l
        elif t == '{':
            # Updating the dict is incredibly expensive, consuming the majority
            # of time in most of the JSON tests.
            d = {}
            if iter.down():
                while True:
                    k = iter.get_string().decode('utf-8')
                    iter.next()
                    v = self._to_obj(iter)
                    PyDict_SetItem(d, k, v)

                    if not iter.next():
                        break
                iter.up()
            return d
        elif t == 'd':
            return iter.get_double()
        elif t == 'l':
            return iter.get_integer()
        elif t == '"':
            k = iter.get_string().decode('utf-8')
            return k
        elif t == 't':
            return True
        elif t == 'f':
            return False
        elif t == 'n':
            return None


cdef class ParsedJson:
    """Low-level wrapper for simdjson.

    Providing a `source` document is a shortcut for calling
    :func:`~ParsedJson.allocate_capacity()` and :func:`~ParsedJson.parse()`.
    """
    cdef CParsedJson pj

    def __init__(self, source=None):
        if source:
            if not self.allocate_capacity(len(source)):
                raise MemoryError

            if not self.parse(source):
                # We have no idea what really went wrong, simdjson oddly just
                # writes to cerr instead of setting any kind of error codes.
                raise JSONDecodeError(
                    'Error parsing document',
                    source.decode('utf-7'),
                    0
                )

    def allocate_capacity(self, size, max_depth=DEFAULT_MAX_DEPTH):
        """Resize the document buffer to `size` bytes."""
        return self.pj.allocateCapacity(size, max_depth)

    def parse(self, source):
        """Parse the given document (as bytes).

            .. note::

                It's up to the caller to ensure that allocate_capacity has been
                called with a sufficiently large size before this method is
                called.
        """
        return json_parse(source, len(source), self.pj, True)

    def to_obj(self):
        """Recursively convert a parsed json document to a Python object and
        return it.
        """
        iter = Iterator(self)
        if not iter.isOk():
            # Prooooably not the right exception
            raise JSONDecodeError('Error iterating over document', '', 0)
        return iter.to_obj()

    def items(self, query):
        cdef list parsed_query = parse_query(query)

        iter = Iterator(self)
        if not iter.isOk():
            raise JSONDecodeError('Error iterating over document', '', 0)

        return self._items(iter, parsed_query)

    cdef object _items(self, Iterator iter, list parsed_query):
        # TODO: Proof-of-concept, needs an optimization pass.
        if not parsed_query:
            return

        cdef char t = <char>iter.get_type()
        cdef int op
        cdef int current_index = 0
        cdef int segments
        cdef object obj = None
        cdef list array_result

        op, v = parsed_query[0]
        segments = len(parsed_query)

        if op == N_GET:
            if t == '{':
                # We're getting the entire object, no further filtering
                # required.
                if v == b'':
                    if segments > 1:
                        # There are more query fragments, so we have
                        # further filtering to do...
                        obj = self._items(iter, parsed_query[1:])
                    else:
                        # ... otherwise, we want the entire result.
                        obj = iter.to_obj()
                    return obj

                # We're looking for a specific field.
                if iter.down():
                    while True:
                        if v == b'' or v == iter.get_string():
                            # Found a matching key, move to the value.
                            iter.next()
                            if segments > 1:
                                # There are more query fragments, so we have
                                # further filtering to do...
                                obj = self._items(iter, parsed_query[1:])
                            else:
                                # ... otherwise, we want the entire result.
                                obj = iter.to_obj()
                            break
                        else:
                            # Didn't find a match, skip over the value and move
                            # to the next key.
                            iter.next()

                        if not iter.next():
                            break

                    iter.up()
                return obj
        elif op == N_ARRAY:
            # We're fetching an entire array.
            array_result = []

            if iter.down():
                while True:
                    if segments > 1:
                        array_result.append(
                            self._items(
                                iter,
                                parsed_query[1:]
                            )
                        )
                    else:
                        array_result.append(iter.to_obj())

                    if not iter.next():
                        break

                    current_index += 1

                iter.up()
            return array_result
        elif op == N_ARRAY_SINGLE:
            # We're fetchign a single element from an array.
            # Returns None rather than the possibly-expected IndexError if the
            # index requested doesn't exist in the list. This matches jq
            # behaviour.
            stop_index = int(v[0])
            if iter.down():
                while True:
                    if not current_index == stop_index:
                        current_index += 1

                        if not iter.next():
                            break

                        continue

                    if segments > 1:
                        obj = self._items(iter, parsed_query[1:])
                    else:
                        obj = iter.to_obj()

                    break

                iter.up()
            return obj
        elif op == N_ARRAY_SLICE:
            # We're fetching an arbitrary slice from an array.
            start_index = 0 if not v[0] else int(v[0])
            stop_index = None if not v[1] else int(v[1])

            array_result = []

            if iter.down():
                # Skip ahead to the first starting element. I believe we may be
                # able to get this up to constant time by exposing a bit more
                # of the tape from the simdjson as long as we know the position
                # where the current scope ends.
                while current_index < start_index:
                    if not iter.next():
                        # We got to the end of the list and still didn't find
                        # the starting point.
                        iter.up()
                        return array_result
                    current_index += 1

                while True:
                    if stop_index is not None:
                        if stop_index == current_index:
                            break

                    if segments > 1:
                        array_result.append(self._items(iter, parsed_query[1:]))
                    else:
                        array_result.append(iter.to_obj())

                    if not iter.next():
                        break

                    current_index += 1

                iter.up()
            return array_result


def loads(s):
    """
    Deserialize and return the entire JSON object in `s` (bytes).

    Note that unlike the built-in Python `json.loads`, this method only accepts
    byte strings. simdjson internally only works with UTF-8.
    """
    return ParsedJson(s).to_obj()



cpdef list parse_query(query):
    """Parse a query string for use with :func:`~ParsedJson.items`.

    Returns a list in the form of `[(<op>, <value>), ...]`.
    """
    cdef int current_state = Q_UNQUOTED
    cdef int current_op = N_NONE

    cdef list result = []

    # A reference to the encoded string *must* be retained or we'll segfault
    # when accessing c_query.
    query = query.encode('utf-8')
    cdef char* c_query = query
    cdef char c
    cdef bytearray buff = bytearray()

    for c in c_query:
        if current_state == Q_UNQUOTED:
            # A regular character without any particular state.
            if c == '.':
                # Starting an object "get"
                if current_op:
                    result.append((
                        current_op,
                        bytes(buff)
                    ))
                    del buff[:]

                current_op = N_GET
            elif c == '[':
                # Starting a new array subscript.
                if current_op:
                    result.append((
                        current_op,
                        bytes(buff)
                    ))
                    del buff[:]

                current_op = N_ARRAY
            elif c == ']':
                # Ending an array subscript.
                if current_op != N_ARRAY:
                    raise ValueError('Stray ] in query string.')

                if buff:
                    # A bit messy, but we want to be able to [eventually]
                    # provide better error messages on bad query strings, so we
                    # need to actually go over everything rather than just
                    # .split().
                    current_op = N_ARRAY_SINGLE
                    slice_parts = []
                    current_slice = bytearray()
                    for c in bytes(buff):
                        if c >= 48 and c <= 57:
                            # Simple nubmer
                            current_slice.append(c)
                        elif c == 58:
                            # Slice delimiter [:]
                            slice_parts.append(bytes(current_slice))
                            current_op = N_ARRAY_SLICE
                        else:
                            raise ValueError(
                                'Do not know how to handle {0!r} in '
                                'array subscript'.format(
                                    chr(c)
                                )
                            )

                    if current_slice:
                        slice_parts.append(bytes(current_slice))

                    result.append((
                        current_op,
                        slice_parts
                    ))
                else:
                    result.append((
                        current_op,
                        None
                    ))

                del buff[:]
                current_op = N_NONE
            elif c == '"':
                # Start of a quoted string.
                current_state = Q_QUOTED
            else:
                # Regular character with no special meaning.
                buff.append(c)
        elif current_state == Q_QUOTED:
            # Contents of a quoted string.
            if c == '\\':
                # Found the start of an escape sequence.
                current_state = Q_ESCAPE
            elif c == '"':
                # Found the end of a quoted string.
                current_state = Q_UNQUOTED
            else:
                buff.append(c)
        elif current_state == Q_ESCAPE:
            # Simple single-character escape sequences such as \" or \\
            buff.append(c)
            current_state = Q_ESCAPE if c == '\\' else Q_QUOTED

    if current_op:
        result.append((
            current_op,
            bytes(buff)
        ))

    return result
