import easyocr
import cv2

# Load the image
image = cv2.imread('wasi_id_card.jpg')

# Convert the image to RGB (EasyOCR requires RGB format)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=False)  # Specify language(s) you want to perform OCR in

result = reader.readtext(image_rgb)

id_number = None
name = None
father_name = None
date_of_birth = None
# Process OCR results
for index, detection in enumerate(result):
    text = detection[1]
    print(text)
    if text.lower() == "identity number":
        id_number = result[index + 2][1]
    if text.lower() == "identity number":
        date_of_birth = result[index + 3][1]
    if text.lower() == "name":
        name = result[index + 1][1]
    if text.lower() == "father name":
        father_name = result[index + 1][1]
# Display results
print("ID number:", id_number)
print("Name:", name)
print("DOB:", date_of_birth)
print("Father Name:", father_name)

# Optionally, you can display the entire image with bounding boxes around detected text
for detection in result:
    text = detection[1]

# Display the image with detected text
# cv2.imshow('Image with Detected Text', image_rgb)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
