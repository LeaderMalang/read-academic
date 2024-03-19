import os
import time
import easyocr
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from concurrent.futures import ThreadPoolExecutor
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
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
# ------------------------------------------------------------------------

@login_required(login_url='/login/')
def index(request):
    if request.method == "POST":
        try:
            # for testing only
            start_time = time.time() 
            
            # ------------------------------- 
            # Get files from request
            ID_CARD_FILE = request.FILES.get('idCard')
            MATRIC_SANAT_FILE = request.FILES.get('matricSanat')
            FSC_SANAT_FILE = request.FILES.get('fscSanat')


            
            # ------------------------------- 
            # Initiallize all variables
            idCard_number = None
            matric_total_marks = None
            matric_obtained_marks = None
            matric_percentage = None
            student_name = None
            father_name = None
            date_of_birth = None
            martic_roll_no = None
            martic_board = None
            fsc_total_marks = None
            fsc_obtained_marks = None
            fsc_percentage = None
            fsc_board = None
            fsc_roll_no = None
            
            
            
            # ------------------------------- 
            # Load easy ocr model
            ocr_reader = easyocr.Reader(['en'])
            print("> Model loaded")



            # ------------------------------- 
            # Check if the 'uploads' directory exists 
            # Create the 'uploads' directory if it not exists
            uploads_dir = os.path.join(settings.BASE_DIR, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            print(">> Directory confirmed")



            # ------------------------------- 
            # Save the file to the 'uploads' directory
            # Scan files and get scanned text
            with ThreadPoolExecutor(max_workers=None) as executor:
                if ID_CARD_FILE:
                    future_id_card = executor.submit(process_file, uploads_dir, ID_CARD_FILE, ocr_reader)

                if MATRIC_SANAT_FILE:
                    future_matric_sanat = executor.submit(process_file, uploads_dir, MATRIC_SANAT_FILE, ocr_reader)

                if FSC_SANAT_FILE:
                    future_fsc_sanat = executor.submit(process_file, uploads_dir, FSC_SANAT_FILE, ocr_reader)

                # scanned files data
                SCANNED_ID_CARD = future_id_card.result() if ID_CARD_FILE else None
                SCANNED_MATRIC_SANAT = future_matric_sanat.result() if MATRIC_SANAT_FILE else None
                SCANNED_FSC_SANAT = future_fsc_sanat.result() if FSC_SANAT_FILE else None

            # ------------------------------- 
            # Extract data from scanned text
            ## Matric Values
            matric_data = extract_matric_data(SCANNED_MATRIC_SANAT)
            martic_board = matric_data["board"] # matric board
            martic_roll_no = matric_data["roll_no"] # matric roll
            matric_total_marks = matric_data["total_marks"] # matric total marks
            matric_obtained_marks = matric_data["obtained_marks"] # matric obtained marks
            matric_percentage = calculate_percentage(matric_total_marks, matric_obtained_marks) # matric percentage

            ## FSC Values
            fsc_data = extract_fsc_data(SCANNED_FSC_SANAT)
            fsc_board = fsc_data["board"] # fsc board
            fsc_roll_no = fsc_data["roll_no"] # fsc roll
            fsc_total_marks = fsc_data["total_marks"] # fsc total marks
            fsc_obtained_marks = fsc_data["obtained_marks"] # fsc obtained marks
            fsc_percentage = calculate_percentage(fsc_total_marks, fsc_obtained_marks) # fsc percentage
                
            ## Personal Values
            idCard_number = extract_idCard_no(SCANNED_ID_CARD) # id card no
            date_of_birth = extract_date_of_birth(SCANNED_MATRIC_SANAT) # dob
            student_name = matric_data["certified_name"] # student name
            father_name = matric_data["son_daughter_of"] # father name
        
        except:
            print("\n\n---- AN ERROR OCCURED ----- \n\n")



        # ------------------------------- 
        # URL of the 'form' view 
        # Values as parameters
        form_url = create_url(idCard_number, matric_total_marks, matric_obtained_marks, matric_percentage, student_name, father_name, date_of_birth,  martic_roll_no, martic_board, fsc_total_marks, fsc_obtained_marks, fsc_percentage, fsc_board, fsc_roll_no)



        # for testing only
        print("\n\nTOTAL TIME TAKEN: ", int(time.time() - start_time), "seconds\n\n") 
            
            
        # ------------------------------- 
        # Redirect to the 'form' page 
        return redirect(form_url)
            
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

    if request.method == 'POST':
        form_email_address = request.POST.get('email_address')
        form_address = request.POST.get('address')
        form_phone_number = request.POST.get('phone_number')

        matric = Matric.objects.create()


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
        matric.fsc_roll_no = fsc_roll_no
        matric.save()
        return redirect('index')
   

    # Pass idCard_number to the template
    return render(request, "submit.html", {'idCard_number': idCard_number,'obtained_marks': obtained_marks, 'total_marks': total_marks, 
                                           'percentage': percentage, 'student_name': student_name , 'father_name': father_name, 'roll_no': roll_no, 'board': board, 'fsc_total_marks': fsc_total_marks, 'fsc_obtained_marks': fsc_obtained_marks, 'fsc_percentage': fsc_percentage, 'fsc_board':fsc_board, 'fsc_roll_no': fsc_roll_no, 'birth_date': date_of_birth})

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