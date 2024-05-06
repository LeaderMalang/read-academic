import os
from django.http import HttpResponse
import time
import easyocr
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from concurrent.futures import ThreadPoolExecutor
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import easyocr
import cv2
from django.contrib.auth.decorators import login_required



# import models
from .models import Matric
# import services (extract data)
from .services.processFile import process_file
from .services.fscData import extract_fsc_data
from .services.idCardNo import extract_idCard_no
from .services.matricData import extract_matric_data
from .services.dateOfBirth import extract_date_of_birth
# import utils (utility functions)
from .utils.calculatePercentage import calculate_percentage
from .utils.createURL import create_url
import threading
lock = threading.Lock()
# ------------------------------------------------------------------------
reader = easyocr.Reader(['en'], gpu=False)
# Initialize all variables


matric_total_marks=0
matric_obtained_marks=0
matric_percentage=0
martic_roll_no=None
martic_board=None

global fsc_total_marks
global fsc_obtained_marks
global fsc_percentage
global fsc_board
global fsc_roll_no

fsc_total_marks = None
fsc_obtained_marks = None
fsc_percentage = None
fsc_board = None
fsc_roll_no = None

global idCard_number
global student_name
global father_name
global date_of_birth


idCard_number = None
student_name = None
father_name = None
date_of_birth = None
# @login_required(login_url='/login/')
# def index(request):
#     if request.method == "POST":
#         try:
#             # for testing only
#             start_time = time.time() 
            
#             # ------------------------------- 
#             # Get files from request
#             ID_CARD_FILE = request.FILES.get('idCard')
#             MATRIC_SANAT_FILE = request.FILES.get('matricSanat')
#             FSC_SANAT_FILE = request.FILES.get('fscSanat')


            
#             # ------------------------------- 
#             # Initiallize all variables
#             idCard_number = None
#             matric_total_marks = None
#             matric_obtained_marks = None
#             matric_percentage = None
#             student_name = None
#             father_name = None
#             date_of_birth = None
#             martic_roll_no = None
#             martic_board = None
#             fsc_total_marks = None
#             fsc_obtained_marks = None
#             fsc_percentage = None
#             fsc_board = None
#             fsc_roll_no = None
            
            
            
#             # ------------------------------- 
#             # Load easy ocr model
#             ocr_reader = easyocr.Reader(['en'])
#             print("> Model loaded")



#             # ------------------------------- 
#             # Check if the 'uploads' directory exists 
#             # Create the 'uploads' directory if it not exists
#             uploads_dir = os.path.join(settings.BASE_DIR, 'uploads')
#             os.makedirs(uploads_dir, exist_ok=True)
#             print(">> Directory confirmed")



#             # ------------------------------- 
#             # Save the file to the 'uploads' directory
#             # Scan files and get scanned text
#             with ThreadPoolExecutor(max_workers=None) as executor:
#                 if ID_CARD_FILE:
#                     future_id_card = executor.submit(process_file, uploads_dir, ID_CARD_FILE, ocr_reader)

#                 if MATRIC_SANAT_FILE:
#                     future_matric_sanat = executor.submit(process_file, uploads_dir, MATRIC_SANAT_FILE, ocr_reader)

#                 if FSC_SANAT_FILE:
#                     future_fsc_sanat = executor.submit(process_file, uploads_dir, FSC_SANAT_FILE, ocr_reader)

#                 # scanned files data
#                 SCANNED_ID_CARD = future_id_card.result() if ID_CARD_FILE else None
#                 SCANNED_MATRIC_SANAT = future_matric_sanat.result() if MATRIC_SANAT_FILE else None
#                 SCANNED_FSC_SANAT = future_fsc_sanat.result() if FSC_SANAT_FILE else None

