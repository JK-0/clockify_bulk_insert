import time
import csv
from optparse import OptionParser
from helium import *


def get_argument():

    parser = OptionParser()

    parser.add_option("-u", "--username", dest="username",
                    help="enter google username", )

    parser.add_option("-p", "--password", dest="password",
                    help="enter google password", )
    
    parser.add_option("-f", "--file",
                      dest="clockifi_data",
                      help="path to clockifi.csv data file ")

    (options, arguments) = parser.parse_args()

    return options

def magic(u, p, f):

    # if password contain specialcharacter
    # p =''
    
    # open clockifi 
    start_chrome("https://clockify.me/")
    time.sleep(5)

    # login with google
    click("Log In")
    click("Continue with Google")
    write(u)
    press(ENTER)
    time.sleep(5)
    write(p)
    press(ENTER)
    time.sleep(5)


    with open(f, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:

            # enter discription
            write(row['Discription'], into="What have you worked on?")            
            time.sleep(1)
            
            # select project
            # click("Project")
            press(TAB)
            write(row['Project'])
            time.sleep(1)
            press(DOWN)
            press(ENTER)
            time.sleep(1)

            # select tag
            press(TAB)
            x = row['Tag'].split(', ')
            for t in range(len(x)):
                click(x[t])
                time.sleep(1)

            # add start time
            press(TAB)
            press(TAB)
            write(row['Start_time'])
            time.sleep(1)

            # add end time
            press(TAB)
            write(row['End_time'])
            time.sleep(1)

            # add date
            press(TAB)
            press(TAB)
            write(row['Date'])
            time.sleep(1)

            # add data 
            click("ADD")
            time.sleep(2)


options = get_argument()
magic(options.username, options.password, options.clockifi_data)

