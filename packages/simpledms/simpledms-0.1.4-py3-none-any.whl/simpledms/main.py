"""This is the main module which serves as a starting point. It starts the UI."""
import datetime
import json
import os
import re
import sys
import webbrowser

import magic  # type: ignore
import qdarkstyle  # type: ignore
import rules  # type: ignore
import ui.about  # type: ignore
import ui.resources  # type: ignore
from pdfhandler import DateExtractor
from pdfhandler import PdfHandler
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFileSystemModel
from utils import MyDictionaryCompleter
from utils import MyRulesWidget
from utils import MyTextEdit

CURRDIR = os.path.dirname(os.path.abspath(__file__))


class Ui(QtWidgets.QMainWindow):
    """Main Class of the simple DMS user interface.

    Arguments:
        nothing

    Returns:
        nothing

    """

    def __init__(self):
        """Initialize variables and connect actions with functions."""
        super(Ui, self).__init__()
        uic.loadUi(os.path.join(CURRDIR, "ui", "main_simpledms.ui"), self)
        self.loadpref()
        self.rules = rules.Rules(self.pref["dmsroot"])
        self.currentselectedrulesfolder = None
        self.currentselectedsearchfolder = None
        self.filemodelmonitor = QFileSystemModel()
        self.rulesfoldermodel = QFileSystemModel()
        self.resultfoldermodel = QFileSystemModel()
        self.searchfoldermodel = QFileSystemModel()
        self.textEdit_tags = MyTextEdit(self.textEdit_tags)
        self.updateui_settings()
        self.updateui_pdfrename()
        self.show()

        # Connect Widget Toolbar Actions
        self.actionScan.triggered.connect(self.select_widget)
        self.actionPdf.triggered.connect(self.select_widget)
        self.actionSettings.triggered.connect(self.select_widget)
        self.actionAbout.triggered.connect(self.show_ui_about)
        self.actionExit.triggered.connect(self.select_widget)

        # Connect Preferences
        self.pushButton_setmonitorfolder.clicked.connect(self.browse_monitor_folder)
        self.pushButton_setdmsroot.clicked.connect(self.browse_dms_root)
        self.treeView_rulesfolders.clicked.connect(self.rulesfolderselected)
        self.treeView_rules.doubleClicked.connect(self.ruledoubleclicked)
        self.pushButton_addrule.clicked.connect(self.addruleclicked)
        self.pushButton_deleterule.clicked.connect(self.deleteruleclicked)

        # Connect page pdf renaming
        self.listView_monitorfiles.clicked.connect(self.listView_monitorfiles_clicked)

        self.treeView_output.clicked.connect(self.treeView_output_clicked)
        self.pushButton_ok.clicked.connect(self.pushButton_ok_clicked)
        self.listView_monitorfiles.doubleClicked.connect(
            self.listView_monitorfiles_doubleclicked
        )
        self.lineEdit_outputfilename.textChanged.connect(self.readyforstorage)
        self.pushButton_addDate.clicked.connect(self.pushButton_addDate_clicked)

    # -------- Settings page -----------
    def rulesfolderselected(self, signal):
        """Update ui if a folder in settings -> rules is selected."""
        self.currentselectedrulesfolder = self.rulesfoldermodel.filePath(signal)
        self.updateui_settings()
        self.pushButton_addrule.setEnabled(True)

    def ruledoubleclicked(self):
        """Open ui for rule adaption of double clicked rule."""
        selectedrule = self.treeView_rules_model.itemData(
            self.treeView_rules.selectedIndexes()[0]
        )
        rule = self.rules.returnruleofkeywords(
            [selectedrule[0]], self.currentselectedrulesfolder
        )
        rulesdialog = MyRulesWidget(
            keywords=rule[0][1],
            booleanoperator=rule[0][2],
            tags=rule[0][3],
            doctitle=rule[0][4],
            indexertags=set(self.rules.returnalltags()),
        )
        rulesdialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if rulesdialog.exec_():
            self.rules.replacerule(
                rule[0][0],
                rulesdialog.keywords,
                rulesdialog.booleanoperator,
                rulesdialog.tags,
                rulesdialog.doctitle,
                self.currentselectedrulesfolder,
            )
            self.updateui_settings()

    def deleteruleclicked(self):
        """Delete selected rule and update ui."""
        if self.treeView_rules.selectedIndexes():
            selectedrule = self.treeView_rules_model.itemData(
                self.treeView_rules.selectedIndexes()[0]
            )
            self.rules.delrule([selectedrule[0]], self.currentselectedrulesfolder)
            self.updateui_settings()

    def addruleclicked(self):
        """Add rule to database if it does not exist yet."""
        rulesdialog = MyRulesWidget(indexertags=set(self.rules.returnalltags()))
        rulesdialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if rulesdialog.exec_():
            if self.rules.returnruleofkeywords(
                rulesdialog.keywords, self.currentselectedrulesfolder
            ):
                QtWidgets.QMessageBox.information(
                    self, "Error", "A rule with these keywords already exists."
                )
            else:
                self.rules.addrule(
                    rulesdialog.keywords,
                    rulesdialog.booleanoperator,
                    rulesdialog.tags,
                    rulesdialog.doctitle,
                    self.currentselectedrulesfolder,
                )
                self.updateui_settings()

    def loadpref(self):
        """Load preferences: root of dms and monitorfolder."""
        if os.path.isfile("pref.json"):
            with open("pref.json") as f:
                self.pref = json.load(f)
                if not os.path.isdir(self.pref["dmsroot"]):
                    os.makedirs(self.pref["dmsroot"])
                    QtWidgets.QMessageBox.information(
                        self, "Attention!", "Stored path of dmsroot does not exist"
                    )
                if not os.path.isdir(self.pref["monitorfolder"]):
                    os.makedirs(self.pref["monitorfolder"])
                    QtWidgets.QMessageBox.information(
                        self,
                        "Attention!",
                        "Stored path of monitorfolder does not exist.",
                    )
        else:
            # If pref.json file does not exist
            if not os.path.isdir(os.path.join(os.path.expanduser("~"), "paperwork")):
                os.makedirs(os.path.join(os.path.expanduser("~"), "paperwork"))
                QtWidgets.QMessageBox.information(
                    self,
                    "Attention!",
                    "Standard path for file cabinet"
                    "was created. If "
                    "needed, please change.",
                )

            if not os.path.isdir(
                os.path.join(os.path.expanduser("~"), "paperwork_open")
            ):
                os.makedirs(os.path.join(os.path.expanduser("~"), "paperwork_open"))
                QtWidgets.QMessageBox.information(
                    self,
                    "Attention!",
                    "Standard path for monitor folder"
                    "was created. If "
                    "needed, please change.",
                )

            self.pref = {
                "dmsroot": os.path.join(os.path.expanduser("~"), "paperwork"),
                "monitorfolder": os.path.join(
                    os.path.expanduser("~"), "paperwork_open"
                ),
            }
            self.savepref()

    def savepref(self):
        """Save preferences to pref.json."""
        with open("pref.json", "w") as f:
            json.dump(self.pref, f)

    def browse_monitor_folder(self):
        """Select monitor folder."""
        # execute getExistingDirectory dialog and set the directory variable to be equal
        # to the user selected directory
        directory = QFileDialog.getExistingDirectory(
            self, "Select a monitor folder with files to be " "processed/imported"
        )
        # if user didn't pick a directory don't continue
        if directory:
            self.pref["monitorfolder"] = directory
            self.savepref()
            self.updateui_settings()
            self.updateui_pdfrename()

    def browse_dms_root(self):
        """Select dms root folder."""
        # execute getExistingDirectory dialog and set the directory variable to be equal
        # to the user selected directory
        directory = QFileDialog.getExistingDirectory(
            self, "Select a root directory of the filing cabinet"
        )
        # if user didn't pick a directory don't continue
        if directory:
            if not len(self.rules.returnallrules()) == 0:
                result = QtWidgets.QMessageBox.question(
                    self,
                    "Attention",
                    "If the root directory is changed, the current rules are "
                    "deleted! Are you sure and want to proceed?",
                )
                if result == QtWidgets.QMessageBox.No:
                    return
            self.rules.resetdb(directory)
            self.pref["dmsroot"] = directory
            self.savepref()
            # self.indexer.__init__(directory)
            self.updateui_settings()

    def updateui_settings(self):
        """Update ui elements of settings page."""
        self.label_monitorfolder.setText(self.pref["monitorfolder"])
        self.label_monitordir.setText(
            ".."
            + os.sep
            + os.path.basename(os.path.normpath(self.pref["monitorfolder"]))
        )
        self.label_dmsroot.setText(self.pref["dmsroot"])
        self.rulesfoldermodel.setRootPath(self.pref["dmsroot"])
        self.rulesfoldermodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Dirs)
        self.treeView_rulesfolders.setModel(self.rulesfoldermodel)
        self.treeView_rulesfolders.setRootIndex(
            self.rulesfoldermodel.index(self.pref["dmsroot"])
        )
        self.treeView_rulesfolders.hideColumn(1)
        self.treeView_rulesfolders.hideColumn(2)
        self.treeView_rulesfolders.hideColumn(3)
        self.treeView_rules_model = QtGui.QStandardItemModel()
        self.treeView_rules.setModel(self.treeView_rules_model)
        self.treeView_rules_model.setHorizontalHeaderLabels(["Rules (keywords)"])
        rulesoffolder = self.rules.returnrulesoffolder(self.currentselectedrulesfolder)
        if rulesoffolder is not None:
            for i in rulesoffolder:
                rule = QtGui.QStandardItem(i[1])
                self.treeView_rules_model.appendRow(rule)

    # -------- Action Bar -----------
    def select_widget(self):
        """Select index of stacked widget based on toolbox actions."""
        sender = self.sender()
        if sender.text() == "Scan":
            pass
        elif sender.text() == "Import":
            self.stackedWidget.setCurrentIndex(0)
        elif sender.text() == "Settings":
            self.stackedWidget.setCurrentIndex(1)
        elif sender.text() == "Exit":
            QtWidgets.QApplication.instance().quit()

    def show_ui_about(self):
        """Show about page."""
        dialog = QDialog()
        dialog.ui = ui.about.Ui_Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

    # -------- pdf renaming page -----------
    def listView_monitorfiles_clicked(self, index):
        """Show preview of pdf, extract date and words and propose tags and directory in dms root."""
        pdffile = os.path.join(
            self.pref["monitorfolder"], self.filemodelmonitor.itemData(index)[0]
        )

        # Check if file is really a pdf.
        if "PDF" not in magic.from_file(pdffile):
            QtWidgets.QMessageBox.information(
                self, "Attention!", "Document is not a pdf."
            )
            return

        self.listView_monitorfiles.setEnabled(False)
        self.setCursor(QtCore.Qt.BusyCursor)
        self.statusbar.showMessage("Reading pdf...")

        self.pdfhandler = PdfHandler(pdffile)
        self.pdfhandler.thumbheight = (
            self.listView_monitorfiles.frameGeometry().height()
        )
        self.pdfhandler.createthumbnail()

        pixmap = QtGui.QPixmap(self.pdfhandler.thumbfpath)
        self.thumbnail.setPixmap(pixmap)
        self.thumbnail.resize(pixmap.width(), pixmap.height())
        self.analyze_text()
        self.listView_monitorfiles.setEnabled(True)
        self.setCursor(QtCore.Qt.ArrowCursor)

    def listView_monitorfiles_doubleclicked(self, index):
        """Open doubleclicked file.

        Arguments:
            index: index from pyqt5 listview which element was clicked.

        Returns:
            nothing

        """
        file2open = os.path.join(
            self.pref["monitorfolder"], self.filemodelmonitor.itemData(index)[0]
        )
        webbrowser.open(file2open)

    def listWidget_pdfthumbnails_doubleclicked(self):
        """Open file in browser."""
        file2open = self.pdfhandler.filepath
        if os.path.isfile(file2open):
            webbrowser.open(file2open)
        else:
            QtWidgets.QMessageBox.information(
                self, "Attention!", "File does not exist!"
            )

    def analyze_text(self):
        """Analyze the found text."""
        text = self.pdfhandler.gettext()
        dateext = DateExtractor(text)
        date = dateext.getdate()
        # If Date not found in text, search for date in filename
        if not date:
            dateext = DateExtractor(self.pdfhandler.filepath)
            date = dateext.getdate()
        result = self.rules.applyrule(text)

        if result["doctitle"] is not None:
            if date is not None:
                self.lineEdit_outputfilename.setText(
                    date.strftime("%Y-%m-%d") + " " + result["doctitle"]
                )
            else:
                self.lineEdit_outputfilename.setText(result["doctitle"])
        else:
            if date is not None:
                self.lineEdit_outputfilename.setText(date.strftime("%Y-%m-%d") + " ")
            else:
                self.lineEdit_outputfilename.clear()

        if result["tags"] is not None:
            self.textEdit_tags.setText(result["tags"])
        else:
            self.textEdit_tags.clear()

        self.destination = result["destination"]

        self.treeView_output.setCurrentIndex(
            self.resultfoldermodel.index(self.destination)
        )

        if not self.readyforstorage():
            self.lineEdit_outputfilename.setFocus()
        else:
            self.pushButton_ok.setFocus()

        self.statusbar.showMessage("Ready")
        self.setCursor(QtCore.Qt.ArrowCursor)

    def readyforstorage(self):
        """Check if file infos like date, text, tags and folder are set."""
        if (
            self.lineEdit_outputfilename.text()
            and re.match(
                r"(\d{4}-\d{2}-\d{2}\s\S+)",
                self.lineEdit_outputfilename.text(),
                re.I | re.UNICODE,
            )
            and self.resultfoldermodel.filePath(self.treeView_output.currentIndex())
        ):
            self.pushButton_ok.setEnabled(True)
            return True
        else:
            self.pushButton_ok.setEnabled(False)
            return False

    def pushButton_ok_clicked(self):
        """Store document with new metadata in target directory."""
        self.setCursor(QtCore.Qt.BusyCursor)
        self.statusbar.showMessage("Storing...")
        doctitle = self.lineEdit_outputfilename.text()[11:]
        date = self.lineEdit_outputfilename.text()[0:10]
        tags = self.textEdit_tags.toPlainText()
        tags = tags.strip(", ")
        path = self.resultfoldermodel.filePath(self.treeView_output.currentIndex())
        self.pdfhandler.update_and_move(path, doctitle, tags, date)
        self.updateui_pdfrename()
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.statusbar.showMessage("ready")

    def pushButton_addDate_clicked(self):
        """Add current date to document name field."""
        if self.lineEdit_outputfilename.text():
            if re.match(r"(\d{4}-\d{2}-\d{2})", self.lineEdit_outputfilename.text()):
                text = (
                    str(datetime.date.today())
                    + self.lineEdit_outputfilename.text()[10:]
                )
                self.lineEdit_outputfilename.setText(text)
            else:
                self.lineEdit_outputfilename.setText(str(datetime.date.today()) + " ")
        else:
            self.lineEdit_outputfilename.setText(str(datetime.date.today()) + " ")
        self.lineEdit_outputfilename.setFocus()

    def treeView_output_clicked(self):
        """Check if all input is available after the target directory was selected."""
        self.readyforstorage()

    def updateui_pdfrename(self):
        """Update ui of page pdfrename."""
        self.filemodelmonitor.setRootPath(self.pref["monitorfolder"])
        self.filemodelmonitor.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files)
        self.filemodelmonitor.setNameFilters(["*.pdf"])
        self.filemodelmonitor.setNameFilterDisables(False)
        self.listView_monitorfiles.setModel(self.filemodelmonitor)
        self.listView_monitorfiles.setRootIndex(
            self.filemodelmonitor.index(self.pref["monitorfolder"])
        )
        self.resultfoldermodel.setRootPath(self.pref["dmsroot"])
        self.resultfoldermodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Dirs)
        self.treeView_output.setModel(self.resultfoldermodel)
        self.treeView_output.setRootIndex(
            self.resultfoldermodel.index(self.pref["dmsroot"])
        )
        self.treeView_output.hideColumn(1)
        self.treeView_output.hideColumn(2)
        self.treeView_output.hideColumn(3)
        # todo: change name of header
        indexertags = set(self.rules.returnalltags())
        completer = MyDictionaryCompleter(myKeywords=indexertags)
        self.textEdit_tags.setCompleter(completer)


def start_gui():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = Ui()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_gui()
