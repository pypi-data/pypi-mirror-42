import requests
import getpass
import time
import sys
from collections import defaultdict

import click
from colorama import Fore, Style

from yalesnotes.core.parser import parse_student_marks


URL_DBUFR = r"https://www-dbufr.ufr-info-p6.jussieu.fr/lmd/2004/master/auths/seeStudentMarks.php"


@click.command()
@click.argument("student_number", type=str)
@click.option("-p", "--password", prompt=True, hide_input=True,
              help="The student's password")
@click.option("-c", "--query-cooldown", type=int, default=60,
              help="Number of seconds before retry querying marks")
@click.option('-l', '--student-level',
              type=click.Choice(["L1", "L2", "L3", "M1", "M2"]), default="M2",
              help="The student's current year")
@click.option('--show-all-marks', is_flag=True,
              help='Show the marks for all years instead of only current year')
def yalesnotes(student_number, password, query_cooldown, student_level,
               show_all_marks):
    content = _query_student_marks(student_number, password)
    marks, lectures_name = parse_student_marks(content)

    # Filter marks by student's year
    if not show_all_marks:
        _filter_marks(marks, student_level)

    # Show the marks for the first time
    for code_lecture, marks_by_exam in marks.items():
        print(code_lecture, lectures_name[code_lecture], ":")
        for exam, mark in marks_by_exam.items():
            print(" ", exam, ":", mark)
    print("")

    # Wait for other marks to arrive
    while True:
        sys.stdout.write('\r')
        sys.stdout.write("Last query done at : " + time.ctime())
        sys.stdout.flush()

        time.sleep(query_cooldown)

        # Query marks
        content = _query_student_marks(student_number, password)
        new_marks, lectures_name = parse_student_marks(content)
        if not show_all_marks:
            _filter_marks(new_marks, student_level)
        # Test 1
        # new_marks = {
        #     '5I852-2018oct': {
        #         '[examen-reparti-1] Examen du 23-11-2018': '10.5/20',
        #         'NOUVEL EXAMEN': '10.5/20'
        #     }
        # }

        # Test 2
        # new_marks = {
        #     'NOUVELLE UE': {
        #         '[examen-reparti-1] Examen du 23-11-2018': '10.5/20'
        #     }
        # }

        # Check for new marks & print them
        new_marks = _get_marks_differences(marks, new_marks)

        for code_lecture, marks_by_exam in new_marks.items():
            print(f"\n\n{Fore.RED}" + code_lecture,
                  lectures_name[code_lecture], ":")
            for exam, mark in marks_by_exam.items():
                print(" ", exam, ":", mark)
                marks[code_lecture][exam] = mark
            print(f"{Style.RESET_ALL}\n\a")


@click.command()
@click.argument("student_number", type=str)
@click.option("-p", "--password", prompt=True, hide_input=True,
              help="The student's password")
def yalesmoyennes(student_number, password):
    content = _query_student_marks(student_number, password)
    marks = parse_student_marks(content)
    print(marks)


def _query_student_marks(student_number, password, url=URL_DBUFR):
    web_page = requests.get(url, auth=(student_number, password))

    while web_page.status_code == 401:
        password = getpass.getpass("Wrong password for student " +
                                   student_number + ", try again :\n>")
        web_page = requests.get(url, auth=(student_number, password))

    if web_page.status_code != 200:
        print("Error with the website. Error code :", web_page.status_code)
        exit(1)

    return web_page.text


def _get_student_year(student_level):
    if student_level == "L1":
        return "1"
    elif student_level == "L2":
        return "2"
    elif student_level == "L3":
        return "3"
    elif student_level == "M1":
        return "4"
    elif student_level == "M2":
        return "5"


def _filter_marks(marks, student_level):
    student_year = _get_student_year(student_level)
    for code_lecture in list(marks.keys()):
        if code_lecture[0] != student_year:
            del marks[code_lecture]


def _get_marks_differences(marks, new_marks):
    difference = defaultdict(dict)

    # Check for new code lecture
    for code_lecture in new_marks.keys():
        if code_lecture not in new_marks.keys():
            difference[code_lecture] = new_marks[code_lecture]

    # Check for new exam in an existing code lecture
    for code_lecture, marks_by_exam in new_marks.items():
        for exam, mark in marks_by_exam.items():
            if exam not in marks[code_lecture].keys():
                difference[code_lecture][exam] = mark
    return difference


if __name__ == '__main__':
    yalesnotes()
