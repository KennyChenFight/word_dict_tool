import logging
from datetime import datetime
from itertools import groupby
import re
import operator
from filelock import FileLock

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_file_name = 'log/' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.log'
handler = logging.FileHandler(log_file_name, 'w+', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)


class WordDictionary:

    lock_dict_file = 'WordData_1227.txt.lock'
    dict_file = 'WordData_1227.txt'
    phonetic_table = 'data/phonetic_compare.txt'
    tone_table = 'data/tone_compare.txt'

    # 在字典檔裡尋找符合的字詞
    @classmethod
    def search_sentence(cls, sentence):
        sentence_pron_dict = {}
        with open(cls.dict_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().split(',')
                line = [item for item in line if item != '']

                text = line[0]
                if text in sentence_pron_dict:
                    logger.debug('Oops! repeated text:', text)
                else:
                    sentence_pron_dict[text] = line[1:]

        sentence_pron_dict = cls.find_all_contain_sentence(sentence, sentence_pron_dict)

        message = ''
        if sentence_pron_dict:
            sentence_all = ''
            for word, pron in sentence_pron_dict.items():
                word_index = word.find(sentence)
                color_sentence = word.replace(sentence,
                                              '<span style=\" color: #ff0000;\">%s</span>' % str(sentence), 1)

                for i in range(word_index, word_index + len(sentence)):
                    pron[i] = '<span style=\" color: #ff0000;\">%s</span>' % str(pron[i])
                color_pron = ','.join(pron)

                sentence_all += color_sentence + ',' + color_pron + '<br>'
            message += sentence_all
        else:
            message += '找不到該字詞!'
        return message

    # 找到所有句子裡包含特定的詞語
    @classmethod
    def find_all_contain_sentence(cls, sentence, sentence_pron_dict):
        sentence_pron_dict = {text: pron for text, pron in sentence_pron_dict.items() if sentence in text}
        sentence_list = sorted(sentence_pron_dict.keys(), key=lambda x: len(x), reverse=True)

        if sentence_list and sentence_list[-1] == sentence:
            sentence = sentence_list.pop(-1)
            sentence_list.insert(0, sentence)

        result = {}
        #sentences = cls.sort_by_words_position(sentence_list, sentence)
        sentences = cls.sort_by_words_position2(sentence_list, sentence)
        for sentence in sentences:
            result[sentence] = sentence_pron_dict[sentence]
        return result

    # 將字進行排序，根據句子的長度
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

    # 將字進行排序，根據特定字出現在句子裡面的順序
    @classmethod
    def sort_by_words_position2(cls, sentence_list, sentence):
        result = []
        if sentence_list:
            max_length = len(max(sentence_list, key=len))
            for i in range(max_length):
                for s in sentence_list:
                    find_index = s.find(sentence)
                    if find_index != -1 and find_index == i:
                        if s not in result:
                            result.append(s)
        return result

    # 標註注音
    @classmethod
    def mark_phonetic(cls, pron_sentence_list):
        phonetic_table, tone_table = cls.read_phonetic_tone_table()
        logger.debug(phonetic_table)
        logger.debug(tone_table)

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
                logger.debug(not_exist_pron)
                if not_exist_pron:
                    phonetic_sentence = []
                    phonetic_sentence_list.append([])
                    break

            logger.debug(phonetic_sentence)
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

        message = ''

        for phonetic_list in phonetic_sentence_list:
            if phonetic_list:
                message += ''.join(phonetic_list) + '\n'
            else:
                message += '找不到拼音' + '\n'

        return message

    # 讀取注音音調表
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

    # 新增字詞到字典檔
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
            else:
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

            if not exists_single_word and len(sentence) > 1:
                info += '無' + '"' + sentence[0] + '"' + '單字詞' + '\n'
                info += '提醒:可加' + '"' + sentence[0] + '"' + '\n'

        return info

    # 用檔案方式新增多個字詞到字典檔
    @classmethod
    def add_multiple_sentence(cls, filepath):
        sentence_pron_dict = {}
        with open(filepath, encoding='utf-8') as f:
            sentence = ''
            pron_list = []
            for line in f:
                line = line.strip()
                test_line = line.replace(' ', '')
                if len(test_line) != 0 and not test_line.encode().isalpha():
                    sentence = line
                if test_line.encode().isalpha():
                    pron_list.append(line)
                if len(test_line) == 0:
                    sentence_pron_dict[sentence] = pron_list
                    pron_list = []
            sentence_pron_dict[sentence] = pron_list
        print(sentence_pron_dict)

        message = []
        for sentence, pron_list in sentence_pron_dict.items():
            info = cls.add_sentence_to_word_dict(sentence, pron_list)
            if '已存在這個字詞' in info:
                message.append(sentence + ':已存在這個字詞')
            elif '新增成功' in info:
                message.append(sentence + ':新增成功')
            else:
                message.append(info)
        return message

    # 新增句子
    @classmethod
    def add_new_line_content(cls, new_line_count, sentence, pron_list):
        lock = FileLock(cls.lock_dict_file, timeout=2)
        with lock:
            collect = []
            with open(cls.dict_file, encoding='utf-8') as i:
                line_count = 1
                for line in i:
                    if line_count == new_line_count:
                        collect.append(sentence)
                        collect.append(',')
                        collect.append(','.join(pron_list))
                        for index in range(0, 10 - len(sentence)):
                            collect.append(',')
                        collect.append('\n')
                        collect.append(line)
                    else:
                        collect.append(line)
                    line_count += 1
            message = ''.join(collect)
            with open(cls.dict_file, 'w', encoding='utf-8') as o:
                o.write(message)
            logger.info('在第' + str(new_line_count) + '行' + '添加:' + sentence)

    # 找到該句子的拼音
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

    # 修改該句子的拼音
    @classmethod
    def alter_sentence_and_pron(cls, sentence, pron_list):
        lock = FileLock(cls.lock_dict_file, timeout=2)
        with lock:
            collect = []
            with open(cls.dict_file, encoding='utf-8') as i:
                line_count = 1
                for line in i:
                    word = line.split(',')[0]
                    if word == sentence:
                        specific_line_count = line_count
                        collect.append(sentence)
                        collect.append(',')
                        collect.append(','.join(pron_list))
                        for index in range(0, 10 - len(sentence)):
                            collect.append(',')
                        collect.append('\n')
                    else:
                        collect.append(line)
                    line_count += 1
            message = ''.join(collect)
            with open(cls.dict_file, 'w', encoding='utf-8') as o:
                o.write(message)
            logger.info('在第' + str(specific_line_count) + '行' + '修改' + '"' + sentence + '"' + '的拼音')
        return '修改成功!'
