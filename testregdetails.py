#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregdetails.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import os
import sys
import sqlite3
import contextlib

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH
_DATABASE_URL = 'file:reg.sqlite'

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def get_classids():
    classids = []
    try:
        with contextlib.closing(
            sqlite3.connect(_DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True)) as connection:

            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = '''
                    SELECT classid FROM classes
                '''
                cursor.execute(stmt_str)
                classids = cursor.fetchall()
                
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)
    
    return classids

#-----------------------------------------------------------------------

def exec_command(program, args):

    print_flush(UNDERLINE)
    command = 'python ' + program + ' ' + args
    print_flush(command)
    exit_status = os.system(command)
    if os.name == 'nt':  # Running on MS Windows?
        print_flush('Exit status = ' + str(exit_status))
    else:
        print_flush('Exit status = ' + str(os.WEXITSTATUS(exit_status)))

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' regdetailsprogram',
            file=sys.stderr)
        sys.exit(1)

    program = sys.argv[1]

    classids = get_classids()

    modulus = 50
    counter = 0

    # Stress test
    for classid in classids:
        
        if counter % modulus == 0:
            exec_command(program, str(classid[0]))

        counter += 1

    # Error edge cases
    exec_command(program, '0')

    exec_command(program, '1 1 1 1 1 1')

    exec_command(program, '-h')

    exec_command(program, '--help')

    exec_command(program, '-help')

    exec_command(program, '1 1 1 -h')

    exec_command(program, '-h 1 1 1')

    exec_command(program, "")

    exec_command(program, '8321 9032')

    exec_command(program, 'abc123')

if __name__ == '__main__':
    main()
