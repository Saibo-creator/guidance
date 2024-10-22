import guidance
from guidance import select, capture
from guidance._grammar import Select, JoinRule
from guidance.library._sequences import exactly_n_repeats
from guidance.library._subgrammar import lexeme
from guidance.library._gen import gen_quote, regex



lm = guidance.models.Transformers(model="microsoft/Phi-3.5-mini-instruct")

lm.echo = False


# out  = lm + f'Do you want a joke or a poem? A ' + select(['joke', 'poem'], name='choice') + f' please!'

# print(out['choice'])

out = lm + f'Do you want a joke or a poem? A ' + Select(['joke', 'poem'], capture_name='choice') + f' please!'
print(out['choice'])


# exactly n repeats

out = lm + f'Please repeat the word "hello" exactly 3 times: ' + capture(exactly_n_repeats('hello', 3), 'repeats')
print(out['repeats'])

# exactly n repeats directly with grammar rules

out = lm + f'Please repeat the word "hello" exactly 3 times: ' + capture(JoinRule(["hello"] * 3), 'repeats')

print(out['repeats'])


# try lexeme

out = lm + f'Please repeat the word "hello": ' + capture(lexeme("hello"), 'lexeme')


print(out['lexeme'])


# text regex

out = lm + f'Please write a telephone number: ' + capture(regex(r'\d{3}-\d{3}-\d{4}'), 'phone')

print(out['phone'])


