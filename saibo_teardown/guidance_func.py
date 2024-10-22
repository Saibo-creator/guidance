import guidance
from guidance import one_or_more, select, zero_or_more, gen, capture


guidance_model = guidance.models.Transformers(model="microsoft/Phi-3.5-mini-instruct")

# @guidance(stateless=True)
def ner_instruction(lm, input):
    lm += f'''\
    Please tag each word in the input with PER, ORG, LOC, or nothing
    ---
    Input: John worked at Apple.
    Output:
    John: PER
    worked: 
    at: 
    Apple: ORG
    .: 
    ---
    Input: {input}
    Output:
    '''
    return lm

wrapper_ner_instruction = guidance(ner_instruction, stateless=True, dedent=False)

# print id of the function
print(f"Function id of ner_instruction is {hex(id(ner_instruction))}")
print(f"Function id of wrapper_ner_instruction is {hex(id(wrapper_ner_instruction))}")

import pdb; pdb.set_trace()
input = 'Julia never went to Morocco in her life!!'
output_state = guidance_model + capture(wrapper_ner_instruction(input), "output1") + capture(gen(stop='---', max_tokens=3), name='output2')


print(f"Prompt used is {output_state['output1']}")
print(f"Output is {output_state['output2']}")