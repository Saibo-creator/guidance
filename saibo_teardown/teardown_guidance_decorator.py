import guidance
from guidance._grammar import JoinRule, GrammarObject
from guidance._guidance import GuidanceGenerator



def do_QA(lm, input):
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
def decorated_do_QA(lm, input):
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



guidance_grammar_generator_do_QA_1 = guidance(do_QA, stateless=True, dedent=False)

guidance_grammar_generator_do_QA_2 = GuidanceGenerator(do_QA, stateless=True)



assert GuidanceGenerator == type(decorated_do_QA) == type(guidance_grammar_generator_do_QA_1) == type(guidance_grammar_generator_do_QA_2), "All three should be guidance objects"
assert guidance_grammar_generator_do_QA_1.f == guidance_grammar_generator_do_QA_2.f == do_QA, "The underlying function should be the same"
assert guidance_grammar_generator_do_QA_1._impl_generator.__code__ == guidance_grammar_generator_do_QA_2._impl_generator.__code__ == decorated_do_QA._impl_generator.__code__, "The underlying implementation should be the same"
assert do_QA == guidance_grammar_generator_do_QA_1._impl_generator.__wrapped__ == guidance_grammar_generator_do_QA_2._impl_generator.__wrapped__ , "The wrapped function should be the same"


###########################################
#
#
#    running the guidance function to get Grammar object
#
#
###########################################

x_grammar_objet = decorated_do_QA("What is the capital of France?")
y_grammar_objet = guidance_grammar_generator_do_QA_1("What is the capital of France?")
z_grammar_objet = guidance_grammar_generator_do_QA_2("What is the capital of France?")


assert type(x_grammar_objet) == type(y_grammar_objet) == type(z_grammar_objet), "Decorated function and wrapper function should return the same output"
assert x_grammar_objet.values[0] == y_grammar_objet.values[0] == z_grammar_objet.values[0], f"while they have differen ids, they should have the same output. Expected: {x_grammar_objet.values[0]} and got {y_grammar_objet.values[0]}"
assert type(x_grammar_objet) == JoinRule and issubclass(type(x_grammar_objet), GrammarObject), "The output should be a GrammarOperator object"






