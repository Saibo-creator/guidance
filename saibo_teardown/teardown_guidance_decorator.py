import guidance
from guidance._grammar import JoinRule, GrammarObject
from guidance._guidance import GuidanceGenerator



def put_QA_prompt(lm, input):
    lm += f'''
    Please answer the following questions
    ---
    Input: What is the capital of France?
    Output: Paris
    ---
    Input: What is the capital of Germany?
    Output: Berlin
    ---
    Input: {input}
    Output:
    '''
    return lm

@guidance(stateless=True)
def decorated_QA_prompt(lm, input):
    lm += f'''
    Please answer the following questions
    ---
    Input: What is the capital of France?
    Output: Paris
    ---
    Input: What is the capital of Germany?
    Output: Berlin
    ---
    Input: {input}
    Output:
    '''
    return lm



guidance_grammar_generator_QA_prompt_1 = guidance(put_QA_prompt, stateless=True, dedent=False)

guidance_grammar_generator_QA_prompt_2 = GuidanceGenerator(put_QA_prompt, stateless=True)



assert GuidanceGenerator == type(decorated_QA_prompt) == type(guidance_grammar_generator_QA_prompt_1) == type(guidance_grammar_generator_QA_prompt_2), "All three should be guidance objects"
assert guidance_grammar_generator_QA_prompt_1.f == guidance_grammar_generator_QA_prompt_2.f == put_QA_prompt, "The underlying function should be the same"
assert guidance_grammar_generator_QA_prompt_1._impl_generator.__code__ == guidance_grammar_generator_QA_prompt_2._impl_generator.__code__ == decorated_QA_prompt._impl_generator.__code__, "The underlying implementation should be the same"
assert put_QA_prompt == guidance_grammar_generator_QA_prompt_1._impl_generator.__wrapped__ == guidance_grammar_generator_QA_prompt_2._impl_generator.__wrapped__ , "The wrapped function should be the same"


###########################################
#
#
#    transform to GrammarObject
#
#
###########################################

x_grammar_objet = decorated_QA_prompt("What is the capital of France?")
y_grammar_objet = guidance_grammar_generator_QA_prompt_1("What is the capital of France?")
z_grammar_objet = guidance_grammar_generator_QA_prompt_2("What is the capital of France?")


assert type(x_grammar_objet) == type(y_grammar_objet) == type(z_grammar_objet), "Decorated function and wrapper function should return the same output"
assert x_grammar_objet.values[0] == y_grammar_objet.values[0] == z_grammar_objet.values[0], f"while they have differen ids, they should have the same output. Expected: {x_grammar_objet.values[0]} and got {y_grammar_objet.values[0]}"
assert issubclass(type(x_grammar_objet), GrammarObject) and type(x_grammar_objet) == JoinRule, "The output should be a GrammarOperator object"

print("All tests passed!")


###########################################
#
#
#    call our guidance function/ grammar object
#
#
###########################################


fake_lm = "hahah"

fake_lm += decorated_QA_prompt("What is the capital of France?")

real_lm = guidance.models.Transformers(model="microsoft/Phi-3.5-mini-instruct")

new_state = real_lm + decorated_QA_prompt("What is the capital of France?")

print(new_state)



