import guidance 
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from transformers import BitsAndBytesConfig

prompt = "Long time ago in a far away galaxy, there was a"

# llama_tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama_v1.1", use_fast=False)

# tiny_llama_model = AutoModel.from_pretrained("TinyLlama/TinyLlama_v1.1")


guidance_model = guidance.models.Transformers(model="microsoft/Phi-3.5-mini-instruct")

guidance_model.echo=False


gen_op = guidance.gen(name="generated_object", max_tokens=5)

# output_state = guidance_model + prompt + gen_op
# print(output_state["generated_object"])


guidance_model._inplace_append(prompt)

output_state = guidance_model + gen_op

print(output_state["generated_object"])