from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Matric (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=105)
    date_of_birth = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100,null=True)
    email_address = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    board = models.CharField( max_length=150, null=True, blank=True)
    total_marks = models.CharField(max_length=100, null=True, blank=True)
    obtained_marks = models.CharField(max_length=100, null=True, blank=True)
    percentage = models.CharField(max_length=100,null=True, blank=True)
    roll_no = models.CharField(max_length=100,null=True, blank=True)
    fsc_board = models.CharField(max_length=100,null=True,blank=True)
    fsc_roll_no = models.CharField(max_length=100,null=True, blank=True)
    fsc_total_marks = models.CharField(max_length=100,null=True, blank=True)
    fsc_obtained_marks = models.CharField(max_length=100,null=True, blank=True)
    fsc_percentage = models.CharField(max_length=100,null=True ,blank=True)
    fsc_board = models.CharField(max_length=100,null=True ,blank=True)
    cgpa = models.FloatField(null=True, blank=True)
    university_master_program = models.CharField(max_length=300, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name