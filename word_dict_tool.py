from dictionary import WordDictionary

# sentence = '華仔'
# sentence_list = WordDictionary.search_sentence(sentence)
# print(sentence_list)

# sentence = ['hu aL aH', 'tz aiL aiL']
# phonetic_list = WordDictionary.mark_phonetic(sentence)
# print(phonetic_list)
#
sentence = '華而'
pron_list = ['hu aL aH', 'tz aiL aiL']
WordDictionary.add_sentence_to_word_dict(sentence, pron_list)