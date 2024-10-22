import guidance 
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from transformers import BitsAndBytesConfig
from guidance._grammar import JoinRule, capture

prompt = "Long time ago in a far away galaxy, there was a"

# llama_tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama_v1.1", use_fast=False)

# tiny_llama_model = AutoModel.from_pretrained("TinyLlama/TinyLlama_v1.1")


guidance_model = guidance.models.Transformers(model="microsoft/Phi-3.5-mini-instruct")

guidance_model.echo=False


gen_op = guidance.gen(name="generated_object", max_tokens=2)

# output_state = guidance_model + prompt + gen_op
# print(output_state["generated_object"])


guidance_model._inplace_append(prompt)

output_state = guidance_model + gen_op

print(output_state["generated_object"])


class TestOperators:
    def __init__(self):
        self.prompt = "Long time ago in a far away galaxy, there was a"
        self.guidance_model = guidance.models.Transformers(model="microsoft/Phi-3.5-mini-instruct")
        self.guidance_model.echo = False
        self.gen_op = guidance.gen(name="generated_object", max_tokens=5)

    def test_gen_repr(self):
        # Test if the gen operation is successfully created
        expected_repr = "gen(name='generated_object', max_tokens=5)"
        assert repr(self.gen_op).startswith("""gen                  <- c        
c                    <- generated_object        capture_name=generated_object """), f"Expected repr to be {expected_repr}, got {repr(self.gen_op)}"

    def test_type_of_operator(self):
        assert isinstance(self.gen_op, JoinRule), "Expected gen_op to be of type Join"


class TestGuidanceModel:
    def __init__(self):
        # Initialize the guidance model and other parameters
        self.prompt = "Long time ago in a far away galaxy, there was a"
        self.guidance_model = guidance.models.Transformers(model="microsoft/Phi-3.5-mini-instruct")
        self.guidance_model.echo = False
        self.gen_op = guidance.gen(name="generated_object", max_tokens=5)

    def test_inplace_append(self):
        # Test if the prompt is successfully appended to the guidance model
        self.guidance_model._inplace_append(self.prompt)
        assert self.guidance_model._state == self.prompt, f"Expected state to be {self.prompt}, got {self.guidance_model._state}"

    def test_gen_repr(self):
        # Test if the gen operation is successfully created
        expected_repr = "gen(name='generated_object', max_tokens=5)"
        assert repr(self.gen_op).startswith("""gen                  <- c        
c                    <- generated_object        capture_name=generated_object """), f"Expected repr to be {expected_repr}, got {repr(self.gen_op)}"

    def test_generate(self):
        # Test if the generated object is successfully generated
        self.guidance_model._inplace_append(self.prompt)
        output_state = self.guidance_model + self.gen_op
        assert output_state["generated_object"], "Expected generated_object to be present in output_state"

# Run the tests manually
if __name__ == "__main__":
    # tester = TestGuidanceModel()
    # tester.test_inplace_append()
    # print("test_inplace_append passed")
    
    # tester.test_gen_repr()
    # print("test_gen_repr passed")
    
    # tester.test_generate()
    # print("test_generate passed")


    tester = TestOperators()
    tester.test_type_of_operator()
