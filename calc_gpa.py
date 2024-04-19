from gpa_helper import prompt_user_input
from gpa_helper import COURSE_MODES
import textwrap

if __name__ == "__main__":
    course_mode = COURSE_MODES[0]
    welcome_msg = textwrap.dedent("""\
        USAGE: grade_scored course_credit <Enter>
        e.g    B 6 <Enter>
        for each Course Entry - Blank Line to designate the END
        Current Mode : %s - Valid Grades are: %s
        TYPE: h | help     for help page
        """ % (course_mode.get_name(), ', '.join(course_mode.get_grade_letters())))
    print(welcome_msg)

    done = False
    while not done:
        result, course_mode = prompt_user_input(course_mode)
        print(type(result))
        print(result)
        print(textwrap.dedent("""
        Your GPA is: %f
        Mode: %s
        """ % (result, course_mode.get_name())))
        user_choice = input("Would you like to continue?  (y,n)")
        if user_choice == 'y':
            continue
        else:
            print("Bye")
            done = True
