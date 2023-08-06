# coding=utf-8
import os
import sqlite3
from itertools import chain


class Rules:

    sqlinsert = """
                INSERT INTO rules(keywords, booleanoperator, tags, doctitle, destination) VALUES
                (?, ?, ?, ?, ?);
                """
    sqlreplace = "" "REPLACE INTO rules VALUES " "(?,?, ?, ?, ?, ?);"

    def __init__(self, storagepath):
        #      self.name = name    # instance variable unique to each instance

        if os.path.isfile(os.path.join(storagepath, ".rules.db")):
            self.conn = sqlite3.connect(os.path.join(storagepath, ".rules.db"))
            self.c = self.conn.cursor()
        else:
            self.conn = sqlite3.connect(os.path.join(storagepath, ".rules.db"))
            self.c = self.conn.cursor()
            self.conn.execute(
                "CREATE TABLE rules "
                "(ruleid INTEGER PRIMARY KEY, "
                "keywords, booleanoperator, tags, doctitle, destination);"
            )
            # self.c.execute("CREATE UNIQUE INDEX ruleid ON rules (keywords)")
            self.conn.commit()

    def addrule(self, keywords, boolop, tags, doctitle, dest):
        assert not isinstance(keywords, str)
        assert not isinstance(tags, str)
        self.c.execute(
            self.sqlinsert,
            (", ".join(keywords), boolop, ", ".join(tags), doctitle, dest),
        )
        self.conn.commit()

    def replacerule(self, ruleid, keywords, boolop, tags, doctitle, dest):
        assert not isinstance(keywords, str)
        assert not isinstance(tags, str)
        self.c.execute(
            self.sqlreplace,
            (ruleid, ", ".join(keywords), boolop, ", ".join(tags), doctitle, dest),
        )
        self.conn.commit()

    def delrule(self, keywords, folder):
        assert not isinstance(keywords, str)
        self.c.execute(
            "DELETE FROM rules WHERE keywords = ? AND destination = ?",
            (", ".join(keywords), folder),
        )
        self.conn.commit()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def applyrule(self, text):
        self.c.execute("SELECT ruleid FROM rules")
        ids = self.c.fetchall()
        for idx in ids:
            self.c.execute("SELECT * FROM rules WHERE ruleid = ?", idx)
            rule = self.c.fetchone()
            if rule[2] == "ALL":
                if all(word.lower() in text.lower() for word in rule[1].split(", ")):
                    return {
                        "keywords": rule[1],
                        "boolop": rule[2],
                        "tags": rule[3],
                        "doctitle": rule[4],
                        "destination": rule[5],
                    }
            elif rule[2] == "ANY":
                if all(word in text for word in rule[1].split(", ")):
                    return {
                        "keywords": rule[1],
                        "boolop": rule[2],
                        "tags": rule[3],
                        "doctitle": rule[4],
                        "destination": rule[5],
                    }
        return {"keywords": None, "tags": None, "doctitle": None, "destination": None}

    def printallrules(self):
        self.c.execute("SELECT * FROM rules")
        rows = self.c.fetchall()
        for row in rows:
            print(row)

    def returnallrules(self):
        self.c.execute("SELECT * FROM rules")
        rows = self.c.fetchall()
        return rows

    def returnalltags(self):
        self.c.execute("SELECT tags FROM rules")
        rows = self.c.fetchall()
        tags = list(chain.from_iterable(rows))
        ll = [i.split(", ") for i in tags]
        tags = [item for sublist in ll for item in sublist]
        return tags

    def returnrulesoffolder(self, folder):
        self.c.execute("SELECT * FROM rules WHERE destination = ?", (folder,))
        rows = self.c.fetchall()
        return rows

    def returnruleofkeywords(self, keywords, folder):
        self.c.execute(
            "SELECT * FROM rules WHERE keywords = ? AND destination = ?",
            (", ".join(keywords), folder),
        )
        row = self.c.fetchall()
        return row

    def resetdb(self, storagepath):
        if os.path.isfile(os.path.join(storagepath, ".rules.db")):
            os.remove(os.path.join(storagepath, ".rules.db"))
        self.conn = sqlite3.connect(os.path.join(storagepath, ".rules.db"))
        self.c = self.conn.cursor()
        self.conn.execute(
            "CREATE TABLE rules "
            "(ruleid INTEGER PRIMARY KEY, "
            "keywords, booleanoperator, tags, doctitle, destination);"
        )
        # self.c.execute("CREATE UNIQUE INDEX ruleid ON rules (keywords)")
        self.conn.commit()
