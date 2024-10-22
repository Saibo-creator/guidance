import guidance
from guidance._grammar import capture
from guidance.library._json import _gen_json, _gen_json_array, _gen_json_object, _gen_json_any, \
    _gen_json_int, _gen_json_number, _gen_json_string, _gen_list, _get_format_pattern




lm = guidance.models.Transformers(model="microsoft/Phi-3.5-mini-instruct")

lm.echo = False



output_state = lm + "Please generate a JSON object with the following fields: " + _gen_json_string(min_length=5, max_length=10)


