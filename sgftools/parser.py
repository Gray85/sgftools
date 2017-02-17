# -*- coding: utf_8 -*-
import codecs
import string

from pyparsing import OneOrMore, Word, QuotedString, Group, TokenConverter, Forward, Literal, ZeroOrMore, ParseBaseException
from sgftools.gamebuilder import GameBuilder


def _deep_to_list(alist):
    if isinstance(alist, str):
        return alist

    try:
        lst = list(alist)
        return [_deep_to_list(i) for i in alist]
    except TypeError:
        return alist


class GroupVariations(TokenConverter):
    def __init__(self, expr):
        super(GroupVariations, self).__init__(expr)

    def postParse(self, instring, loc, tokenlist):
        alist = list(tokenlist)
        if len(alist) == 0:
            return []

        alist.insert(0, 'variations')
        return [alist]


class SgfPyParser:
    def __init__(self):
        self._parser = self._game_tree_parser()

    def parse_file(self, file_name_or_file):
        try:
            return _deep_to_list(self._parser.parseFile(file_name_or_file))
        except ParseBaseException as ex:
            raise ValueError(ex)

    def parse_string(self, string):
        if not isinstance(string, str):
            raise TypeError("'string' must be str type")

        try:
            return _deep_to_list(self._parser.parseString(string))
        except ParseBaseException as ex:
            raise ValueError(ex)

    def _game_tree_parser(self):
        lparen = Literal('(').suppress()
        rparen = Literal(')').suppress()
        game_tree = Forward()
        game_tree << (lparen + self._sequence()
                      + GroupVariations(ZeroOrMore(Group(game_tree)))
                      + rparen
                      )
        return game_tree

    def _sequence(self):
        node = Literal(';').suppress() + ZeroOrMore(self._node_property())
        return OneOrMore(Group(node))  # TODO: группировать свойства по имени

    def _node_property(self):
        prop_ident = Word(string.ascii_uppercase)
        value = QuotedString(quoteChar='[', endQuoteChar=']', escChar='\\', multiline=True)
        return Group(prop_ident + OneOrMore(value))


class SgfParser:
    def __init__(self):
        self.tokenParser = SgfPyParser()

    def load_game_from_string(self, string_data):
        tokens = self.tokenParser.parse_string(string_data)
        return GameBuilder().build(tokens)

    def load_game(self, filename):
        with get_sgf_reader(open(filename, "rb")) as file:
            return self.load_game_from_string(file.read())

    def load_game_from_stream(self, binary_stream):
        file = get_sgf_reader(binary_stream)
        return self.load_game_from_string(file.read())


def get_sgf_reader(binary_stream):
    buffer = binary_stream.readline()
    encoding = extract_encoding(buffer)

    try:
        reader_creator = codecs.getreader(encoding)
    except LookupError:
        reader_creator = codecs.getreader("ascii")

    return reader_creator(BufferedReader(binary_stream, buffer))


def extract_encoding(bytes_data):
    if bytes_data.startswith(codecs.BOM_UTF32_LE):
        return 'utf-32-le'
    if bytes_data.startswith(codecs.BOM_UTF32_BE):
        return 'utf-32-be'
    if bytes_data.startswith(codecs.BOM_UTF16_LE):
        return 'utf-16-le'
    if bytes_data.startswith(codecs.BOM_UTF16_BE):
        return 'utf-16-be'
    if bytes_data.startswith(codecs.BOM_UTF8):
        return 'utf-8-sig'

    try:
        ind = bytes_data.index(b'CA[')
        close_index = bytes_data.index(b']', ind + 1)
        return str(bytes_data[ind + 3:close_index], encoding='ascii')
    except ValueError:
        return 'utf-8'


class BufferedReader:
    def __init__(self, bytes_stream, buffer):
        self._buffer = buffer
        self._stream = bytes_stream
        self._buffer_index = 0
        self._buffer_len = len(buffer)

    def read(self, count=-1):
        if count < 0:
            from_buffer = self._read_from_buffer(count)
            return from_buffer + self._stream.read()

        if self._buffer_index >= len(self._buffer):
            return self._stream.read(count)
        else:
            from_buffer = self._read_from_buffer(count)
            return from_buffer + self._stream.read(count - len(from_buffer))

    def seek(self, offset, origin):
        if origin == 1:
            self._buffer_index += offset
            if self._buffer_index > self._buffer_len:
                return self._stream.seek(origin, self._buffer_index - self._buffer_len)
            else:
                return self._buffer_index
        else:
            result = self._stream.seek(offset, origin)
            self._buffer_index = self._buffer_len
            return result

    def close(self):
        if self._stream is not None:
            self._stream.close()
            self._stream = None

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _read_from_buffer(self, count):
        if self._buffer_index >= len(self._buffer):
            return b""

        result = self._buffer[self._buffer_index:min(self._buffer_index + count, len(self._buffer))]
        self._buffer_index += count;
        return result

