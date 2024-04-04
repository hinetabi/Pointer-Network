import requests
import json
import torch
from fairseq.models.transformer import TransformerModel
from pointer_generator.preprocess import add_oov_sentence, reformat_sentence
from pointer_generator.postprocess import replace_oov_sentence

class Generate():
    def __init__(self) -> None:
        model_path = "checkpoints/checkpoint24.pt"
        self.model = TransformerModel.from_pretrained(
                ".", # path to the model directory
                checkpoint_file=model_path,
                data_name_or_path="bin",
                is_gpu=True,
                user_dir= "pointer_generator/pointer_generator_src"
            )
            
        self.model.eval()
        


    def generate_correct_sentence(self, sentence):
        preprocess_sentence = add_oov_sentence(reformat_sentence(sentence), vocab_file="sample_data/dict.pg.txt")
        generated_sentence = self.model.translate([preprocess_sentence], beam = 6)[0]
        postprocess_sentence = replace_oov_sentence(reformat_sentence(sentence), generated_sentence)
        
        return postprocess_sentence

if __name__ == '__main__':
    sentence = "Cơn mưa ng ang qua mang em ddi xa."
    # sentence = "Công nghệ <unk-2> : <unk-4> động lớn đến các nền kinh tế mới nổi ."
    # sentence = "Công nghệ Blockchain : Tasc động lớn đến các nền kinh tế mới nổi ."
    generate = Generate()
    sent = generate.generate_correct_sentence(sentence)
    print(sent)