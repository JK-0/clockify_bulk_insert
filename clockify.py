#!/usr/bin/env python

import csv
import os
import re
import time

import six
from PyInquirer import (
    Token,
    ValidationError,
    Validator,
    print_json,
    prompt,
    style_from_dict
)
from helium import *
from selenium.common.exceptions import SessionNotCreatedException
from pyfiglet import figlet_format

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})


def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)


class EmailValidator(Validator):
    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"

    def validate(self, email):
        if len(email.text):
            if re.match(self.pattern, email.text):
                return True
            else:
                raise ValidationError(
                    message="Invalid email",
                    cursor_position=len(email.text)
                )
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(email.text)
            )

class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text)
            )


class FilePathValidator(Validator):
    def validate(self, value):
        if len(value.text):
            if os.path.isfile(value.text):
                return True
            else:
                raise ValidationError(
                    message="File not found",
                    cursor_position=len(value.text)
                )
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text)
            )


def login(basicinfo):
    log("Opening a browser...", "yellow")
    login_url = "https://clockify.me/login"
    browser = basicinfo.get('browser')
    login_method = basicinfo.get('login_method')
    if login_method == 'google':
        email = basicinfo.get('google_email')
        password = basicinfo.get('google_password')
    else:
        email = basicinfo.get('regular_email')
        password = basicinfo.get('regular_password')

    # Open Clockify Login Page
    if (browser == 'firefox'):
        try:
            start_firefox(login_url)
        except SessionNotCreatedException:
            log("Firefox browser not found. Try again.", "red")
            exit()
    else:
        try:
            start_chrome(login_url)
        except SessionNotCreatedException:
            log("Chrome browser not found. Try again.", "red")
            exit()
    time.sleep(5) # Wait

    log("Opened, Now logging you in...", "yellow")
    if (login_method == 'google'): # Google Login
        highlight("Continue with Google")
        click("Continue with Google")
        write(email, into="Email or phone")
        click('Next')
        time.sleep(5) # Wait
        write(password, into="Enter your password")
        click('Next')
        time.sleep(5) # Wait
    else: # Regular Login
        write(email, into="Enter email")
        write(password, into="Enter password")
        press(ENTER)
        time.sleep(5) # Wait

    log("Logged in", "yellow")
    return True


def bulkInsert(basicinfo):
    log("Loading csv file...", "yellow")
    csv_file = basicinfo.get('data')

    # Process CSV File
    log("Reading....", "yellow")
    reader = csv.DictReader(csv_file)

    log("Start Processing....", "green")
    totalrows = 0
    for row in reader:
        # Enter Task Description
        log(row['Description'], "magenta")
        write(row['Description'], into="What have you worked on?")
        time.sleep(1) # Wait

        # Select Project
        log(row['Project'], "magenta")
        press(TAB)
        write(row['Project'])
        time.sleep(1) # Wait
        press(DOWN)
        press(ENTER)
        time.sleep(1) # Wait

        # Select Tag
        log(row['Tag'], "magenta")
        press(TAB)
        tags = row['Tag'].split(',')
        for tag in tags:
            click(tag)
            time.sleep(1) # Wait

        # Fill Start Time
        log(row['Start_time'], "magenta")
        press(TAB)
        press(TAB)
        write(row['Start_time'])
        time.sleep(1) # Wait

        # Fill End Time
        log(row['End_time'], "magenta")
        press(TAB)
        write(row['End_time'])
        time.sleep(1) # Wait

        # Fill Date
        log(row['Date'], "magenta")
        press(TAB)
        press(TAB)
        write(row['Date'])
        time.sleep(1) # Wait

        # Add'em
        log('Inserting....', "magenta")
        click("ADD")
        time.sleep(5) # Wait
        log('Inserted', "green")

        totalrows += 1

    return totalrows


def getLoginMethod(answer, login_method):
    return answer.get("login_method").lower() == login_method.lower()


def askBasicInformation():
    questions = [
        {
            'type': 'list',
            'name': 'browser',
            'message': 'Your Preferred Browser:',
            'choices': ['Chrome', 'Firefox'],
            'filter': lambda val: val.lower()
        },
        {
            'type': 'list',
            'name': 'login_method',
            'message': 'Choose Login Method:',
            'choices': ['Regular', 'Google'],
            'filter': lambda val: val.lower()
        },
        {
            'type': 'input',
            'name': 'google_email',
            'message': 'Enter Google Email:',
            'when': lambda answers: getLoginMethod(answers, "google"),
            'validate': EmailValidator
        },
        {
            'type': 'password',
            'name': 'google_password',
            'message': 'Enter Google Password:',
            'when': lambda answers: getLoginMethod(answers, "google"),
            'validate': EmptyValidator
        },
        {
            'type': 'input',
            'name': 'regular_email',
            'message': 'Enter Regular Email:',
            'when': lambda answers: getLoginMethod(answers, "regular"),
            'validate': EmailValidator
        },
        {
            'type': 'password',
            'name': 'regular_password',
            'message': 'Enter Regular Password:',
            'when': lambda answers: getLoginMethod(answers, "regular"),
            'validate': EmptyValidator
        },
        {
            'type': 'input',
            'name': 'data',
            'message': 'Enter CSV File Path: (Caution : Please double check your data)',
            'validate': FilePathValidator,
            'filter': lambda val: open(val, newline=''),
        },
        {
            'type': 'confirm',
            'name': 'ready',
            'message': 'Lets Begin with Loggin in.. Keep checking this terminal..'
        }
    ]

    answers = prompt(questions, style=style)
    return answers


def takeConfirmation():
    questions = [
        {
            'type': 'confirm',
            'name': 'is_loggedin',
            'message': 'Are you able to login in to system ? If not, please try to login manually, and let me know when you\'re done.'
        },
        {
            'type': 'confirm',
            'name': 'is_maximize',
            'message': 'Is your browser is Maximized ?',
            'when': lambda answers: answers.get("is_loggedin", False)
        },
        {
            'type': 'confirm',
            'name': 'ready',
            'message': 'Have you double checked your data ? Ready to insert data ?',
            'when': lambda answers: answers.get("is_maximize", False)
        }
    ]

    answers = prompt(questions, style=style)
    return answers


def cli():
    """
    Simple CLI for automate bulk insertion of clockify enteries.
    """
    log("CLOCKIFY", color="blue", figlet=True)
    log("Welcome to Clockify Bulk Insert", "blue")

    basicinfo = askBasicInformation()
    if basicinfo.get("ready", False):
        try:
            loggedin = login(basicinfo)
        except Exception as e:
            raise Exception("An error occured: %s" % (e))

        if loggedin:
            c = takeConfirmation()
            l = c.get("is_loggedin", False)
            m = c.get("is_maximize", False)
            r = c.get("ready", False)
            if l and m and r:
                log("Looks like you're ready to go!!", "green")
                try:
                    response = bulkInsert(basicinfo)
                    if response > 0:
                        log("Insertion Successful", "blue")
                        log("Total {} Entries Inserted".format(response), "green")
                    else:
                        log("An error while trying to insert.", "red")
                except Exception as e:
                    log("Something went wrong, Please try again.", "red")
                    raise Exception("An error occured: %s" % (e))
            else:
                log("Phew!! You need to re-run the process again.", "green")
    log("Never mind!! Better luck next time.", "green")

if __name__ == '__main__':
    cli()
