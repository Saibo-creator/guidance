from guidance._parser import TokenParser

from guidance._grammar import Select, JoinRule
from guidance.library._sequences import exactly_n_repeats
from guidance.library._subgrammar import lexeme
from guidance.library._gen import gen_quote, regex

from guidance.models.transformers._transformers import TransformersTokenizer


select_grammar = Select(['joke', 'poem'], capture_name='choice')

exactly_n_repeats_grammar = exactly_n_repeats('hello', 3)

lexeme_grammar = lexeme("hello")

regex_grammar = regex(r'\d{3}-\d{3}-\d{4}')


phi_tokenizer = TransformersTokenizer(model="microsoft/Phi-3.5-mini-instruct",
                                      transformers_tokenizer=None)


select_token_parser = TokenParser(select_grammar, phi_tokenizer)

print("successful")