#             # ------------------------------- 
#             # Extract data from scanned text
#             ## Matric Values
#             matric_data = extract_matric_data(SCANNED_MATRIC_SANAT)
#             martic_board = matric_data["board"] # matric board
#             martic_roll_no = matric_data["roll_no"] # matric roll
#             matric_total_marks = matric_data["total_marks"] # matric total marks
#             matric_obtained_marks = matric_data["obtained_marks"] # matric obtained marks
#             matric_percentage = calculate_percentage(matric_total_marks, matric_obtained_marks) # matric percentage

#             ## FSC Values
#             fsc_data = extract_fsc_data(SCANNED_FSC_SANAT)
#             fsc_board = fsc_data["board"] # fsc board
#             fsc_roll_no = fsc_data["roll_no"] # fsc roll
#             fsc_total_marks = fsc_data["total_marks"] # fsc total marks
#             fsc_obtained_marks = fsc_data["obtained_marks"] # fsc obtained marks
#             fsc_percentage = calculate_percentage(fsc_total_marks, fsc_obtained_marks) # fsc percentage
                
#             ## Personal Values
#             idCard_number = extract_idCard_no(SCANNED_ID_CARD) # id card no
#             date_of_birth = extract_date_of_birth(SCANNED_MATRIC_SANAT) # dob
#             student_name = matric_data["certified_name"] # student name
#             father_name = matric_data["son_daughter_of"] # father name
        
#         except:
#             print("\n\n---- AN ERROR OCCURED ----- \n\n")



#         # ------------------------------- 
#         # URL of the 'form' view 
#         # Values as parameters
#         form_url = create_url(idCard_number, matric_total_marks, matric_obtained_marks, matric_percentage, student_name, father_name, date_of_birth,  martic_roll_no, martic_board, fsc_total_marks, fsc_obtained_marks, fsc_percentage, fsc_board, fsc_roll_no)



#         # for testing only
#         print("\n\nTOTAL TIME TAKEN: ", int(time.time() - start_time), "seconds\n\n") 
            
            
#         # ------------------------------- 
#         # Redirect to the 'form' page 
#         return redirect(form_url)
            
#     return render(request, "index.html")
def matric_data_extraction(img_path):
    global matric_obtained_marks 
    global matric_total_marks 
    global matric_percentage 
    global martic_roll_no
    global martic_board
    with lock: 
        matric_image = cv2.imread(img_path)
        if matric_image is None:

            raise Exception("Matric image not found or could not be read")
        matric_image_rgb = cv2.cvtColor(matric_image, cv2.COLOR_BGR2RGB)
        matric_result = reader.readtext(matric_image_rgb)
        
        for index, detection in enumerate(matric_result):
            text = detection[1]
            print(f'Matric Result: {text}')
            if text.lower() == "roll no":
                martic_roll_no = matric_result[index+1][1].replace('_cahoreBoardon','')
            if text.lower() == "roll no.":
                martic_roll_no = matric_result[index+1][1]

            if text == "TOTAL MARKS (In Fiqures)":
                matric_obtained_marks = int(matric_result[index+7][1])
                matric_total_marks = int(matric_result[index+6][1])
            if text == "TOTAL MARKS (In figures)":
                matric_obtained_marks = int(matric_result[index+4][1])
                matric_total_marks = int(matric_result[index+3][1])

            if text.lower() == "marks (in figures)":
                matric_obtained_marks = int(matric_result[index+1][1])
                matric_total_marks = int(matric_result[index+2][1])
            if text.lower() == "out":
                if len(matric_result) > index+2 and len(matric_result[index+2]) > 1:
                    element_to_convert = str(matric_result[index+2][1])
                    matric_total_marks = int(element_to_convert.rstrip("_"))
            # if text.lower() == "marks":
            #     matric_obtained_marks = int(matric_result[index-1][1])
            if text == "TOTAL":
                matric_total_marks = int(matric_result[index+1][1])
                matric_obtained_marks = int(matric_result[index+2][1])
            if "islamabad" in text.lower():
                martic_board= "board of intermediate and secondary education Islamabad"
            if "rawalpindi" in text.lower():
                martic_board = "board of intermediate and secondary education rawalpindi"

            if "multan" in text.lower():
                martic_board = "board of intermediate and secondary education multan"
            if "lahore" in text.lower():
                martic_board = "board of intermediate and secondary education lahore"

            if "faisalabad" in text.lower():
                martic_board = "board of intermediate and secondary education faisalabad"


        if matric_total_marks is not None and matric_total_marks != 0:
            matric_percentage = float((matric_obtained_marks / matric_total_marks) * 100)
    
    print("Job Done")

