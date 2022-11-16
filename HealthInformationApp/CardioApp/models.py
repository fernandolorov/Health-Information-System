from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
from django.contrib.auth.models import User


class StaffMember(models.Model):
	
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	#if user.groups.filter(name = 'Staff').exists():
	age = models.CharField(max_length=5, blank=True)
	telephone = models.CharField(max_length=20, blank=True)


class Patient(models.Model):

	GENDERS = (('Male', 'Male'), ('Female', 'Female'),  ('Other', 'Other'))

	name = models.CharField(max_length = 30)
	middle_name = models.CharField(max_length = 30, null = True, blank=True)
	last_name = models.CharField(max_length = 30)
	gender = models.CharField(max_length = 6, choices = GENDERS)
	birth_date = models.DateField(max_length = 30, null = True)
	nationality = models.CharField(max_length = 30)
	email = models.CharField(max_length = 30)
	visit_date = models.DateField(max_length = 30, null = True)

	def get_age(self):
		return self.birth_date

	def __str__(self):

		#return name + middle_name + last_name + '/n' +  gender + birth_date + nationality + '/n' + email + '/n' + visit_date 
		middle_name = ''
		if self.middle_name is not None:
			middle_name = middle_name + self.middle_name

		return self.name + ' ' + middle_name + ' ' + self.last_name


class Investigation(models.Model):

	patient = models.ForeignKey('Patient', on_delete=models.CASCADE)

	temperature = models.CharField(max_length = 30, blank=True)
	heart_rate = models.CharField(max_length = 30, blank=True)
	symptoms = models.CharField(max_length = 300, blank = True)
	experienced_before = models.BooleanField()

class Diagnosis(models.Model):

	patient = models.ForeignKey('Patient', on_delete=models.CASCADE)

	diagnosis = models.ForeignKey('SNOMED_Diagnosis', on_delete=models.CASCADE)
	aditional_comments = models.CharField(max_length = 30, blank=True)
	diagnosis_date = models.DateField(max_length = 30, null = True)



class Images(models.Model):
	diagnosis = models.ForeignKey('Diagnosis', default = None,  on_delete=models.CASCADE)
	image = models.ImageField(upload_to='images/', verbose_name='Image', null = True) 

class Cardiogram(models.Model):
	patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
	cardiogram = models.FileField(upload_to='cardiograms/', verbose_name='File', null = True) 

class SNOMED_Diagnosis(models.Model):

	code = models.CharField(max_length = 30, blank=True)
	snomed_diagnosis =  models.CharField(max_length = 255, blank=True)

	def __str__(self):
		return self.code + ' ' + self.snomed_diagnosis
