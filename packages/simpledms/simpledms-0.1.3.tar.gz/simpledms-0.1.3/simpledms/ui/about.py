# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'about.ui'
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
        Dialog.resize(561, 266)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_info_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setLocale(
            QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany)
        )
        self.label_4.setText("")
        self.label_4.setPixmap(
            QtGui.QPixmap(":/icons/icons/outline_info_white_18dp.png")
        )
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 2, 1, 2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Bitstream Charter")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 2)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 2)

        self.retranslateUi(Dialog)
        self.buttonBox.clicked["QAbstractButton*"].connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About this Program"))
        self.label.setText(
            _translate(
                "Dialog", "Images: https://github.com/google/material-design-icons"
            )
        )
        self.label_3.setText(_translate("Dialog", "Simple Document Management System"))
        self.label_2.setText(_translate("Dialog", "Author: Tobias Wartzek, 2019"))
