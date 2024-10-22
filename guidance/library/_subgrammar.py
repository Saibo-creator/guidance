from guidance._grammar import LLSerializer, RegularGrammar, string
from .._grammar import Subgrammar, GrammarLexemeTerminalRule, GrammarObject, capture
from typing import Optional


def lexeme(
    body_regex: str,
    contextual: bool = False,
    json_string: bool = False,
) -> GrammarLexemeTerminalRule:
    """
    Constructs a Lexeme based on a given regular expression.

    Parameters:
    body_regex (str): The regular expression that will greedily match the input.
    contextual (bool): If false, all other lexemes are excluded when this lexeme is recognized.
        This is normal behavior for keywords in programming languages.
        Set to true for eg. a JSON schema with both `/"type"/` and `/"[^"]*"/` as lexemes,
        or for "get"/"set" contextual keywords in C#.
    json_string (bool): Specifies if the lexeme should be quoted as a JSON string.
        For example, /[a-z"]+/ will be quoted as /([a-z]|\\")+/.
        Defaults to False.
    """
    return GrammarLexemeTerminalRule(body_regex=body_regex, contextual=contextual, json_string=json_string)


def subgrammar(
    name: str = None,
    *,
    body: GrammarObject,
    skip_regex: Optional[str] = None,
    no_initial_skip: bool = False,
    max_tokens=100000000,
) -> GrammarObject:
    r: GrammarObject = Subgrammar(
        body=body,
        skip_regex=skip_regex,
        no_initial_skip=no_initial_skip,
        max_tokens=max_tokens,
    )
    if name:
        r = capture(r, name)
    return r


def as_regular_grammar(value, lexeme=False) -> RegularGrammar:
    # TODO: assert that value is not empty since we don't yet support that
    if isinstance(value, str):
        value = string(value)
    # check if it serializes
    _ignore = LLSerializer().regex(value)
    return RegularGrammar(value, lexeme=lexeme)
