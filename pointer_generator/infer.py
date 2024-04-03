import requests
import json
import torch
from pointer_generator.pointer_generator_src.transformer_pg import TransformerPointerGeneratorModel

def generate_correct_api(Error_Sentence: str):
    url = "https://nlp.laban.vn/wiki/ajax_spelling_checker_check/"

    payload = {
        'text': Error_Sentence,
        'app_type': 'web_demo'
    }
    
    files=[]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    response = json.loads(response.text)['result'][0]['suggested_text']
    return response

def generate_correct_sentence(sentence, batch_size, max_length, length_penalty, beam_size):
    model_path = "checkpoint24.pt"
    model = TransformerPointerGeneratorModel.from_pretrained(
        "checkpoints/", # path to the model directory
        checkpoint_file=model_path,
        data_name_or_path="bin",
        is_gpu=True,
        user_dir= "pointer_generator/pointer_generator_src"
    )
    
    model.eval()

    # # Tokenize input sentence
    # tokens = model.encode(sentence)

    # # Generate output sequence
    # generated_tokens = model.generate(
    #     tokens, # Add batch dimension
    #     beam=beam_size,
    #     lenpen=length_penalty,
    #     max_len_b=max_length
    # )

    # Decode generated tokens
    generated_sentence = model.translate([sentence])

    return generated_sentence

if __name__ == '__main__':
    sentence = "Cơn mưa ng ang qua mang em ddi xa ."
    sent = generate_correct_sentence(sentence, batch_size=1, max_length=100, beam_size=6, length_penalty=1.0)
    print(sent)