def fsc_data_extraction(img_path):
    global fsc_obtained_marks 
    global fsc_total_marks 
    global fsc_percentage 
    global fsc_board
    with lock: 
        fsc_image = cv2.imread(img_path)
        if fsc_image is None:
            raise Exception("FSC image not found or could not be read")

        # image_height, image_width, _ = fsc_image.shape
        # start_x = 0
        # start_y = (2 * image_height) // 3
        # roi_width = image_width
        # roi_height = image_height // 3

        # fsc_roi_image = fsc_image[start_y:start_y + roi_height,start_x:start_x + roi_width]
        fsc_image_rgb = cv2.cvtColor(fsc_image, cv2.COLOR_BGR2RGB)
        fsc_result = reader.readtext(fsc_image_rgb)

        for index, detection in enumerate(fsc_result):
            text = detection[1]
            print(f'FSC Result: {text}')
            if text.lower() == "total marks (in figures)":
                fsc_obtained_marks = int(fsc_result[index+1][1])
                fsc_total_marks = int(fsc_result[index+2][1])
            if text.lower() == "total marks  (in figures)":
                fsc_obtained_marks = int(fsc_result[index-1][1])
                fsc_total_marks = int(fsc_result[index-2][1])
            if text.lower() == "total":
                fsc_total_marks = int(fsc_result[index+3][1])
                fsc_obtained_marks = int(fsc_result[index+2][1])
            if text.lower() == "oul":
                fsc_total_marks = int(fsc_result[index+2][1])
            if text.lower() == "out":
                fsc_total_marks = int(fsc_result[index+2][1])
            # if text.lower() == "marks":
            #     fsc_obtained_marks = int(fsc_result[index-3][1])
            if "rawalpindi" in text.lower():
                fsc_board = "board of intermediate and secondary education rawalpindi"
            if "islamabad" in text.lower():
                fsc_board = "board of intermediate and secondary education islamabad"

            if "multan" in text.lower():
                fsc_board = "board of intermediate and secondary education multan"
            if "lahore" in text.lower():
                fsc_board = "board of intermediate and secondary education lahore"

            if "faisalabad" in text.lower():
                fsc_board = "board of intermediate and secondary education faisalabad"


        if fsc_total_marks is not None and fsc_total_marks != 0:
            fsc_percentage = float((fsc_obtained_marks / fsc_total_marks) * 100)
    
    print("Job Done")

def id_card_data_extraction(img_path):
    global idCard_number 
    global date_of_birth 
    global student_name 
    global father_name
    with lock: 
        id_card_image = cv2.imread(img_path)
        if id_card_image is None:
            raise Exception("ID card image not found or could not be read")

        id_card_image_rgb = cv2.cvtColor(id_card_image, cv2.COLOR_BGR2RGB)
        id_card_result = reader.readtext(id_card_image_rgb)

        for index, detection in enumerate(id_card_result):
            text = detection[1]
            print(text)
            if text.lower() == "identity number":
                idCard_number = id_card_result[index + 2][1]
            if text.lower() == "identity number":
                date_of_birth = id_card_result[index + 3][1]
            if text.lower() == "name":
                student_name = id_card_result[index + 1][1]
            if text.lower() == "father name":
                father_name = id_card_result[index + 1][1]
    
    print("Job Done")

