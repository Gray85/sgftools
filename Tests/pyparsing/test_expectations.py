import unittest
from pyparsing import OneOrMore, Word, QuotedString,Group, TokenConverter, Forward, Literal, ZeroOrMore
import string

def tolist(s, l, t):
        l = list(t)
        l.append('!')
        return l

class ByList(TokenConverter):
    def __init__(self, expr):
        super(ByList, self).__init__(expr)
        self.saveAsList = True

    def postParse( self, instring, loc, tokenlist ):
        result = [list(tokenlist)]
        return result


class pyparsingexpectations(unittest.TestCase):

    def get_aproperty(self):
        prop_ident = Word(string.ascii_uppercase)
        value = QuotedString(quoteChar='[', endQuoteChar = ']', escChar = '\\', multiline = True)
        return  prop_ident + OneOrMore(value)

    def test_simple_example(self):
        aProperty = self.get_aproperty()
        result = aProperty.parse_string("AW[ab]\r\n[bc][]")
        self.assertEqual(['AW', 'ab', 'bc', ''], list(result))

    def test_escapes(self):
        aProperty = self.get_aproperty()
        result = aProperty.parse_string("AW[a\]b]\r\n[b\\\\c][]")
        self.assertSequenceEqual(['AW', 'a]b', 'b\\c', ''], result)

    def test_tokenconverter_override(self):
        aProperty = OneOrMore(ByList(self.get_aproperty()))
        result = aProperty.parseString("AW[ab]AB[dd]")
        self.assertEqual([['AW', 'ab'],['AB', 'dd']], list(result))

    def test_parse_action(self):
        parser = OneOrMore(Word('ab')).setParseAction(tolist)
        actual = parser.parse_string('a b a')
        self.assertSequenceEqual(['a', 'b', 'a', '!'], actual)

if __name__ == '__main__':
    unittest.main()