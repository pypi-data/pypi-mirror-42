#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbdoc import DbDoc

def test_mysql():
    doc = DbDoc(db_uri='mysql+pymysql://root:root@127.0.0.1/pkuph_emr?charset=utf8')
    doc.save()