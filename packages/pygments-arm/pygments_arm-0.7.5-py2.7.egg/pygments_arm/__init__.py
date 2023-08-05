# -*- coding: utf-8 -*-
"""
    ARM lexer
    ~~~~~~~~~

    Pygments lexer for ARM Assembly.

    :copyright: Copyright 2017 Jacques Supcik
    :license: Apache 2, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include
from pygments.token import Text, Name, Number, String, Comment, Punctuation

__all__ = ['ArmLexer']

class ArmLexer(RegexLexer):
    name = 'ARM'
    aliases = ['arm']
    filenames = ['*.S']

    string = r'"(\\"|[^"])*"'
    char = r'[\w$.@-]'
    identifier = r'(?:[a-zA-Z$_]' + char + '*|\.' + char + '+)'
    number = r'(?:0[xX][a-zA-Z0-9]+|\d+)'

    tokens = {
        'root': [
            include('whitespace'),
            (identifier + ':', Name.Label),
            (number + ':', Name.Label),
            (r'[.#]' + identifier, Name.Attribute, 'directive-args'),
            (identifier, Name.Function, 'instruction-args'),
            (r'[\r\n]+', Text)
        ],
        'directive-args': [
            (identifier, Name.Constant),
            (string, String),
            (number, Number.Integer),
            (r'[\r\n]+', Text, '#pop'),
            include('punctuation'),
            include('whitespace')
        ],
        'instruction-args': [
            (identifier, Name.Constant),
            (number, Number.Integer),
            # Registers
            ('r[rR]\d+', Name.Variable),
            (r"'(.|\\')'?", String.Char),
            (r'[\r\n]+', Text, '#pop'),
            include('punctuation'),
            include('whitespace')
        ],
        'whitespace': [
            (r'[ \t]', Text),
            (r'//[\w\W]*?(?=\n)', Comment.Single),
            (r'/[*][\w\W]*?[*]/', Comment.Multiline),
            (r'[;@].*?(?=\n)', Comment.Single)
        ],
        'punctuation': [
            (r'[-*,.()\[\]!:{}^=#\+\\]+', Punctuation)
        ],
        'eol': [
            (r'[\r\n]+', Text)
        ],
    }
