# -*- coding: utf_8 -*-
import codecs
import string

from pyparsing import OneOrMore, Word, QuotedString, Group, TokenConverter, Forward, Literal, ZeroOrMore
from sgftools.gamebuilder import GameBuilder


def _deepToList(alist):
    if isinstance(alist, str):
        return alist

    try:
        lst = list(alist)
        return [_deepToList(i) for i in alist]
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

    def parseFile(self, fileNameOrFile):
        return _deepToList(self._parser.parseFile(fileNameOrFile))

    def parseString(self, string):
        return _deepToList(self._parser.parseString(string))

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

    def load_game_from_string(self, string):
        tokens = self.tokenParser.parseString(string)
        return GameBuilder().Build(tokens)

    def load_game(self, filename):
        encoding = self.extract_encoding(filename)
        with open(filename, 'r', encoding=encoding) as file:
            return self.load_game_from_string(file.read())

    @staticmethod
    def extract_encoding(filename):
        with open(filename, 'rb') as afile:
            line = afile.readline()
            if line.startswith(codecs.BOM_UTF32_LE):
                return 'utf-32-le'
            if line.startswith(codecs.BOM_UTF32_BE):
                return 'utf-32-be'
            if line.startswith(codecs.BOM_UTF16_LE):
                return 'utf-16-le'
            if line.startswith(codecs.BOM_UTF16_BE):
                return 'utf-16-be'
            if line.startswith(codecs.BOM_UTF8):
                return 'utf-8-sig'

            try:
                ind = line.index(b'CA[')
                close_index = line.index(b']', ind + 1)
                return str(line[ind + 3:close_index], encoding='ascii')
            except ValueError:
                return 'utf-8'
