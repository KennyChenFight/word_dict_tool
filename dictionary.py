class WordDictionary:

    dict_file = 'WordData_1227.txt'
    phonetic_table = 'phonetic_compare.txt'
    tone_table = 'tone_compare.txt'

    @classmethod
    def search_sentence(cls, sentence):
        sentence_pron_dict = {}
        with open(cls.dict_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().split(',')
                line = [item for item in line if item != '']

                text = line[0]
                if text in sentence_pron_dict:
                    print('Oops! repeated text:', text)
                else:
                    sentence_pron_dict[text] = line[1:]

        sentence_list = cls.find_all_contain_sentence(sentence, sentence_pron_dict)
        return sentence_list

    @classmethod
    def find_all_contain_sentence(cls, sentence, sentence_pron_dict):
        sentence_pron_dict = {text: pron for text, pron in sentence_pron_dict.items() if sentence in text}
        sentence_list = sorted(sentence_pron_dict.keys(), key=lambda x: len(x), reverse=True)

        if sentence_list and sentence_list[-1] == sentence:
            sentence = sentence_list.pop(-1)
            sentence_list.insert(0, sentence)
        return sentence_list

    @classmethod
    def mark_phonetic(cls, pron_sentence_list):
        phonetic_table, tone_table = cls.read_phonetic_tone_table()
        print(phonetic_table)
        print(tone_table)

        phonetic_sentence_list = []
        for pron_sentence in pron_sentence_list:
            phonetic_sentence = []
            pron_sentence = pron_sentence.split(' ')
            phonetic_sentence.append(len(pron_sentence))
            for pron in pron_sentence:
                not_exist_pron = True
                for phonetic, compare_pron in phonetic_table.values():
                    if pron == compare_pron:
                        not_exist_pron = False
                        phonetic_sentence.append(phonetic)
                        phonetic_sentence.append(compare_pron[-1])
                print(not_exist_pron)
                if not_exist_pron:
                    phonetic_sentence = []
                    break

            print(phonetic_sentence)
            collection = []
            if phonetic_sentence and phonetic_sentence[0] == 3:
                collection.append(phonetic_sentence[1])
                collection.append(phonetic_sentence[3])
                for tail_pron, tone in tone_table.items():
                    tail = phonetic_sentence[4] + phonetic_sentence[6]
                    if tail_pron == tail:
                        collection.append(tone)
                phonetic_sentence_list.append(collection)
            elif phonetic_sentence and phonetic_sentence[0] == 2:
                collection.append(phonetic_sentence[1])
                collection.append(phonetic_sentence[3])
                for tail_pron, tone in tone_table.items():
                    tail = phonetic_sentence[2] + phonetic_sentence[4]
                    if tail_pron == tail:
                        collection.append(tone)
                phonetic_sentence_list.append(collection)

        return phonetic_sentence_list

    @classmethod
    def read_phonetic_tone_table(cls):
        phonetic_table = {}
        with open(cls.phonetic_table, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().split(',')
                phonetic_table[line[0]] = [line[1], line[2]]

        tone_table = {}
        with open(cls.tone_table, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().split(',')
                tone_table[line[0] + line[1]] = line[2]
        return phonetic_table, tone_table

    @classmethod
    def add_sentence_to_word_dict(cls, sentence, pron_list):
        with open(cls.dict_file, 'r', encoding='utf-8') as f:
            text_list = []
            for line in f:
                line = line.strip().split(',')
                line = [item for item in line if item != '']

                text = line[0]
                size = len(sentence)
                if sentence in text and len(sentence) == len(text):
                    text_list.append(text)
            print(text_list)