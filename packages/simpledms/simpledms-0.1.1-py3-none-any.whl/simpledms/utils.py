"""Classes which are needed in main GUI."""
import re

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from ui.editrules import Ui_Dialog


class MyDictionaryCompleter(QtWidgets.QCompleter):
    insertText = QtCore.pyqtSignal(str)

    def __init__(self, myKeywords=None, parent=None):
        QtWidgets.QCompleter.__init__(self, myKeywords, parent)

    def changeCompletion(self, completion):
        if completion.find("(") != -1:
            completion = completion[: completion.find("(")]
        print(completion)
        self.insertText.emit(completion)


class MyTextEdit(QtWidgets.QTextEdit):
    def __init__(self, *args):
        super(MyTextEdit, self).__init__()
        # *args to set parent
        QtWidgets.QLineEdit.__init__(self, *args)
        self.completer = None

    def setCompleter(self, completer):
        # if self.completer:
        #    self.disconnect(self.completer, 0, self, 0)
        if not completer:
            return

        completer.setWidget(self)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:] + ", ")
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QtWidgets.QTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        if (
            self.completer
            and self.completer.popup()
            and self.completer.popup().isVisible()
        ):
            if event.key() in (
                QtCore.Qt.Key_Enter,
                QtCore.Qt.Key_Return,
                QtCore.Qt.Key_Escape,
                QtCore.Qt.Key_Tab,
                QtCore.Qt.Key_Backtab,
            ):
                event.ignore()
                return
        # has ctrl-Space been pressed??
        isShortcut = (
            event.modifiers() == QtCore.Qt.ControlModifier
            and event.key() == QtCore.Qt.Key_Space
        )
        m = re.search(r"\w{1,}$", self.toPlainText() + event.text())
        if m and len(m.group(0)) > 1:
            isShortcut = True
            QtWidgets.QTextEdit.keyPressEvent(self, event)

        if not self.completer or not isShortcut:
            pass
            QtWidgets.QTextEdit.keyPressEvent(self, event)

        ctrlOrShift = event.modifiers() in (
            QtCore.Qt.ControlModifier,
            QtCore.Qt.ShiftModifier,
        )
        if ctrlOrShift and event.text() == "":
            return

        completionPrefix = self.textUnderCursor()

        if not isShortcut:
            if self.completer.popup():
                self.completer.popup().hide()
            return
        # print("complPref: {}".format(completionPrefix))
        # print("completer.complPref: {}".format(self.completer.completionPrefix()))
        # print("mode: {}".format(self.completer.completionMode()))
        # if (completionPrefix != self.completer.completionPrefix()):
        self.completer.setCompletionPrefix(completionPrefix)
        popup = self.completer.popup()
        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
        cr = self.cursorRect()
        cr.setWidth(
            self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width()
        )
        self.completer.complete(cr)  # popup it up!


class MyRulesWidget(QtWidgets.QDialog, Ui_Dialog):
    def __init__(
        self,
        parent=None,
        keywords=None,
        booleanoperator=None,
        tags=None,
        doctitle=None,
        indexertags=None,
    ):
        super(MyRulesWidget, self).__init__(parent)
        self.keywords = keywords
        self.tags = tags
        self.booleanoperator = booleanoperator
        self.doctitle = doctitle
        self.textkeyexist = False
        self.doctitleexist = False
        self.setupUi(self)
        self.textEdit_keywords.setPlainText(keywords)

        self.lineEdit_doctitle.setText(doctitle)
        if booleanoperator == "ANY":
            self.radioButton_any.setChecked(True)

        completer = MyDictionaryCompleter(myKeywords=indexertags)
        self.textEdit_tags = MyTextEdit(self.textEdit_tags)
        self.textEdit_tags.setCompleter(completer)
        self.textEdit_tags.setPlainText(tags)

        self.textEdit_keywords.textChanged.connect(self.textEdit_keywords_changed)
        self.lineEdit_doctitle.textChanged.connect(self.lineEdit_doctitle_changed)
        self.textEdit_tags.textChanged.connect(self.textEdit_tags_changed)
        self.pushButton_ok.clicked.connect(self.closedialogok)
        self.pushButton_cancel.clicked.connect(self.closedialogcancel)

        if keywords:
            self.textkeyexist = True
        if doctitle:
            self.doctitleexist = True
        if self.textkeyexist and self.doctitleexist:
            self.pushButton_ok.setEnabled(True)

    def textEdit_tags_changed(self):
        self.tags = re.split(r"[;,\s]\s*", self.textEdit_tags.toPlainText())

    def textEdit_keywords_changed(self):
        self.keywords = self.textEdit_keywords.toPlainText()
        if self.textEdit_keywords.toPlainText():
            self.textkeyexist = True
        else:
            self.textkeyexist = False

        if self.textkeyexist and self.doctitleexist:
            self.pushButton_ok.setEnabled(True)
        else:
            self.pushButton_ok.setEnabled(False)

    def lineEdit_doctitle_changed(self):
        self.doctitle = self.lineEdit_doctitle.text()
        if self.lineEdit_doctitle.text():
            self.doctitleexist = True
        else:
            self.doctitleexist = False

        if self.textkeyexist and self.doctitleexist:
            self.pushButton_ok.setEnabled(True)
        else:
            self.pushButton_ok.setEnabled(False)

    def closedialogok(self):
        if self.radioButton_all.isChecked():
            self.booleanoperator = "ALL"
        else:
            self.booleanoperator = "ANY"
        self.keywords = re.split(r"[;,\s]\s*", self.keywords)
        tags = self.textEdit_tags.toPlainText()
        tags = tags.strip(", ")
        self.tags = re.split(r"[;,\s]\s*", tags)
        print(self.tags)
        print(type(self.tags))
        self.doctitle = self.lineEdit_doctitle.text()
        self.accept()

    def closedialogcancel(self):
        self.reject()
