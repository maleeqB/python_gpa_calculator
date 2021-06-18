from collections import defaultdict
import textwrap
import sys


class CourseMode:
    def __init__(self, name, grade_points):
        self._name = name
        self._grade_points = grade_points

    def get_name(self):
        return self._name

    def get_grade_points(self):
        return self._grade_points

    def get_grade_letters(self):
        return list(self._grade_points.keys())


COURSE_MODES = [CourseMode("NG 5.0", {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}),
                CourseMode("NG 4.0", {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}),
                CourseMode("US Grade", {'A+': 4.000, 'A': 4.000, 'A-': 3.667, 'B+': 3.333, 'B': 3.000, 'B-': 2.667,
                                        'C+': 2.333, 'C': 2.000, 'C-': 1.667, 'D+': 1.333, 'D': 1.000, 'D-': 0.667,
                                        'F': 0.000})]


def get_help_text():
    help_text = textwrap.dedent("""\
    GPA calculator
    Enter Grade Scored and Course Credit as space separated values
    E.g: A+ 3 <Enter>
    Enter blank line to designate the End

    Default mode is NG 5.0 grading system

TYPE:
    h | help <Enter> to print this Help Page
    m | mode <Enter> to change Grading mode
    q | quit <Enter> to Exit the Program\
""")
    return help_text


def get_mode_text(mode):
    mode_text = textwrap.dedent("""\
        Your current mode is %s
        ENTER:\
        """ % mode.get_name())
    # loop through COURSE_MODES and append each mode to mode_text
    # meant to prevent hardcoded text
    # user choose input that corresponds to preferred mode
    modes = 0
    for course_mode in COURSE_MODES:
        modes += 1
        mode_text += """
        %i <ENTER>    - for %s mode
        """ % (modes, course_mode.get_name())
    return mode_text


def compute_gpa(user_grades, grade_points):
    total_course_units = 0
    total_point_scored = 0
    for grade, units in user_grades.items():
        for unit in units:
            total_course_units += unit
            total_point_scored += unit * grade_points[grade]
    # In case of zero credit unit, avoid division by zero
    if total_course_units == 0:
        return 0
    average_point = total_point_scored / total_course_units
    return round(average_point, 2)


def prompt_user_input(mode):
    prompt = 1
    user_grades = defaultdict(list)
    done = False
    while not done:
        user_input = input("[%i] " % prompt)
        entered_grade = user_input.split()
        if user_input == "h" or user_input == "help":
            print(get_help_text())
        elif user_input == "m" or user_input == "mode":
            print(get_mode_text(mode))
            preferred_choice = input("[mode] ")
            # check if user's mode choice is valid
            # if invalid continue with current mode
            if preferred_choice not in [str(i) for i in range(1, len(COURSE_MODES) + 1)]:
                print("oops! Invalid mode")
                continue
            # valid mode choice
            # change the CourseMode, reset the Prompt and previously entered user grades
            else:
                mode_index = int(preferred_choice) - 1
                mode = COURSE_MODES[mode_index]
                prompt = 1
                user_grades = defaultdict(list)
                print(textwrap.dedent("""\
                Using grade %s
                Valid Grades are: %s\
                """ % (mode.get_name(), ', '.join(mode.get_grade_letters()))))

        elif user_input == "q" or user_input == "quit":
            print("Bye")
            sys.exit()
        elif len(entered_grade) == 0:
            done = True
        elif len(entered_grade) < 2:
            print(textwrap.dedent("""\
            Invalid Input %s skipped
            USAGE: grade_scored course_credit <Enter>
            e.g    B 6 <Enter>
            """ % user_input))
        elif not entered_grade[0] in mode.get_grade_letters():
            print(textwrap.dedent("""
            Invalid Grade %s skipped 
            VALID GRADES are : %s
            """ % (entered_grade[0], ', '.join(mode.get_grade_letters()))))
        elif not entered_grade[1].isdecimal():
            print(textwrap.dedent("""
            Invalid Course Credit. Course credit must be DIGIT
            """))
        else:
            prompt += 1
            user_grades[entered_grade[0]].append(int(entered_grade[1]))
    result = compute_gpa(user_grades, mode.get_grade_points())
    return result, mode
