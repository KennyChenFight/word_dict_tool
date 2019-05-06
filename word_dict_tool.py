from dictionary import WordDictionary

import sys
from word_dict_tool_ui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton, QMainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pb_search_sentence.clicked.connect(self.search_sentence_click)
        self.ui.le_search_sentence.returnPressed.connect(self.search_sentence_click)
        self.ui.pb_mark_phonetic.clicked.connect(self.mark_phonetic_click)
        self.ui.pb_add_sentence.clicked.connect(self.add_sentence_to_dict_click)
        self.ui.le_add_sentence.returnPressed.connect(self.add_sentence_to_dict_click)
        self.ui.pb_alter_sentence_and_pron.clicked.connect(self.alter_sentence_and_pron_click)
        self.ui.le_alter_sentence.returnPressed.connect(self.alter_sentence_and_pron_click)

    def search_sentence_click(self):
        sentence = self.ui.le_search_sentence.text()
        if sentence == '':
            QMessageBox.warning(self,
                                '>_<',
                                '你沒有輸入字詞喔~',
                                QMessageBox.Yes)
        else:
            sentence_pron_dict = WordDictionary.search_sentence(sentence)
            self.ui.tb_sentence_list.setText('')

            all = ''
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
                all += sentence_all
            else:
                all += '找不到該字詞!'
            self.ui.tb_sentence_list.setText(all)
            self.ui.tb_sentence_list.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
            self.ui.tb_sentence_list.horizontalScrollBar().setValue(0)

    def mark_phonetic_click(self):
        prons = self.ui.te_mark_list.toPlainText()
        if prons == '':
            QMessageBox.warning(self,
                                '>_<',
                                '你沒有輸入拼音喔~',
                                QMessageBox.Yes)
        else:
            pron_list = prons.split('\n')
            phonetic_collection = WordDictionary.mark_phonetic(pron_list)

            message = ''

            for phonetic_list in phonetic_collection:
                if phonetic_list:
                    message += ''.join(phonetic_list) + '\n'
                else:
                    message += '找不到拼音' + '\n'
            self.ui.tb_mark_list.setText(message)

    def add_sentence_to_dict_click(self):
        sentence = self.ui.le_add_sentence.text()
        prons = self.ui.te_add_sentence_pron_list.toPlainText()
        if sentence == '' or prons == '':
            QMessageBox.warning(self,
                                '>_<',
                                '你沒有輸入字詞或拼音喔~',
                                QMessageBox.Yes)
        else:
            pron_list = prons.split('\n')
            info = WordDictionary.add_sentence_to_word_dict(sentence, pron_list)

            QMessageBox.information(self,
                                    '>_<',
                                    info,
                                    QMessageBox.Yes)

    def alter_sentence_and_pron_click(self):
        sentence = self.ui.le_alter_sentence.text()
        prons = self.ui.te_alter_sentence_pron_list.toPlainText()
        if sentence == '' or prons == '':
            QMessageBox.warning(self,
                                '>_<',
                                '你沒有輸入字詞或拼音喔~',
                                QMessageBox.Yes)
        else:
            new_pron_list = prons.split('\n')
            odd_pron_list = WordDictionary.find_sentence_pron(sentence)

            if not odd_pron_list:
                QMessageBox.warning(self,
                                    '>_<',
                                    '找不到該字詞，無法修改!',
                                    QMessageBox.Yes)
            else:
                new_prons = '\n'.join(new_pron_list)
                odd_prons = '\n'.join(odd_pron_list)

                msgBox = QMessageBox()
                msgBox.setText('舊的拼音如下:' + '\n' +
                               odd_prons + '\n' +
                               '新的拼音如下:' + '\n' +
                               new_prons + '\n')
                msgBox.addButton(QPushButton('修改'), QMessageBox.YesRole)
                msgBox.addButton(QPushButton('不修改'), QMessageBox.NoRole)
                ret = msgBox.exec()

                if ret == 0:
                    WordDictionary.alter_sentence_and_pron(sentence, new_pron_list)
                    QMessageBox.information(self,
                                            '>_<',
                                            '修改成功!',
                                            QMessageBox.Yes)

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())



# sentence = '銷售'
# sentence_dict = WordDictionary.search_sentence(sentence)
# print(sentence_dict)

# sentence = ['hu aL aH', 'tz aiL aiL']
# phonetic_list = WordDictionary.mark_phonetic(sentence)
# print(phonetic_list)
#
# sentence = '華仔'
# pron_list = ['hu aL aH', 'tz aiL aiL']
# WordDictionary.add_sentence_to_word_dict(sentence, pron_list)

# sentence = '華仔'
# new_pron_list = ['hu aL aH', 'tz aiL aiL']
# odd_pron_list = WordDictionary.find_sentence_pron(sentence)
# print('舊的拼音:', odd_pron_list)
# WordDictionary.alter_sentence_and_pron(sentence, new_pron_list)

# WordDictionary.sort_by_words_position2('1', '華')
