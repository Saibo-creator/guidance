from guidance._guidance import GuidanceFunction

def simple_function(lm, text):
    return lm + f"Generated with: {text}"

guidance_func = GuidanceFunction(simple_function, stateless=True)

print(simple_function)
import pprint
pprint.pprint(guidance_func.__dict__)
print(guidance_func.__signature__)

# Usage
result = guidance_func("My input text")
print(result)
