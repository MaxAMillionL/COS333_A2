#-----------------------------------------------------------------------
# regdetails.py
# Author: Maxwell Lloyd and Emily You
#-----------------------------------------------------------------------

import sys
import sqlite3
import contextlib
import argparse
import textwrap

#-----------------------------------------------------------------------

_DATABASE_URL = 'file:reg.sqlite'
_LINE_LENGTH = 72

# format and print each row of output
def print_formatted(title, table):
    for row in table:
        lines = textwrap.wrap(title + " " + " ".join(map(str, row)),
                              _LINE_LENGTH, subsequent_indent="   ")
        for line in lines:
            print(line)

# print relevant course info
def print_course_info(classid):
    try:
        with contextlib.closing(
            sqlite3.connect(_DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True)) as connection:

            with contextlib.closing(connection.cursor()) as cursor:
                print('--------------')
                print('Course Details')
                print('--------------')

                stmt_str = '''
                    SELECT courseid FROM classes
                    WHERE classid = ?
                '''
                cursor.execute(stmt_str, [classid])
                table = cursor.fetchall()
                for row in table:
                    courseid = " ".join(map(str, row))
                print_formatted("Course Id:", table)

                stmt_str = '''
                    SELECT dept, coursenum FROM crosslistings
                    WHERE courseid = ?
                    ORDER BY dept ASC, coursenum ASC
                '''
                cursor.execute(stmt_str, [courseid])
                table = cursor.fetchall()
                if table:
                    print_formatted("Dept and Number:", table)

                stmt_str = '''
                    SELECT area FROM courses
                    WHERE courseid = ?
                '''
                cursor.execute(stmt_str, [courseid])
                table = cursor.fetchall()
                print_formatted("Area:", table)

                stmt_str = '''
                    SELECT title FROM courses
                    WHERE courseid = ?
                '''
                cursor.execute(stmt_str, [courseid])
                table = cursor.fetchall()
                print_formatted("Title:", table)

                stmt_str = '''
                    SELECT descrip FROM courses
                    WHERE courseid = ?
                '''
                cursor.execute(stmt_str, [courseid])
                table = cursor.fetchall()
                print_formatted("Description:", table)

                stmt_str = '''
                    SELECT prereqs FROM courses
                    WHERE courseid = ?
                '''
                cursor.execute(stmt_str, [courseid])
                table = cursor.fetchall()
                print_formatted("Prerequisites:", table)

                stmt_str = '''
                    SELECT profname FROM  profs, coursesprofs
                    WHERE coursesprofs.courseid = ?
                    AND coursesprofs.profid = profs.profid
                    ORDER BY profs.profname ASC
                '''
                cursor.execute(stmt_str, [courseid])
                table = cursor.fetchall()
                print_formatted("Professor:", table)


    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

def print_class_info(classid):
    try:
        with contextlib.closing(
            sqlite3.connect(_DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True)) as connection:

            with contextlib.closing(connection.cursor()) as cursor:

                stmt_str = '''SELECT classid FROM classes
                    WHERE classid = ?
                    '''

                cursor.execute(stmt_str, [classid])
                table = cursor.fetchall()

                if not table:
                    sys.exit(sys.argv[0] + ": "
                             f"no class with classid {classid} exists"
                             )

                print("-------------")
                print("Class Details")
                print("-------------")

                print_formatted("Class Id:", table)


                stmt_str = '''
                    SELECT days FROM classes
                    WHERE classid = ?
                '''
                cursor.execute(stmt_str, [classid])
                table = cursor.fetchall()
                print_formatted("Days:", table)

                stmt_str = '''
                    SELECT starttime FROM classes
                    WHERE classid = ?
                '''
                cursor.execute(stmt_str, [classid])
                table = cursor.fetchall()
                print_formatted("Start time:", table)

                stmt_str = '''
                    SELECT endtime FROM classes
                    WHERE classid = ?
                '''
                cursor.execute(stmt_str, [classid])
                table = cursor.fetchall()
                print_formatted("End time:", table)

                stmt_str = '''
                    SELECT bldg FROM classes
                    WHERE classid = ?
                '''
                cursor.execute(stmt_str, [classid])
                table = cursor.fetchall()
                print_formatted("Building:", table)

                stmt_str = '''
                    SELECT roomnum FROM classes
                    WHERE classid = ?
                '''
                cursor.execute(stmt_str, [classid])
                table = cursor.fetchall()
                print_formatted("Room:", table)

    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)


def main():
    # Implement argument parser
    parser = argparse.ArgumentParser(
        description="Registrar application: show details about a class"
    )
    parser.add_argument(
        "classid", 
        help="the id of the class whose details should be shown",
        type=int
        )

    parser.parse_args()

    classid = sys.argv[1]
    try:
        print_class_info(classid)
        print_course_info(classid)
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)



if __name__ == '__main__':
    main()
