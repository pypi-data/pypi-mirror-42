# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'editrules.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(321, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_description_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        Dialog.setWindowIcon(icon)
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_ok = QtWidgets.QPushButton(Dialog)
        self.pushButton_ok.setEnabled(False)
        self.pushButton_ok.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_check_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButton_ok.setIcon(icon1)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.gridLayout.addWidget(self.pushButton_ok, 15, 1, 1, 1)
        self.radioButton_any = QtWidgets.QRadioButton(Dialog)
        self.radioButton_any.setObjectName("radioButton_any")
        self.gridLayout.addWidget(self.radioButton_any, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)
        self.textEdit_keywords = QtWidgets.QTextEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textEdit_keywords.sizePolicy().hasHeightForWidth()
        )
        self.textEdit_keywords.setSizePolicy(sizePolicy)
        self.textEdit_keywords.setMinimumSize(QtCore.QSize(0, 50))
        self.textEdit_keywords.setAcceptRichText(False)
        self.textEdit_keywords.setObjectName("textEdit_keywords")
        self.gridLayout.addWidget(self.textEdit_keywords, 5, 0, 4, 2)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 9, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.radioButton_all = QtWidgets.QRadioButton(Dialog)
        self.radioButton_all.setChecked(True)
        self.radioButton_all.setObjectName("radioButton_all")
        self.gridLayout.addWidget(self.radioButton_all, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 11, 0, 1, 1)
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setEnabled(True)
        self.pushButton_cancel.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_cancel_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButton_cancel.setIcon(icon2)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.gridLayout.addWidget(self.pushButton_cancel, 15, 0, 1, 1)
        self.textEdit_tags = QtWidgets.QTextEdit(Dialog)
        self.textEdit_tags.setObjectName("textEdit_tags")
        self.gridLayout.addWidget(self.textEdit_tags, 10, 0, 1, 2)
        self.lineEdit_doctitle = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_doctitle.setObjectName("lineEdit_doctitle")
        self.gridLayout.addWidget(self.lineEdit_doctitle, 12, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit rules"))
        self.pushButton_ok.setToolTip(
            _translate("Dialog", "Keywords and title need to be filled.")
        )
        self.radioButton_any.setText(_translate("Dialog", "ANY"))
        self.label_7.setText(_translate("Dialog", "of the following keywords"))
        self.label_2.setText(_translate("Dialog", "Set these tags"))
        self.label_3.setText(_translate("Dialog", "If the document contains"))
        self.radioButton_all.setText(_translate("Dialog", "ALL"))
        self.label_4.setText(_translate("Dialog", "and set this document title:"))
