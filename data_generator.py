from tqdm import tqdm
import random
import numpy as np
import re

np.random.seed(42)
class DataGenerator:
    def __init__(self,data = ()):
        if data == None:
            self.data = []
        else: 
            self.data = list(data)
        self.generated_data = []
        self.generated_label = []
        self.error_counts = {'No Error':0, 
                             'Telex Typing Error':0,
                             'VNI Typing Error':0,
                             'Missing Diacritical Marks':0,
                             'Excess Letter Error': 0,
                             'Missing Letter Error':0,
                             'Wrong Spelling Error':0
                             }
        self.label2id = {0 : 'No Error',
                         1 : 'Telex Typing Error',
                         2 : 'VNI Typing Error',
                         3 : 'Missing Diacritical Marks',
                         4 : 'Excess Letter Error',
                         5 : 'Missing Letter Error',
                         6 : 'Wrong Spelling Error'
                        }
    def __len__(self):
        if len(self.generated_data):
            return len(self.generated_data)
        else: 
            raise Exception("Data has not been generated. Please call generate() to generate data")
    def __getitem__(self, index):
        if len(self.generated_data):
            return self.generated_data[index]
        raise Exception("Data has not been generated. Please call generate() to generate data") 
        
    def No_Error(self, text):
        return [text, 0]

    def Telex_Typing_Error(self, word):
        telex_dict = {'à': 'af', 'á': 'as', 'ả': 'ar', 'ã': 'ax', 'ạ': 'aj',
                    'ă': 'aw', 'ằ': ['awf', 'afw'], 'ắ': ['aws' ,'asw'], 'ẳ': ['awr', 'arw'], 'ẵ': ['awx', 'axw'], 'ặ': ['awj','ajw'],
                    'â': 'aa', 'ầ': ['aaf', 'afa'], 'ấ': ['aas', 'asa'], 'ẩ': ['aar', 'ara'], 'ẫ': ['aax', 'axa'], 'ậ': ['aaj','aja'],
                    'è': 'ef', 'é' : 'es', 'ẻ': 'er', 'ẽ': 'ex', 'ẹ': 'ej',
                    'ê': 'ee', 'ề': ['eef', 'efe'], 'ế': ['ees', 'ese'], 'ể': ['eer', 'ere'], 'ễ': ['eex', 'exe'], 'ệ': ['eej','eje'],
                    'ì': 'if', 'í': 'is', 'ỉ': 'ir', 'ĩ': 'ix', 'ị':'ij',
                    'ò': 'of', 'ó':'os', 'ỏ': 'or', 'õ': 'ox', 'ọ': 'oj',
                    'ô': 'oo', 'ồ': ['oof', 'ofo'], 'ố': ['oos', 'oso'], 'ổ': ['oor', 'oro'], 'ỗ': ['oox', 'oxo'], 'ộ': ['ooj', 'ojo'],
                    'ơ': 'ow', 'ờ': ['owf', 'ofw'], 'ớ': ['ows', 'osw'], 'ở': ['owr', 'orw'], 'ỡ': ['owx', 'oxw'], 'ợ': ['owj', 'ojw'],
                    'ù': 'uf', 'ú': 'us', 'ủ': 'ur', 'ũ': 'ux', 'ụ': 'uj',
                    'ư': 'uw', 'ừ': ['uwf', 'ufw'], 'ứ': ['uws', 'usw'], 'ử': ['uwr', 'urw'], 'ữ': ['uwx', 'uxw'], 'ự': ['uwj', 'ujw'],
                    'ỳ': 'yf', 'ý': 'ys', 'ỷ': 'yr', 'ỹ': 'yx', 'ỵ': 'yj',
                    'đ': 'dd'
                    }
        telex_word = ''
        for char in word: 
            if char.lower() in telex_dict:
                if type(telex_dict[char.lower()]) == list:
                    if random.random() <= 0.8:
                        telex_char = telex_dict[char.lower()][0]
                    else:
                        telex_char = telex_dict[char.lower()][1]
                else:

                    telex_char = telex_dict[char.lower()]
                if char.isupper():
                        telex_char = telex_char.title()
                telex_word += telex_char 
            else:
                telex_word += char
        if telex_word == word:
            return [word, 0]
        else:
            return [telex_word,1]

    def VNI_Typing_Error(self, word):
        vni_dict = {'à': 'a2', 'á': 'a1', 'ả': 'a3', 'ã': 'a4', 'ạ': 'a5',
                    'ă': 'a8', 'ằ': ['a82', 'a28'], 'ắ': ['a81' ,'a18'], 'ẳ': ['a83', 'a38'], 'ẵ': ['a84', 'a48'], 'ặ': ['a85','a58'],
                    'â': 'a6', 'ầ': ['a62', 'a26'], 'ấ': ['a61', 'a16'], 'ẩ': ['a63', 'a36'], 'ẫ': ['a64', 'a46'], 'ậ': ['a65','a56'],
                    'è': 'e2', 'é' : 'e1', 'ẻ': 'e3', 'ẽ': 'e4', 'ẹ': 'e5',
                    'ê': 'e6', 'ề': ['e62', 'e26'], 'ế': ['e61', 'e16'], 'ể': ['e63', 'e36'], 'ễ': ['e64', 'e46'], 'ệ': ['e65','e56'],
                    'ì': 'i2', 'í': 'i1', 'ỉ': 'i3', 'ĩ': 'i4', 'ị':'i5',
                    'ò': 'o2', 'ó':'o1', 'ỏ': 'o3', 'õ': 'o4', 'ọ': 'o5',
                    'ô': 'o6', 'ồ': ['o62', 'o26'], 'ố': ['o61', 'o16'], 'ổ': ['o63', 'o36'], 'ỗ': ['o64', 'o46'], 'ộ': ['o65', 'o56'],
                    'ơ': 'o7', 'ờ': ['o72', 'o27'], 'ớ': ['o71', 'o17'], 'ở': ['o73', 'o37'], 'ỡ': ['o74', 'o47'], 'ợ': ['o75', 'o57'],
                    'ù': 'u2', 'ú': 'u1', 'ủ': 'u3', 'ũ': 'u4', 'ụ': 'u5',
                    'ư': 'u7', 'ừ': ['u72', 'u27'], 'ứ': ['u71', 'u17'], 'ử': ['u73', 'u37'], 'ữ': ['u74', 'u47'], 'ự': ['u75', 'u57'],
                    'ỳ': 'y2', 'ý': 'y1', 'ỷ': 'y3', 'ỹ': 'y4', 'ỵ': 'y5',
                    'đ': 'd9'
                    }
        vni_word = ''
        for char in word: 
            if char.lower() in vni_dict:
                if type(vni_dict[char.lower()]) == list:
                    if random.random() <= 0.8:
                        vni_char = vni_dict[char.lower()][0]
                    else:
                        vni_char = vni_dict[char.lower()][1]
                else:
                    vni_char = vni_dict[char.lower()]
                if char.isupper():
                        vni_char = vni_char.title()
                vni_word += vni_char 
            else:
                vni_word += char
        if vni_word == word:
            return [word, 0]
        else:
            return [vni_word,2] 
    
    def Mising_Diacritical_Marks(self, word):
        non_diacritical_mark_dict = {
            'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
            'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
            'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
            'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
            'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
            'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
            'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
            'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
            'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
            'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
            'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
            'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
            'đ': 'd'
        }
        non_diacritic_word = ''
        for char in word:
            if char.lower() in non_diacritical_mark_dict:
                new_char = non_diacritical_mark_dict[char.lower()]
                if char.isupper():
                    new_char = new_char.title()    
                non_diacritic_word += new_char
            else:
                non_diacritic_word += char
        if non_diacritic_word == word:
            return [word, 0]
        else:
            return [non_diacritic_word,3] 
    
    def Excess_Letter_Error(self,word):
        excess_letter_word = word
        vowels = ['a', 'e', 'i', 'o', 'u','y']
        consonants = ['b', 'c', 'd', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x']
        length = random.randint(1, 2)
        for i in range(length):
            if word[-1] in vowels:
                if random.random() < 0.7:
                    excess_letter_word += random.choice(consonants)
                else:
                    excess_letter_word += random.choice(vowels)
            else:
                if random.random() < 0.7:
                    excess_letter_word += random.choice(vowels)
                else:
                    excess_letter_word += random.choice(consonants)
        if excess_letter_word == word:
            return [word, 0]
        else:
            return [excess_letter_word,4]
        
    def Missing_Letter_Error(self, word):
        if len(word) == 1:
            return [word,0]
        else:
            length = 1
            indices = random.sample(range(len(word)), length) 
            missing_letter_word = ''
            for i in range(len(word)):
                if i in indices:
                    missing_letter_word += '_'
                else:
                    missing_letter_word += word[i]
            missing_letter_word = missing_letter_word.replace("_",'')
            return [missing_letter_word,5]

    # Wrong Spelling Error
    def get_first_letters(self, word, types_error):
        found = False
        first_letters = []
        for letter in types_error.keys():
            if letter in word[:len(letter)]:
                first_letters.append(letter)
                found = True
                break
        if not found:
            first_letters.append(None)
        return first_letters
    def random_first_letter(self, word):
        true_word = word
        types_error = {'d': 'gi',
                        'gi': 'd',
                        'l': 'r',
                        'r': 'l',
                        'b': 'p',
                        'p': 'b',
                        'x': 's',
                        's': 'x',
                        'ch': 'tr',
                        'k': 'c',
                        'tr': 'ch'}
        
        letter = self.get_first_letters(word, types_error)[0]
        if letter != None:
            word = word.replace(letter,types_error[letter])
        if word == true_word:
            return [true_word, 0]
        else:
            return [word,6]     
    def Wrong_Spelling_Error(self, word):
        return self.random_first_letter(word)
    
    def get_error(self, text, type_error = 0):
        match (type_error):
            case 0:
                return self.No_Error(text)
            case 1:
                return self.Telex_Typing_Error(text)
            case 2:
                return self.VNI_Typing_Error(text)
            case 3:
                return self.Mising_Diacritical_Marks(text)
            case 4:
                return self.Excess_Letter_Error(text)
            case 5:
                return self.Missing_Letter_Error(text)
            case 6:
                return self.Wrong_Spelling_Error(text)
            case default:
                return self.No_Error(text)

    
    def remove_punctuation(self, input_string):
        out_string = re.sub(r'[^\w\s]', '', input_string)
        return out_string
    
    def generate(self, data = None,iterations = 1, prob = None):
        if prob == None:
            prob =  [0.00000000000000000,
                     0.14925373134328357,
                     0.14925373134328357,
                     0.14925373134328357,
                     0.14925373134328357,
                     0.14925373134328357,
                     0.25373134328358204]
        if data == None:
            data = self.data
        for idx, text in enumerate(data):
            data[idx] = self.remove_punctuation(text)
            
        rng = np.random.default_rng()
        for iteration in tqdm(range(iterations)):
            for text in data:
                out_text = text.split()
                label = [0]*len(out_text)
                wrong_percent = len(out_text)*40//100
                random_word_idx = np.random.choice(np.arange(0, len(out_text)), size=wrong_percent, replace=False)
                for i, word in enumerate(out_text):
                    if i not in random_word_idx:
                        out_text[i], label[i] = [word,0]
                    else:
                        type_error = rng.choice(7, 1, p = prob)
                        out_text[i], label[i] = self.get_error(word, type_error)
                        type_err = self.label2id.get(label[i])
                        self.error_counts[type_err] = self.error_counts[type_err] + 1
                
                gen_data = " ".join(out_text)
                gen_label = (out_text, label)
                self.generated_data.append((gen_data,text))
                self.generated_label.append(gen_label)
        return "Generated data!"
      
    def get_data(self):
        tokens, error_col, type_err_col = [], [], []
        input_data, target_data = [], [] 
        
        for data in self.generated_data:
            input_data.append(data[0])
            target_data.append(data[1])
            
        for token, errors in self.generated_label:
            tokens.append(token)
            error_col.append(errors)
        
        return dict(input_text = input_data,
                    target_text = target_data,
                    tokens = tokens,
                    tags = error_col,
                    )
        
    def get_data_info(self):
        num_spacing = len('Missing Diacritical Marks') + 2
        print(f"Length of generated dataset: {len(self.generated_data)} \n \n")
        print("Number of errors in each type: ")
        for key, item in self.error_counts.items():
            print(f"{key:<{num_spacing}}:   {item}")
        