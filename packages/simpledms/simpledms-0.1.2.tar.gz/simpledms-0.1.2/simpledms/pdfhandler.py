"""Package for pdf handling like text extraction, and date parsing."""
import calendar
import locale
import os
import re
import subprocess  # nosec
import tempfile
from typing import List

import cv2  # type: ignore
import dateparser  # type: ignore
from pdfrw import PdfReader
from pdfrw import PdfWriter
from tika import parser  # type: ignore


class PdfHandler:
    """Class for pdf handling."""

    def __init__(self, filepath: str):
        """Initialize all variables.

        Arguments:
            filepath {str} -- Filepath of the pdf, e.g. /home/user/test.pdf

        """
        self.filepath = filepath
        self.thumbheight = 500
        self.tempdirectory = tempfile.TemporaryDirectory()
        self.thumbfpath = None

    def gettext(self) -> str:
        """Extract text from pdf.

        Returns:
            str -- Extracted text.

        """
        raw = parser.from_file(self.filepath)
        return raw["content"]

    def createthumbnail(self):
        """Create a thumbnail of first page of pdf to be shown in GUI.

        Requires pdftoppm installed.

        """
        args = [
            "pdftoppm",
            self.filepath,
            os.path.join(self.tempdirectory.name, "out"),
            "-l",
            "1",
            "-jpeg",
            "-r",
            "300",
        ]
        subprocess.call(args)  # nosec
        im = cv2.imread(os.path.join(self.tempdirectory.name, "out-1.jpg"))
        h, w, _ = im.shape
        h_new = self.thumbheight
        w_new = int(w * h_new / h)
        im = cv2.resize(im, (w_new, h_new))
        cv2.imwrite(os.path.join(self.tempdirectory.name, "out-1.jpg"), im)
        self.thumbfpath = os.path.join(self.tempdirectory.name, "out-1.jpg")

    def update_and_move(
        self, targetdir: str, doctitle: str, tags: List[str], date: str
    ):
        """Update metadata of pdf and move to target directory.

        Arguments:
            targetdir {str} -- Target directory where pdf shall be placed.
            doctitle {str} -- New document title of pdf.
            tags {List[str]} -- Keywords/tags which shall be added to pdf.
            date {str} -- Date which will be entered into pdf filename.

        """
        pdf = PdfReader(self.filepath)
        # Check for correct file ending
        if doctitle[-4:] != ".pdf":
            filename = date + " " + doctitle + ".pdf"
        else:
            filename = date + " " + doctitle
            doctitle = doctitle[0:-4]

        # Check for unique filename
        n = 1
        if os.path.isfile(os.path.join(targetdir, filename)):
            filename = filename[0:-4] + "-" + str(n) + ".pdf"
        while os.path.isfile(os.path.join(targetdir, filename)):
            regex = re.compile(r"-\d{1,}.pdf", re.IGNORECASE)
            filename = regex.sub("-" + str(n) + ".pdf", filename)
            n = n + 1
        pdf.Info.Keywords = tags
        pdf.Info.Title = doctitle

        # Write data
        PdfWriter(os.path.join(targetdir, filename), trailer=pdf).write()

        # try to delete file ##
        try:
            os.remove(self.filepath)
        except OSError as e:  # if failed, report it back to the user ##
            print("Error: %s - %s." % (e.filename, e.strerror))


class DateExtractor:
    """Class to extract date from text."""

    def __init__(self, text: str):
        """Initialize variables.

        Arguments:
            text {str} -- Text from which date shall be extracted.

        """
        self.text = text

    def getdate(self):
        """Search in text for date.

        Returns:
            datetime -- Found date in python datetime format.

        """
        locale.setlocale(locale.LC_ALL, "")
        pattern = []
        prefix = r"Datum:|Date:|übermittelt| übermittelt am | übermittelt am:"

        # Datum: 01.01.2018 and 01-01-2018
        pattern.append(
            r"((?:%s)\s*\d{1,2}[ _.-]\d{1,2}[ _.-](?:19[6789]\d|2[01][0123]\d))"
            % prefix
        )

        # Datum: 02 Jan 2018 02. Jan 2018
        pattern.append(
            r"((?:Datum|Date):\s*\d{1,2}(?:[ _.-]|. )(?:%s) (?:19[6789]\d|2[01][0123]\d))"
            % "|".join(calendar.month_abbr[1:])
        )

        # Datum: 02 Januar 2018 02. Januar 2018
        pattern.append(
            r"((?:Datum|Date):\s*\d{1,2}(?:[ _.-]|. )(?:%s) (?:19[6789]\d|2[01][0123]\d))"
            % "|".join(calendar.month_name)
        )

        # 01.01.2018 and 01-01-2018
        pattern.append(r"(\d{1,2}[ _.-]\d{1,2}[ _.-](?:19[6789]\d|2[01][0123]\d))")

        # 02 Jan 2018 02. Jan 2018
        pattern.append(
            r"(\d{1,2}(?:[ _.-]|. )(?:%s) (?:19[6789]\d|2[01][0123]\d))"
            % "|".join(calendar.month_abbr[1:])
        )

        # 02 Januar 2018 02. Januar 2018
        pattern.append(
            r"(\d{1,2}(?:[ _.-]|. )(?:%s) (?:19[6789]\d|2[01][0123]\d))"
            % "|".join(calendar.month_name)
        )

        for p in pattern:
            dates = re.findall(p, self.text)
            if dates:
                m = re.search(r"\d", dates[0])
                return dateparser.parse(
                    dates[0][m.start() :], settings={"DATE_ORDER": "DMY"}
                )

        pattern = []

        # 2018_02_01
        pattern.append(r"((?:19[6789]\d|2[01][0123]\d)[ _.-]\d{1,2}[ _.-]\d{1,2})")

        for p in pattern:
            dates = re.findall(p, self.text)
            if dates:
                m = re.search(r"\d", dates[0])
                return dateparser.parse(
                    dates[0][m.start() :], settings={"DATE_ORDER": "MDY"}
                )


# if __name__ == "__main__":

#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     file = os.path.join(dir_path, "../tests/Letter_de.pdf")
#     pdfh = PdfHandler(file)
#     text = pdfh.gettext()

#     dateex = DateExtractor(text)
#     print(dateex.getdate())

#     source_text = "dasd übermittelt 02.12.1999 555 01.01.2018 "
#     dateex = DateExtractor(source_text)
#     print(dateex.getdate())

#     source_text = "dasd 2018_02_01_02_03 "
#     dateex = DateExtractor(source_text)
#     print(dateex.getdate())
