import threading



# Initialize all variables
matric_total_marks = None
matric_obtained_marks = None
matric_percentage = None
martic_roll_no = None
martic_board = None

fsc_total_marks = None
fsc_obtained_marks = None
fsc_percentage = None
fsc_board = None
fsc_roll_no = None

idCard_number = None
student_name = None
father_name = None
date_of_birth = None

class NewThreadedTask(threading.Thread):

  def __init__(self):
    super(NewThreadedTask, self).__init__()
 
  def run(self):
    # run some code here
    print('Threaded task has been completed')