@login_required(login_url='/login/')
def index(request):
    # Check if record already exists
    if request.method == "GET":
        try:
            # Check if record already exists
            result = Matric.objects.get(user=request.user)
            return render(request, "already.html", {'result': result})
        except Matric.DoesNotExist:
            pass
        
    elif request.method == "POST":
        try:
            
            # for testing only
            
            start_time = time.time() 
            
            # ------------------------------- 
            # Get files from request
            ID_CARD_FILE = request.FILES.get('idCard')
            MATRIC_SANAT_FILE = request.FILES.get('matricSanat')
            FSC_SANAT_FILE = request.FILES.get('fscSanat')
            CGPA = request.POST.get('cgpa')
            UNI_MASTER_PROGRAM = request.POST.get('master_program')
            UNI_YEAR = request.POST.get('user_year')

            # Check if the 'uploads' directory exists 
            # Create the 'uploads' directory if it does not exist
            uploads_dir = os.path.join(settings.BASE_DIR, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            print(">> Directory confirmed")

            # Save files to the 'uploads' directory
            id_card_path = os.path.join(uploads_dir, ID_CARD_FILE.name)
            with open(id_card_path, 'wb+') as destination:
                for chunk in ID_CARD_FILE.chunks():
                    destination.write(chunk)

            matric_sanat_path = os.path.join(uploads_dir, MATRIC_SANAT_FILE.name)
            with open(matric_sanat_path, 'wb+') as destination:
                for chunk in MATRIC_SANAT_FILE.chunks():
                    destination.write(chunk)

            fsc_sanat_path = os.path.join(uploads_dir, FSC_SANAT_FILE.name)
            with open(fsc_sanat_path, 'wb+') as destination:
                for chunk in FSC_SANAT_FILE.chunks():
                    destination.write(chunk)
            
            
            cgpa = CGPA
            uni_master_program = UNI_MASTER_PROGRAM
            uni_year = UNI_YEAR
            

            # For Matric
            
            matric_thread=threading.Thread(target=matric_data_extraction,args=(matric_sanat_path,))
            matric_thread.start()
            # Wait until the thread completes
            matric_thread.join()

            # For FSC
            fsc_thread=threading.Thread(target=fsc_data_extraction,args=(fsc_sanat_path,))
            fsc_thread.start()
            # Wait until the thread completes
            fsc_thread.join()

            # For idCard
            id_card_thread=threading.Thread(target=id_card_data_extraction,args=(id_card_path,))
            id_card_thread.start()
            # Wait until the thread completes
            id_card_thread.join()


            # URL of the 'form' view 
            # Values as parameters
            
            form_url = create_url(idCard_number, matric_total_marks, matric_obtained_marks, matric_percentage, student_name, father_name, date_of_birth, martic_roll_no, martic_board, fsc_total_marks, fsc_obtained_marks, fsc_percentage, fsc_board, fsc_roll_no, cgpa, uni_master_program, uni_year)

            # for testing only
            print("\n\nTOTAL TIME TAKEN: ", int(time.time() - start_time), "seconds\n\n") 

            # Redirect to the 'form' page 
            return redirect(form_url)
            
        except Exception as e:
            error_message = str(e)
            return HttpResponse(error_message)
    
    return render(request, "index.html")

# ------------------------------------------------------------------------

@login_required(login_url='/login/')
def form(request):
    idCard_number = request.GET.get('idCard_number', None)
    total_marks = request.GET.get('total_marks', None)
    obtained_marks = request.GET.get('obtained_marks', None)
    percentage = request.GET.get('percentage', None)
    student_name = request.GET.get('student_name', None)
    father_name = request.GET.get('father_name', None)
    roll_no = request.GET.get('roll_no', None)
    board = request.GET.get('board', None)
    fsc_total_marks = request.GET.get('fsc_total_marks', None)
    fsc_obtained_marks = request.GET.get('fsc_obtained_marks', None)
    fsc_percentage = request.GET.get('fsc_percentage', None)
    fsc_board = request.GET.get('fsc_board', None)
    fsc_roll_no = request.GET.get('fsc_roll_no', None)
    date_of_birth = request.GET.get('date_of_birth', None)
    cgpa = request.GET.get('cgpa', None)
    uni_master_program = request.GET.get('uni_master_program', None)
    uni_year = request.GET.get('uni_year', None)
    
    if request.method == 'POST':
        form_email_address = request.POST.get('email_address')
        form_address = request.POST.get('address')
        form_phone_number = request.POST.get('phone_number')

        matric = Matric.objects.create()

        matric.user = request.user
        matric.name = idCard_number
        matric.date_of_birth = date_of_birth
        matric.student_name = student_name
        matric.father_name = father_name
        matric.email_address = form_email_address
        matric.address = form_address
        matric.phone_number = form_phone_number
        matric.board = board
        matric.total_marks = total_marks 
        matric.obtained_marks = obtained_marks
        matric.percentage = percentage
        matric.roll_no = roll_no
        matric.fsc_total_marks = fsc_total_marks
        matric.fsc_obtained_marks = fsc_obtained_marks
        matric.fsc_percentage = fsc_percentage
        matric.fsc_board = fsc_board
        if cgpa and uni_master_program and uni_year:
            matric.cgpa = cgpa
            matric.university_master_program = uni_master_program
            matric.year = uni_year
        matric.save()
        return redirect('index')
   

    # Pass idCard_number to the template
    return render(request, "submit.html", {'idCard_number': idCard_number,'obtained_marks': obtained_marks, 'total_marks': total_marks, 
                                           'percentage': percentage, 'student_name': student_name , 'father_name': father_name, 'roll_no': roll_no, 'board': board, 'fsc_total_marks': fsc_total_marks, 'fsc_obtained_marks': fsc_obtained_marks, 'fsc_percentage': fsc_percentage, 'fsc_board':fsc_board, 'fsc_roll_no': fsc_roll_no, 'birth_date': date_of_birth, 'cgpa':cgpa, 'university_master_program': uni_master_program, 'univeristy_year': uni_year})

# ------------------------------------------------------------------------
@login_required(login_url='/login/')
def app_admin(request):
    if request.user.is_staff:
        records = Matric.objects.all()
        print("RECORDS")
        print(records)
        print("RECORDS")
        return render(request, 'admin.html', {'records': records})
    else:
        return render(request, 'admin.html', {'error': "You are not logged in as an admin"})

# ------------------------------------------------------------------------

def login(request):
    if request.user.is_authenticated:
        return render(request, 'Login.html', {'already_logged_in': True})
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_staff:
                return redirect(reverse('app_admin'))
            else:
                return redirect(reverse('index'))
        elif user is not None and not user.is_active:
            return render(request, 'Login.html', {'error': "Your admin request is in processing. Please wait for approval."})
        elif user is None:
            return render(request, 'Login.html', {'error': "Invalid username or password"})
    else:
        return render(request, 'Login.html')
    
# ------------------------------------------------------------------------

def signup(request):
    if request.user.is_authenticated:
        return render(request, 'Signup.html', {'already_logged_in': True})
    
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_superuser = request.POST.get('is_superuser')
        
        if User.objects.filter(email=email).exists():
            return render(request, 'Signup.html', {'error': 'User with this email already exists'})
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = fullname.split()[0] 
        user.last_name = ' '.join(fullname.split()[1:]) 
        # 
        user.is_superuser = True if is_superuser else False
        user.is_staff = True if is_superuser else False
        user.is_active = False if is_superuser else True
        user.save()
    
        return redirect('/login/') 
    else:
        return render(request, 'Signup.html')

# ------------------------------------------------------------------------

@login_required
def logout(request):
    auth_logout(request)
    return redirect('/login/')