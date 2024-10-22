
import guidance
from transformers import (
    LlamaForCausalLM,
    LlamaConfig,
    AutoTokenizer,
    Phi3Config,
    Phi3ForCausalLM,
)
from transformers.utils import ModelOutput
import torch


class EchoModelMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repeat_queue = Queue()

    def set_repeat_sequence(self, token_ids: list[int]):
        """Set the sequence of tokens that the model will repeat during generation."""
        for token_id in token_ids:
            self._repeat_queue.put(token_id)

    def adjust_logits_for_repeat(self, output: ModelOutput):
        """Adjust logits to focus on repeating the next token from the queue."""
        try:
            next_token_to_repeat = self._repeat_queue.get(block=False)
        except:
            next_token_to_repeat = self.config.eos_token_id

        # print("Next token to repeat:", next_token_to_repeat)
        # Set the logits of all tokens other than the next token to -inf.
        output.logits[:, :, :next_token_to_repeat] = float("-inf")
        output.logits[:, :, next_token_to_repeat + 1:] = float("-inf")
        return output
    
    def forward(self, input_ids=None, **kwargs) -> ModelOutput:
        output = super().forward(input_ids, **kwargs)
        return self.adjust_logits_for_repeat(output)


from queue import Queue


class EchoLlamaForCausalLM(EchoModelMixin,LlamaForCausalLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EchoPhi3ForCausalLM(EchoModelMixin, Phi3ForCausalLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




if __name__ == "__main__":

    # randomly init a tiny llama model
    pretrained_llama_tokenizer = AutoTokenizer.from_pretrained(
        "hf-internal-testing/llama-tokenizer", use_fast=False
    )
    tiny_llama_config = LlamaConfig(
        vocab_size=pretrained_llama_tokenizer.vocab_size,
        eos_token_id=pretrained_llama_tokenizer.eos_token_id,
        pad_token_id=pretrained_llama_tokenizer.pad_token_id,
        bos_token_id=pretrained_llama_tokenizer.bos_token_id,
        hidden_size=4,
        intermediate_size=8,
        num_attention_heads=1,
        num_hidden_layers=1,
    )

    echo_llama_model = EchoLlamaForCausalLM(tiny_llama_config)
    # print(echo_llama_model)

    llama_model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

    echo_llama_model = EchoLlamaForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

    pretrained_llama_tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-3.2-1B", use_fast=False
    )

    prompt = " The quick brown fox jumps over the lazy dog."

    # # set the target token ids
    target_token_ids = pretrained_llama_tokenizer(prompt)["input_ids"]
    print(target_token_ids)
    ###################
    # Output
    ###################

    prompt = " The quick brown fox jumps over the lazy dog."

    # set the target token ids
    target_token_ids = pretrained_llama_tokenizer(prompt)["input_ids"]
    print(target_token_ids)
    print(pretrained_llama_tokenizer(prompt*2)["input_ids"])

    echo_llama_model.set_repeat_sequence(token_ids=target_token_ids[1:]) # TODO, need to remove the BOS token in a proper way
    guidance_model = guidance.models.Transformers(model=echo_llama_model, tokenizer=pretrained_llama_tokenizer)
    # guidance_model = guidance.models.Transformers(model=llama_model, tokenizer=pretrained_llama_tokenizer)


    gen_op = guidance.gen(name="generated_object", max_tokens=20)

    output_state = guidance_model + "" + gen_op # replace prompt by "" to avoid error TODO, use prompt will cause error
    # print(output_state["generated_object"])
    