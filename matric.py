import easyocr
import cv2

# Load the image
image = cv2.imread('new_matric.jpg')

# Convert the image to RGB (EasyOCR requires RGB format)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=False)  # Specify language(s) you want to perform OCR in

result = reader.readtext(image_rgb)

roll_number=None
board_name=None
total_marks = None
obtain_marks = None
# Print the recognized text

for index,detection in enumerate(result):
    text = detection[1]
    # print(text)
    if text.lower()=="roll no.":
      roll_number=result[index+1][1]
    if text.lower()=="total":
      total_marks=int(result[index+1][1])
      obtain_marks=int(result[index+2][1])
    # if text.lower()=="roll no":
    #   roll_number=result[index+1][1]
    # if text=="Marks (In figures)":
    #   obtain_marks=int(result[index+1][1])
    #   total_marks=int(result[index+2][1])
    if "islamabad" in text.lower():
      board_name="board of intermediate and secondary education Islamabad"
    # if "rawalpindi" in text.lower():
    #   board_name="board of intermediate and secondary education, rawalpindi secondary school certificate examination"

    # print(text)

percentage=float((obtain_marks/total_marks)*100)

print('Roll Number:', roll_number)
print("Total Marks:", total_marks)
print("Obtain Marks:", obtain_marks)
print("Percentage:", percentage)
print("Board Name:", board_name)



# Optionally, you can display the entire image with bounding boxes around detected text
# for detection in result:
#     top_left = tuple(detection[0][0])
#     bottom_right = tuple(detection[0][2])
#     text = detection[1]
#     cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
#     cv2.putText(image, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# # Display the image with detected text
# cv2.imshow('Image with Detected Text', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

