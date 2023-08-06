#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    DBDoc
    ~~~~~

    A simple database doc with one html file.

    :copyright: &copy; 2019 by the faeli.
    :license:  Apache License 2.0
"""
__version__ = '0.0.1'

import os
import datetime
from sqlalchemy import create_engine, inspect

with open(os.path.dirname(os.path.abspath(__file__))+'/style.css', 'r') as f:
    style = f.read()


class DbDoc(object):
    def_top_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset='utf-8'>
    <style>
    {style}
    </style>
    """.format(style=style)

    def_bottom_html = """
    </body></html>
    """

    def __init__(self, *args, **kwargs):
        self.db_uri = kwargs['db_uri']
        self.engine = create_engine(self.db_uri, encoding="utf8")
        self.inspector = inspect(self.engine)
        self.schema_name = self.inspector.default_schema_name
        self.doc_file = "%s.doc.html" % (self.schema_name)
        self.tables = self.get_tables()
        if self.tables and len(self.tables) > 0:
            self.first_table = self.tables[0]
            self.last_table = self.tables[-1]
        self.doc_content = []
        self.date_now = datetime.datetime.now()

    def write_content(self, content):
        self.doc_content.append(content)

    def get_tables(self):
        return self.inspector.get_table_names()

    def get_columns(self, table_name):
        return self.inspector.get_columns(table_name)

    def get_table_name(self, table):
        return table

    def get_table_comment(self, table):
        comment = self.inspector.get_table_comment(self.get_table_name(table))
        if comment and not isinstance(comment, str):
            return comment['text']
        else:
            return comment

    def get_column_name(self, column):
        return column['name']

    def get_column_type(self, column):
        return column['type']

    def get_column_comment(self, column):
        comment = column['comment']
        if comment and not isinstance(comment, str):
            return comment['text']
        else:
            return comment

    def build_top(self):
        top = []
        top.append("<title>%s</title></head><body>" % (self.schema_name))
        top.append("<header><h1 id='%s'>%s</h1><p><label class='date'><small>%s</small></label></p></header>" %
                   (self.schema_name, self.schema_name, self.date_now))
        return "".join(top)

    def build_menus(self):
        menus_html = []
        menus_html.append("<div id='menus' class='menus'><dl>")
        for t in self.tables:
            table_name = self.get_table_name(t)
            menus_html.append("<dt><a href='#%s'>%s</a></dt><dd>%s</dd>" %
                              (table_name, table_name, self.get_table_comment(t)))
        menus_html.append("</dl></div>")
        return "".join(menus_html)

    def build_table(self, table):
        table_name = self.get_table_name(table)
        table_html = []
        table_html.append("<div class='table'><table id='%s'>" % (table_name))
        table_html.append("<caption>%s = %s</caption>" %
                          (table_name, self.get_table_comment(table)))
        table_html.append("<thead>")
        table_html.append("<tr><th colspan='3'>Columns</th></tr>")
        # TODO PK FK Default
        table_html.append(
            "<tr><th class='name'>Name</th><th class='type'>Type</th><th class='comment'>Comment</th></tr>")
        table_html.append("</thead>")
        table_html.append("<tbody>")
        for column in self.get_columns(table_name):
            table_html.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (self.get_column_name(
                column), self.get_column_type(column), self.get_column_comment(column)))
        table_html.append("</tbody>")
        table_html.append("</table></div>")
        return "".join(table_html)

    def build_body(self):
        body = []
        for t in self.tables:
            body.append(self.build_table(t))
        return "".join(body)

    def build_bottom(self):
        bottom = []
        bottom.append("<a href='#%s' class='go_top'></a>" % (self.schema_name))
        bottom.append("<footer>")
        bottom.append(
            "<p>Build by <a href='https://github.com/faeli/dbdoc' target='_black'>DBDoc</a> on %s</p>" % (self.date_now))
        bottom.append("</footer>")
        return "".join(bottom)

    def build(self):
        self.write_content(self.def_top_html)
        self.write_content(self.build_top())
        self.write_content(self.build_menus())
        self.write_content(self.build_body())
        self.write_content(self.build_bottom())
        self.write_content(self.def_bottom_html)

    def save(self):
        self.build()
        with open(self.doc_file, "w", encoding="utf8") as file:
            print("".join(self.doc_content), file=file)
            return self.doc_file
