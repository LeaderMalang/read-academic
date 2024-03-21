import easyocr
import cv2

# Load the image
image = cv2.imread('2.jpg')

# Get image width and height
# image_height, image_width, _ = image.shape


# # Define the region of interest (ROI) as the lower 1/3 of the image
# start_x = 0
# start_y = (2 * image_height) // 3  # Start from 2/3 of the image vertically
# roi_width = image_width
# roi_height = image_height // 3  # Lower 1/3 of the image

# # Extract the ROI from the image
# roi_image = image[start_y:start_y + roi_height, start_x:start_x + roi_width]

# Convert the ROI image to RGB (EasyOCR requires RGB format)
roi_image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#blue and noise removal  
#detect noise and blur 

# cv2.imshow('image RGB',roi_image_rgb)
# Initialize EasyOCR
reader = easyocr.Reader(['en'],gpu=False)  # Specify language(s) you want to perform OCR in

# Perform text recognition on the ROI
result = reader.readtext(roi_image_rgb)

obtain_marks=0
total_marks=0
board_name=None
fsc_roll_no = None
# Print the recognized text
for index,detection in enumerate(result):
    text = detection[1]
    print(text)
    # if text=="Total Marks (In figures)":
    #   obtain_marks=int(result[index+1][1])
    #   total_marks=int(result[index+2][1])

    if text.lower()=="roll no.":
      fsc_roll_no=result[index+1][1]
    
    # if text.lower()=="total":
    #   total_marks=int(result[index+1][1])
    #   obtain_marks=int(result[index+2][1])
    if "rawalpindi" in text.lower():
      board_name="board of intermediate and secondary education rawalpindi"
    if "islamabad" in text.lower():
      board_name="board of intermediate and secondary education islamabad"


# percentage=float((obtain_marks/total_marks)*100)

print("Roll no.", fsc_roll_no)
# print("Obtain Marks",obtain_marks)
# print( "Total Marks",total_marks)
# print("Percentage",percentage)
# print("Board Name",board_name)


# # Display the ROI with bounding boxes around detected text (optional)
# for detection in result:
#     top_left = tuple(detection[0][0])
#     bottom_right = tuple(detection[0][2])
#     text = detection[1]
#     if text=='words) 18th':
#       continue
#     if text=='This':
#       continue

#     cv2.rectangle(roi_image, top_left, bottom_right, (0, 255, 0), 2)
#     cv2.putText(roi_image, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# #Display the ROI image with detected text
# cv2.imshow('ROI with Detected Text', roi_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

