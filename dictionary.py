import logging
from datetime import datetime
import os
from itertools import groupby
from itertools import permutations
import re
import operator

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_file_name = 'log/' + 'info' + '.log'
handler = logging.FileHandler(log_file_name, 'w+', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)


class WordDictionary:

    dict_file = 'WordData_1227.txt'
    phonetic_table = 'data/phonetic_compare.txt'
    tone_table = 'data/tone_compare.txt'

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

        sentence_pron_dict = cls.find_all_contain_sentence(sentence, sentence_pron_dict)
        return sentence_pron_dict

    @classmethod
    def find_all_contain_sentence(cls, sentence, sentence_pron_dict):
        sentence_pron_dict = {text: pron for text, pron in sentence_pron_dict.items() if sentence in text}
        sentence_list = sorted(sentence_pron_dict.keys(), key=lambda x: len(x), reverse=True)

        if sentence_list and sentence_list[-1] == sentence:
            sentence = sentence_list.pop(-1)
            sentence_list.insert(0, sentence)

        result = {}
        sentences = cls.sort_by_words_position(sentence_list, sentence)
        for sentence in sentences:
            result[sentence] = sentence_pron_dict[sentence]
        return result

    @classmethod
    def sort_by_words_position(cls, sentence_list, sentence):
        group_by_len = [list(g) for k, g in groupby(sentence_list, key=len)]

        sorted_group = []
        for group in group_by_len:
            temp_dict = {}
            for word in group:
                temp_list = [m.start() for m in re.finditer(sentence, word)]
                temp_dict[word] = temp_list[0]
            sorted_group.append(temp_dict)

        result = []
        for group in sorted_group:
            sorted_dict = sorted(group.items(), key=operator.itemgetter(1))
            for word, show_index in sorted_dict:
                result.append(word)

        return result

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
                    phonetic_sentence_list.append([])
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
                # collection.append(phonetic_sentence[1])
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
        word_dict = {}
        info = ''
        with open(cls.dict_file, 'r', encoding='utf-8') as f:
            line_count = 1
            for line in f:
                line = line.strip().split(',')[0]
                word_dict[line_count] = line
                line_count += 1

        fit_first_word_dict = {}
        for line_count, word in word_dict.items():
            if word[0] == sentence[0]:
                fit_first_word_dict[line_count] = word

        if not fit_first_word_dict:
            info += '沒有' + '"' + sentence[0] + '"' + '為字首之任何字詞' + '\n'
            info += '無法新增' + '\n'
        else:
            fit_length_word_dict = {}
            already_exists_sentence = False
            exists_single_word = False
            for line_count, word in fit_first_word_dict.items():
                if len(word) == 1:
                    exists_single_word = True
                if word == sentence:
                    already_exists_sentence = True
                elif len(word) == len(sentence):
                    fit_length_word_dict[line_count] = word

            if already_exists_sentence:
                info += '已存在這個字詞' + '\n'
            elif len(sentence) > 1:
                if fit_length_word_dict:
                    line_count, word = fit_length_word_dict.popitem()
                    new_line_count = line_count + 1
                    cls.add_new_line_content(new_line_count, sentence, pron_list)
                else:
                    greater_than_len_words_line_count = [line_count for line_count, word in fit_first_word_dict.items() if len(word) > len(sentence)]
                    if greater_than_len_words_line_count:
                        new_line_count = greater_than_len_words_line_count[-1] + 1
                        cls.add_new_line_content(new_line_count, sentence, pron_list)
                    else:
                        less_than_len_words_line_count = [line_count for line_count, word in fit_first_word_dict.items() if len(word) < len(sentence)]
                        new_line_count = less_than_len_words_line_count[0]
                        cls.add_new_line_content(new_line_count, sentence, pron_list)
                info += '新增成功' + '\n'

            if not exists_single_word:
                info += '無' + '"' + sentence[0] + '"' + '單字詞' + '\n'
                info += '提醒:可加' + '"' + sentence[0] + '"' + '\n'

        return info
    @classmethod
    def add_new_line_content(cls, new_line_count, sentence, pron_list):
        with open(cls.dict_file, encoding='utf-8') as i, open('test.txt', 'w', encoding='utf-8') as o:
            line_count = 1
            for line in i:
                if line_count == new_line_count:
                    o.write(sentence)
                    o.write(',')
                    o.write(','.join(pron_list))
                    for index in range(0, 10 - len(sentence)):
                        o.write(',')
                    o.write('\n')
                    o.write(line)
                else:
                    o.write(line)
                line_count += 1
        os.remove(cls.dict_file)
        os.rename('test.txt', cls.dict_file)
        logger.info('在第' + str(new_line_count) + '行' + '添加:' + sentence)

    @classmethod
    def find_sentence_pron(cls, sentence):
        with open(cls.dict_file, encoding='utf-8') as f:
            for line in f:
                line = line.strip().split(',')
                line = [item for item in line if item != '']
                word = line[0]
                pron_list = line[1:]
                if word == sentence:
                    return pron_list

    @classmethod
    def alter_sentence_and_pron(cls, sentence, pron_list):
        with open(cls.dict_file, encoding='utf-8') as i, open('test.txt', 'w', encoding='utf-8') as o:
            line_count = 1
            for line in i:
                word = line.split(',')[0]
                if word == sentence:
                    specific_line_count = line_count
                    o.write(sentence)
                    o.write(',')
                    o.write(','.join(pron_list))
                    for index in range(0, 10 - len(sentence)):
                        o.write(',')
                    o.write('\n')
                else:
                    o.write(line)
                line_count += 1

        os.remove(cls.dict_file)
        os.rename('test.txt', cls.dict_file)
        logger.info('在第' + str(specific_line_count) + '行' + '修改' + '"' + sentence + '"' + '的拼音')
