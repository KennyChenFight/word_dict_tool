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
        self.ui.pb_add_mutiple_sentence.clicked.connect(self.add_multiple_sentence_to_dict_click)
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
            message = WordDictionary.search_sentence(sentence)
            self.ui.tb_sentence_list.setText('')
            self.ui.tb_sentence_list.setText(message)
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
            message = WordDictionary.mark_phonetic(pron_list)
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
            if len(pron_list) == len(sentence):
                info = WordDictionary.add_sentence_to_word_dict(sentence, pron_list)

                QMessageBox.information(self,
                                        '>_<',
                                        info,
                                        QMessageBox.Yes)
            else:
                QMessageBox.warning(self,
                                    '>_<',
                                    '字詞跟拼音數量不一致喔',
                                    QMessageBox.Yes)

    def add_multiple_sentence_to_dict_click(self):
        filepath, filetype = QFileDialog. \
            getOpenFileName(self,
                            "選取文件",
                            "./",
                            "Text Files (*.txt)")
        messages = WordDictionary.add_multiple_sentence(filepath)

        QMessageBox.information(self,
                                '>_<',
                                '\n'.join(messages),
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
            if len(new_pron_list) == len(sentence):
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
                        message = WordDictionary.alter_sentence_and_pron(sentence, new_pron_list)
                        QMessageBox.information(self,
                                                '>_<',
                                                message,
                                                QMessageBox.Yes)
            else:
                QMessageBox.warning(self,
                                    '>_<',
                                    '字詞跟拼音數量不一致喔',
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

# WordDictionary.add_multiple_sentence('test.txt')
