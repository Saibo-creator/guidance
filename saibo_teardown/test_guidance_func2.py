from guidance._guidance import  RawFunctionObject

# Mock class to represent a model object and a GrammarRule for demonstration purposes.
class MockModel:
    def __init__(self, state=""):
        self.state = state

    def __str__(self):
        return self.state
    
    def generate(self):
        return "hhhhhhhh"

# Define a simple function that we want to wrap in a RawFunction.
def append_hello(model, *args, **kwargs):
    model.state  = model.generate()
    model.state += "Hello "
    return model

# Create a RawFunction that wraps our simple function.
raw_func = RawFunctionObject(append_hello, args=[], kwargs={})

# Create a mock model object.
model = MockModel()

# Call the RawFunction with the model.
raw_func(model)
print("After calling raw_func:", model)  # Output: "Hello "

