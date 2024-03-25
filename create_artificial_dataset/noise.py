import random
import argparse
import os
import shutil
from .utils import tokenize, append_sent_to_file

# from underthesea import pos_tag
list1 = "qwertyuiopasdfghjklzxcvbnmư"
list2 = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
dict1 = {'à':'af', 'á':'as', 'ả':'ar', 'ã':'ax', 'ạ':'aj', 'ă':'aw', 'ằ':'afw', 'ắ':'asw', 'ẳ':'arw', 'ẵ':'axw', 'ặ':'ajw', 'â':'aa', 'ầ':'aaf',
         'ấ':'aas', 'ẩ':'aar', 'ẫ':'aax', 'ậ':'aaj', 'đ':'dd', 'è':'ef', 'é':'es', 'ẻ':'er', 'ẽ':'ex', 'ẹ':'ej', 'ê':'ee', 'ề':'eef', 'ế':'ees',
         'ể':'eer', 'ễ':'eex', 'ệ':'eej', 'ì':'if', 'í':'is', 'ỉ':'ir', 'ĩ':'ix', 'ị':'ij', 'ò':'of', 'ó':'os', 'ỏ':'or', 'õ':'ox', 'ọ':'oj',
         'ô':'oo', 'ồ':'oof', 'ố':'oos', 'ổ':'oor', 'ỗ':'oox', 'ộ':'ooj', 'ơ':'ow', 'ờ':'owf', 'ớ':'ows', 'ở':'owr', 'ỡ':'owx', 'ợ':'owj',
         'ù':'uf', 'ú':'us', 'ủ':'ur', 'ũ':'ux', 'ụ':'uj', 'ư':'uw', 'ừ':'uwf', 'ứ':'uws', 'ử':'uwr', 'ữ':'uwx', 'ự':'uwj', 'ỳ':'yf',
         'ý':'ys', 'ỷ':'yr', 'ỹ':'yx', 'ỵ':'yj','l':'n', 's':'x','x':'s','n':'l'}

dict2 = {'tr':'ch', 'ch':'tr', 'ỏa': 'oả', "óa" : "oá", "ủy": "uỷ", "ội": "ôị", "ỏe": "oẻ", "Ủy": "Uỷ",
         "tr": "ch", "oạ": "ọa", 'ệu': 'êụ', 'uá': 'úa', 'iá': 'ía', 'ùy':'uỳ', 'ọa': 'oạ', 'gi': 'd', 'ủa':'ảu', 'úa':'uá',
         'uả': 'ủa', 'oà': 'òa', 'ũy': 'uỹ', 'iả': 'ỉa', 'ượ': 'ựơ', 'oá': 'óa', 'ụy': 'uỵ', 'ườ': 'uwof', 'ĩa': 'iã', 'ậu': 'âụ',
         'ại': 'aị', 'oả': 'ỏa', 'uý': 'úy', 'iệ': 'ịê', 'ượ': 'ựo', 'ượ': 'uợ', 'ượ': 'ự', 'Ch': 'Tr', 'ướ': 'ứ', 'gi': 'r', 'úy': 'uý', 'ợi': 'ơị',
         'áo': 'óa', 'uố': 'ướ', 'ải': 'ẩn', 'ài': 'ìa', 'uà': 'ùa', 'ửa': 'ưả', 'ưở': 'uow', 'ọa': 'oạ', 'ều': 'êù', 'kh': 'k', 'ng':'n'}

dict3 = {'a': ['ạ', 'á', 'à', 'ã', 'a'],
         'ă': ['ắ', 'ằ', 'ặ'],
         'â': ['ẩ', 'ậ', 'ấ', 'ẫ', 'ẩ'],
         'uo': ['ướ', 'ứơ', 'ươ'],
         'o': ['ơ', 'ọ', 'ó', 'ò', 'õ', 'o', 'ô'],
         'ơ': ['ớ', 'ờ', 'ợ', 'ở', 'ỡ'],
         'd': ['gi', 'r', 'd'],
         'u': ['ư','ù','ú','ủ', 'ụ', 'u'],
         'ư': ['ự', 'ừ', 'ử', 'ữ', 'ứ'],
         'i': ['ĩ', 'ì', 'í', 'ỉ', 'ị', 'i'],
         'e': ['é', 'ẽ','ẹ', 'è', 'ẻ', 'e', 'ê'],
         'ô': ['ố', 'ồ', 'ổ', 'ộ', 'ỗ'] }

change_tone = list(dict3.values())

