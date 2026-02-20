#-----------------------------------------------------------------------
# testregoverviews.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import os
import sys

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

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
        print('usage: ' + sys.argv[0] + ' regprogram', file=sys.stderr)
        sys.exit(1)

    program = sys.argv[1]

    exec_command(program, '-d COS')
    exec_command(program, '-d COS -a qr -n 2 -t intro')

    # Add more tests here.
    exec_command(program, '')
    exec_command(program, '-d -a -n -t')
    exec_command(program, '-d RANDOM')
    exec_command(program, '-a RANDOM')
    exec_command(program, '-n RANDOM')
    exec_command(program, '-t RANDOM')
    
    exec_command(program)
    exec_command(program, '-n 333')
    exec_command(program, '-n b')
    exec_command(program, '-a Qr')
    exec_command(program, '-t intro')
    exec_command(program, '-t science')
    exec_command(program, '-t C_S')
    exec_command(program, ('-t c%S'))
    exec_command(program, '-t "Independent Study"')
    exec_command(program, '-t "Independent Study "')
    exec_command(program, '-t "Independent Study "')
    exec_command(program, '-t " Independent Study"')
    exec_command(program, '-t "  Independent Study"')
    exec_command(program, '-t=-c')
    exec_command(program, '-n 333')
    exec_command(program, '-d ant -a em')
    exec_command(program, ('-d dan -a la -n 2'))
    exec_command(program, '-n 2')
    exec_command(program, '-d mat -n 3 -a qr')
    exec_command(program, '-d vis -n 4 -t advanced')
    exec_command(program, '-d vis -n ""')
    exec_command(program, '-d "" -a "" -t writing')
    
    # Error handling
    exec_command(program, ('-a qr'))
    exec_command(program, ('-A qr'))
    exec_command(program, (' "-a " qr'))
    exec_command(program, ('-a'))
    exec_command(program, ('-a qr -d'))
    exec_command(program, ('-a -d cos'))
    exec_command(program, ('-x'))
    exec_command(program, ('-t -a'))



#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()