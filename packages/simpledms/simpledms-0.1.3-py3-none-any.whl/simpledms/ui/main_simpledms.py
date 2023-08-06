# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'main_simpledms.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1070, 664)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_description_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(
            QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany)
        )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_pdfrename = QtWidgets.QWidget()
        self.page_pdfrename.setObjectName("page_pdfrename")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_pdfrename)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_monitordir = QtWidgets.QLabel(self.page_pdfrename)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_monitordir.setFont(font)
        self.label_monitordir.setObjectName("label_monitordir")
        self.gridLayout_3.addWidget(self.label_monitordir, 0, 0, 1, 1)
        self.label_outputfilename = QtWidgets.QLabel(self.page_pdfrename)
        self.label_outputfilename.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.label_outputfilename.setObjectName("label_outputfilename")
        self.gridLayout_3.addWidget(self.label_outputfilename, 0, 2, 1, 1)
        self.lineEdit_outputfilename = QtWidgets.QLineEdit(self.page_pdfrename)
        self.lineEdit_outputfilename.setObjectName("lineEdit_outputfilename")
        self.gridLayout_3.addWidget(self.lineEdit_outputfilename, 2, 2, 1, 1)
        self.listView_monitorfiles = QtWidgets.QListView(self.page_pdfrename)
        self.listView_monitorfiles.setObjectName("listView_monitorfiles")
        self.gridLayout_3.addWidget(self.listView_monitorfiles, 2, 0, 5, 1)
        self.listWidget_pdfthumbnails = QtWidgets.QListWidget(self.page_pdfrename)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.listWidget_pdfthumbnails.sizePolicy().hasHeightForWidth()
        )
        self.listWidget_pdfthumbnails.setSizePolicy(sizePolicy)
        self.listWidget_pdfthumbnails.setMinimumSize(QtCore.QSize(0, 0))
        self.listWidget_pdfthumbnails.setMaximumSize(QtCore.QSize(300, 16777215))
        self.listWidget_pdfthumbnails.setStyleSheet("")
        self.listWidget_pdfthumbnails.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )
        self.listWidget_pdfthumbnails.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.listWidget_pdfthumbnails.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget_pdfthumbnails.setViewMode(QtWidgets.QListView.IconMode)
        self.listWidget_pdfthumbnails.setObjectName("listWidget_pdfthumbnails")
        self.gridLayout_3.addWidget(self.listWidget_pdfthumbnails, 2, 1, 5, 1)
        self.pushButton_addDate = QtWidgets.QPushButton(self.page_pdfrename)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_addDate.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_addDate.setSizePolicy(sizePolicy)
        self.pushButton_addDate.setMinimumSize(QtCore.QSize(10, 0))
        self.pushButton_addDate.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_addDate.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_calendar_today_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButton_addDate.setIcon(icon1)
        self.pushButton_addDate.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_addDate.setObjectName("pushButton_addDate")
        self.gridLayout_3.addWidget(self.pushButton_addDate, 2, 3, 1, 1)
        self.textEdit_tags = QtWidgets.QTextEdit(self.page_pdfrename)
        self.textEdit_tags.setObjectName("textEdit_tags")
        self.gridLayout_3.addWidget(self.textEdit_tags, 4, 2, 1, 2)
        self.treeView_output = QtWidgets.QTreeView(self.page_pdfrename)
        self.treeView_output.setObjectName("treeView_output")
        self.gridLayout_3.addWidget(self.treeView_output, 5, 2, 1, 2)
        self.pushButton_ok = QtWidgets.QPushButton(self.page_pdfrename)
        self.pushButton_ok.setEnabled(False)
        self.pushButton_ok.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_check_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButton_ok.setIcon(icon2)
        self.pushButton_ok.setAutoDefault(True)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.gridLayout_3.addWidget(self.pushButton_ok, 6, 2, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.page_pdfrename)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 3, 2, 1, 1)
        self.stackedWidget.addWidget(self.page_pdfrename)
        self.page_settings = QtWidgets.QWidget()
        self.page_settings.setObjectName("page_settings")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_settings)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.page_settings)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_pref = QtWidgets.QWidget()
        self.tab_pref.setObjectName("tab_pref")
        self.formLayout = QtWidgets.QFormLayout(self.tab_pref)
        self.formLayout.setObjectName("formLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.formLayout.setItem(0, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.pushButton_setmonitorfolder = QtWidgets.QPushButton(self.tab_pref)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_search_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButton_setmonitorfolder.setIcon(icon3)
        self.pushButton_setmonitorfolder.setObjectName("pushButton_setmonitorfolder")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.pushButton_setmonitorfolder
        )
        self.label_monitorfolder = QtWidgets.QLabel(self.tab_pref)
        self.label_monitorfolder.setObjectName("label_monitorfolder")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.label_monitorfolder
        )
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.formLayout.setItem(2, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        self.pushButton_setdmsroot = QtWidgets.QPushButton(self.tab_pref)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_setdmsroot.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_setdmsroot.setSizePolicy(sizePolicy)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_archive_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButton_setdmsroot.setIcon(icon4)
        self.pushButton_setdmsroot.setObjectName("pushButton_setdmsroot")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.pushButton_setdmsroot
        )
        self.label_dmsroot = QtWidgets.QLabel(self.tab_pref)
        self.label_dmsroot.setObjectName("label_dmsroot")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.label_dmsroot
        )
        self.tabWidget.addTab(self.tab_pref, "")
        self.tab_rules = QtWidgets.QWidget()
        self.tab_rules.setObjectName("tab_rules")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_rules)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_addrule = QtWidgets.QPushButton(self.tab_rules)
        self.pushButton_addrule.setEnabled(False)
        self.pushButton_addrule.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_add_circle_outline_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButton_addrule.setIcon(icon5)
        self.pushButton_addrule.setObjectName("pushButton_addrule")
        self.gridLayout_4.addWidget(self.pushButton_addrule, 2, 2, 1, 1)
        self.treeView_rules = QtWidgets.QTreeView(self.tab_rules)
        self.treeView_rules.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView_rules.setObjectName("treeView_rules")
        self.gridLayout_4.addWidget(self.treeView_rules, 1, 2, 1, 2)
        self.pushButton_deleterule = QtWidgets.QPushButton(self.tab_rules)
        self.pushButton_deleterule.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_remove_circle_outline_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButton_deleterule.setIcon(icon6)
        self.pushButton_deleterule.setAutoDefault(False)
        self.pushButton_deleterule.setDefault(False)
        self.pushButton_deleterule.setFlat(False)
        self.pushButton_deleterule.setObjectName("pushButton_deleterule")
        self.gridLayout_4.addWidget(self.pushButton_deleterule, 2, 3, 1, 1)
        self.treeView_rulesfolders = QtWidgets.QTreeView(self.tab_rules)
        self.treeView_rulesfolders.setObjectName("treeView_rulesfolders")
        self.gridLayout_4.addWidget(self.treeView_rulesfolders, 1, 0, 2, 2)
        self.tabWidget.addTab(self.tab_rules, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_settings)
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1070, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMaximumSize(QtCore.QSize(16666666, 16777215))
        self.toolBar.setAutoFillBackground(True)
        self.toolBar.setStyleSheet("")
        self.toolBar.setMovable(False)
        self.toolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setIconSize(QtCore.QSize(20, 20))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionScan = QtWidgets.QAction(MainWindow)
        self.actionScan.setCheckable(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_scanner_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.actionScan.setIcon(icon7)
        self.actionScan.setObjectName("actionScan")
        self.actionPdf = QtWidgets.QAction(MainWindow)
        self.actionPdf.setCheckable(False)
        self.actionPdf.setIcon(icon4)
        self.actionPdf.setObjectName("actionPdf")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setCheckable(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_settings_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.actionSettings.setIcon(icon8)
        self.actionSettings.setObjectName("actionSettings")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_exit_to_app_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.actionExit.setIcon(icon9)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(
            QtGui.QPixmap(":/icons/icons/outline_info_white_18dp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.actionAbout.setIcon(icon10)
        self.actionAbout.setObjectName("actionAbout")
        self.toolBar.addAction(self.actionPdf)
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionScan)
        self.toolBar.addAction(self.actionAbout)
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Simple Document Management System")
        )
        self.label_monitordir.setText(_translate("MainWindow", "Monitor Directory"))
        self.label_outputfilename.setText(_translate("MainWindow", "Filename"))
        self.lineEdit_outputfilename.setToolTip(
            _translate("MainWindow", "Format: YYYY-MM-DD Documenttitle")
        )
        self.listWidget_pdfthumbnails.setSortingEnabled(False)
        self.pushButton_addDate.setToolTip(
            _translate("MainWindow", "Füge Datum von heute ein")
        )
        self.label_5.setText(_translate("MainWindow", "Tags:"))
        self.pushButton_setmonitorfolder.setText(
            _translate("MainWindow", "Monitor Directory")
        )
        self.label_monitorfolder.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_setdmsroot.setText(
            _translate("MainWindow", "Archive directory")
        )
        self.label_dmsroot.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_pref),
            _translate("MainWindow", "Base Settings"),
        )
        self.treeView_rulesfolders.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Wenn leer, bitte Ordnerstruktur im Archivpfad des Aktenschranks anpassen.</p></body></html>",
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_rules), _translate("MainWindow", "Rules")
        )
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionScan.setText(_translate("MainWindow", "Scan"))
        self.actionScan.setToolTip(
            _translate("MainWindow", "Start script to scan document.")
        )
        self.actionPdf.setText(_translate("MainWindow", "Rename"))
        self.actionPdf.setIconText(_translate("MainWindow", "Rename"))
        self.actionPdf.setToolTip(
            _translate(
                "MainWindow", "Rename pdf and sort into corresponding directory."
            )
        )
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSettings.setToolTip(_translate("MainWindow", "Settings"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setIconText(_translate("MainWindow", "Exit"))
        self.actionExit.setToolTip(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