def create_Error(sent, error_rate):
    tokens = tokenize(sent)
    out = []
    count = 0
    for i, token in enumerate(tokens):
        # nếu là dấu hoặc các từ đặc biệt thì giữ nguyên, không tạo lỗi
        if not token.isalpha():
            out.append(0)
            continue
        prob = random.random()
        # nếu word trong 1 câu có xác suất nhỏ hơn pivot thì tiến hành tạo lỗi trên nó
        # make sure that number of error not large than 1/2 total number of tokens
        if prob < error_rate and count <= len(tokens) // 2:
            count = count + 1
            prob = prob/error_rate
                # đổi chỗ vị trí 2 char
            if prob < 0.05:
                modified_word = list(token)
                word_length = len(modified_word)
                if word_length - 2 <= 0:
                  out.append(0)
                  continue
                modified_index = random.randint(0, word_length - 2)
                modified_word[modified_index], modified_word[modified_index + 1] = modified_word[modified_index + 1], modified_word[modified_index]
                tokens[i] = ''.join(modified_word)
                if tokens[i] == token:
                  out.append(0)
                else: out.append(1)
                # thêm 1 char vào word
            elif prob < 0.1:
                modified_word = list(token)
                word_length = len(modified_word)
                modified_index = random.randint(0, word_length - 1)
                y = random.randrange(len(list1))
                tokens[i] = ''.join(modified_word[:modified_index]) + list1[y] + ''.join(modified_word[modified_index:])

                if tokens[i] == token:
                  out.append(0)
                else: out.append(1)
                # xóa 1 char khỏi word
            elif prob < 0.15:
                modified_word = list(token)
                word_length = len(modified_word)
                modified_index = random.randint(0, word_length - 1)
                tokens[i] =  ''.join(modified_word[:modified_index ] + modified_word[modified_index + 1:])

                if tokens[i] == token:
                  out.append(0)
                else: out.append(1)
                # xóa từ ở vị trí này
            elif prob < 0.16:
                tokens[i] =  ''
                # đổi dấu của 1 char, nếu không có dấu thì giữ nguyên
            elif prob < 0.6:
                changed = False
                new_token = token
                for k in range(len(change_tone)):
                    tone = random.choice(change_tone)
                    for ton in tone:
                      if ton in token:
                        while new_token == token:
                            new_token = token.replace(ton, random.choice(tone))
                        changed = True
                        break
                    if changed:
                      break
                if tokens[i] == new_token:
                  out.append(0)
                else:
                  out.append(1)
                  tokens[i] = new_token
                # thay 1 char bằng 1 char khác
            elif prob < 0.75:
                modified_word = list(token)
                word_length = len(modified_word)
                modified_index = random.randint(0, word_length - 1)
                modified_char = random.choice(list2)
                # loại trừ trường hợp random ra chính từ gốc
                while modified_char == modified_word[modified_index]:
                    modified_char = random.choice(list2)
                # thay thế từ đã được sửa
                modified_word[modified_index] = modified_char
                tokens[i] = ''.join(modified_word)

                if tokens[i] == token:
                  out.append(0)
                else: out.append(1)
                #chuyển word về dạng telex của nó, nếu nó ko có từ nào chuyển được thì giữ nguyên
            elif prob < 0.85:
                vn_letters = [char for char in token if char in dict1.keys()]
                if vn_letters:
                    # Randomly select one of the Vietnamese letters
                    modified_letter = random.choice(vn_letters)
                    # Replace the letter with its corresponding Telex coding
                    tokens[i] = tokens[i].replace(modified_letter, dict1[modified_letter])
                    out.append(1)
                else:
                    out.append(0)
            # đổi vị trí 2 dấu câu, không có từ nào thì giữ nguyên
            elif prob < 0.99:
                vn_letters = [token[i:i+2] for i in range(len(token)-1) if token[i:i+2] in dict2.keys()]
                if vn_letters:
                    # Randomly select one of the Vietnamese letters
                    modified_letter = random.choice(vn_letters)
                    # Replace the letter with its corresponding Telex coding
                    tokens[i] = tokens[i].replace(modified_letter, dict2[modified_letter])
                    out.append(1)
                else:
                    out.append(0)
                # tách từ ra thành 2 từ
            else:
              modified_word = list(token)
              word_length = len(modified_word)

              if word_length < 2:
                out.append(0)
                continue

              modified_index = random.randint(1, word_length - 1)
              tokens[i] =  token[:modified_index] + " " + token[modified_index:]
              if tokens[i] == token:
                out.append(0)
              else: out.append(1)
        else:
            out.append(0)
        if count >= len(tokens) // 2:
            out.extend([0] * (len(tokens) - i - 1))
            return ' '.join(tokens), out
    return ' '.join(tokens), out

def load_dataset(file_path):
    dataset = []
    with open(file_path, 'r',encoding= "utf-8") as f:
        for line in f:
            line = line.strip()
            dataset.append(line)
    return dataset

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    arguments = [
        ('--input', {"dest": "input_path","type": str, "default" : "sample_document/train.txt",
         "help": "input file to create dataset"}),
        ('--output', {"dest": "output_folder","type": str, "default" : "sample_document",
         "help": "output folder to save created dataset"}),
        ('--error-rate', {"dest": "error_rate","type": int, "default" : 0.1,
         "help": "Probability that a word in a sentence has an error."})
    ]

    for argument, kwargs in arguments:
        parser.add_argument(argument, **kwargs)

    options = parser.parse_args()
    
    
    error_dataset = []
    mask_dataset = []
    i = 0
    
    output_file = os.path.join(options.output_folder, os.path.basename(options.input_path).split(".txt")[0])
    
    # write into source file using batch
    with open(options.input_path,encoding = 'utf-8') as txt_file:
        for line in txt_file:
            i = i + 1
            error_sent,mask = create_Error(line,0.1)
            error_dataset.append(error_sent)
            mask_dataset.append(mask)

            if i % 100 == 0:
                append_sent_to_file(f"{output_file}.src", error_dataset)
                error_dataset = []
                mask_dataset = []
        # check if there are any sent in the last lines
        if len(error_dataset) > 0:
            append_sent_to_file(f"{output_file}.src", error_dataset)
            
    shutil.copyfile(options.input_path, f"{output_file}.tgt")
    print(f"Processing file {options.input_path} done! Saving into 2 new files {output_file}.src and {output_file}.tgt")