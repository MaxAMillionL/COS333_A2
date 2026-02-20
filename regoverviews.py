#!/usr/bin/env python

#-----------------------------------------------------------------------
# regoverviews.py
# Author: Emily You & Maxwell Lloyd
#-----------------------------------------------------------------------

import sys
import contextlib
import sqlite3
import argparse
import textwrap

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite'
MAX_LINE_LENGTH = 72

# format and print each row of output
def print_formatted(table):
    for row in table:
        prefix = '%5s %4s %6s %4s ' % (row[0], row[1],row[2], row[3])
        wrap = textwrap.fill(row[4], width=MAX_LINE_LENGTH,
                    initial_indent=prefix, subsequent_indent=' ' * 23)
        print(wrap)

def main():
    # create parser for command-line options and arguments
    parser = argparse.ArgumentParser(description="Registrar " \
    "application: show overviews of classes")
    parser.add_argument("-d", help="show only those classes " \
    "whose department contains dept", dest="dept", metavar='dept')
    parser.add_argument("-n", help="show only those classes " \
    "whose course number contains num", dest="num", metavar='num')
    parser.add_argument("-a", help="show only those classes " \
    "whose distrib area contains area", dest="area", metavar='area')
    parser.add_argument("-t", help="show only those classes " \
    "whose course title contains title", dest="title", metavar='title')
    args = parser.parse_args()

    try:
        with contextlib.closing(
            sqlite3.connect(DATABASE_URL + '?mode=ro',
            isolation_level=None,uri=True)) as connection:

            with contextlib.closing(connection.cursor()) as cursor:
                print("ClsId Dept CrsNum Area Title")
                print("----- ---- ------ ---- -----")

                # array that stores command-line arguments
                fields = []
                stmt_str = ''' SELECT classid, dept, coursenum, area,
                    title 
                    FROM classes, crosslistings, courses 
                    WHERE courses.courseid=classes.courseid AND
                    courses.courseid=crosslistings.courseid
                    '''
                if args.dept:
                    stmt_str += " AND dept LIKE ?"
                    fields.append(f"%{args.dept}%")
                if args.num:
                    stmt_str += " AND coursenum LIKE ?"
                    fields.append(f"%{args.num}%")
                if args.area:
                    stmt_str += " AND area LIKE ?"
                    fields.append(f"%{args.area}%")
                if args.title:
                    # replace for insensitivity
                    if '%' in args.title or '_' in args.title:
                        title = args.title.replace('%', '\\%') \
                            .replace('_', '\\_')
                    else:
                        title = args.title
                    stmt_str += " AND title LIKE ? ESCAPE '\\'"
                    fields.append(f"%{title}%")

                # order based on priority
                stmt_str += ''' ORDER BY dept ASC, coursenum ASC,
                classid ASC '''
                cursor.execute(stmt_str, fields)

                table = cursor.fetchall()
                print_formatted(table)

    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
