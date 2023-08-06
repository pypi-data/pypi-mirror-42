#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from dbdoc import DbDoc


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        doc = DbDoc(db_uri=args[0])
        f = doc.save()
        print(f)
    else:
        print("")
        print("dbdoc is A simple database doc with one html file")
        print("build with love by faeli and friends in python.")
        print("")
        print("Usage:")
        print("  dbdoc dialect+driver://username:password@host:port/database")
        print("")
        print("Example:")
        print("  dbdoc mysql+pymysql://root:root@127.0.0.1:3306/testing")
        print("  dbdoc postgresql+psycopg2://root:root@127.0.0.1:5443/testing")
        print("  dbdoc mssql+pymssql://scott:tiger@hostname:port/dbname")
        print("  dbdoc sqlite:////absolute/path/to/foo.db")
        print("")
        print("")


if __name__ == '__main__':
    main()
