
import easyocr
import cv2

ID_CARD_FILE = request.FILES.get('idCard')
MATRIC_SANAT_FILE = request.FILES.get('matricSanat')
FSC_SANAT_FILE = request.FILES.get('fscSanat')

# Initiallize all variables

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


reader = easyocr.Reader(['en'], gpu=False)

# For Matric

matric_image = cv2.imread(MATRIC_SANAT_FILE)
matric_image_rgb = cv2.cvtColor(matric_image, cv2.COLOR_BGR2RGB)
matric_result = reader.readtext(matric_image_rgb)
for index,detection in enumerate(matric_result):
    text = detection[1]
    if text.lower()=="roll no.":
      martic_roll_no=matric_result[index+1][1]
    if text.lower()=="total":
      matric_total_marks=int(matric_result[index+1][1])
      matric_obtained_marks=int(matric_result[index+2][1])
    if "islamabad" in text.lower():
      martic_board="board of intermediate and secondary education Islamabad"

matric_percentage=float((matric_obtained_marks/matric_total_marks)*100)

# For FSC

fsc_image = cv2.imread(FSC_SANAT_FILE)


image_height, image_width, _ = fsc_image.shape

start_x = 0
start_y = (2 * image_height) // 3
roi_width = image_width
roi_height = image_height // 3

fsc_roi_image = fsc_image[start_y:start_y + roi_height, start_x:start_x + roi_width]
fsc_image_rgb = cv2.cvtColor(fsc_roi_image, cv2.COLOR_BGR2RGB)
fsc_result = reader.readtext(fsc_image_rgb)

for index,detection in enumerate(fsc_result):
    text = detection[1]
    if text=="Total Marks (In figures)":
      fsc_obtained_marks=int(fsc_result[index+1][1])
      fsc_total_marks=int(fsc_result[index+2][1])
    
    if text.lower()=="total":
      fsc_total_marks=int(fsc_result[index+1][1])
      fsc_obtained_marks=int(fsc_result[index+2][1])
    if "rawalpindi" in text.lower():
      fsc_board="board of intermediate and secondary education rawalpindi"
    if "islamabad" in text.lower():
      fsc_board="board of intermediate and secondary education islamabad"


percentage=float((fsc_obtained_marks/fsc_total_marks)*100)

# For ID Card


id_card_image = cv2.imread(ID_CARD_FILE)

id_card_image_rgb = cv2.cvtColor(id_card_image, cv2.COLOR_BGR2RGB)

id_card_result = reader.readtext(id_card_image_rgb)

for index, detection in enumerate(id_card_result):
    text = detection[1]
    # print(text)
    if text.lower() == "identity number":
        idCard_number = id_card_result[index + 2][1]
    if text.lower() == "identity number":
        date_of_birth = id_card_result[index + 3][1]
    if text.lower() == "name":
        student_name = id_card_result[index + 1][1]
    if text.lower() == "father name":
        father_name = id_card_result[index + 1][1]
