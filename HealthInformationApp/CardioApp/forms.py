from django.forms import ModelForm, SelectDateWidget, Select, BooleanField, ImageField, TextInput, BooleanField, FileField

from CardioApp.models import Patient, Investigation, Diagnosis, Images, Cardiogram

class PatientForm(ModelForm):

	class Meta:

		GENDERS = (('Male', 'Male'), ('Female', 'Female'))
		NACIONALITIES = (('belgian', 'Belgian'), ('spanish', 'Spanish'), )

		model = Patient
		fields = "__all__"
		widgets = {
			'name': TextInput(attrs={'class': 'form-control',}),
			'middle_name': TextInput(attrs={'class': 'form-control',}),
			'last_name': TextInput(attrs={'class': 'form-control',}),
            'birth_date': SelectDateWidget(years = range(1900, 2020), attrs={'class':'form-control'}),
            'visit_date': SelectDateWidget(attrs={'class':'form-control'}),
            'gender': Select(choices=GENDERS, attrs={'class':'form-control'}),
          	'nationality': Select(choices=NACIONALITIES, attrs={'class':'form-control'}),
			'email': TextInput(attrs={'class': 'form-control',}),
        }

class InvestigationForm(ModelForm):

	class Meta:

		model = Investigation
		fields = "__all__"
		widgets = {
			'patient': Select(attrs={'class':'form-control'}),
			'temperature': TextInput(attrs={'class': 'form-control',}),
			'heart_rate': TextInput(attrs={'class': 'form-control',}),
            'symptoms': TextInput(attrs={'class': 'form-control',}),
        }
	
class DiagnosisForm(ModelForm):

	class Meta:

		model = Diagnosis
		fields = "__all__"
		widgets = {
			'patient': Select(attrs={'class':'form-control'}),
			'diagnosis': Select(attrs={'class':'form-control'}),
			'aditional_comments':  TextInput(attrs={'class': 'form-control',}),
        	'diagnosis_date': SelectDateWidget(attrs={'class':'form-control'}),

        }

class ImageForm(ModelForm):

	image = ImageField(label='Image')
	class Meta:
		model = Images
		fields = ('image',)

class CardiogramForm(ModelForm):

	cardiogram = FileField(label='File')
	class Meta:

		model = Cardiogram
		
		fields = "__all__"
		widgets = {
			'patient': Select(attrs={'class':'form-control'}),
	    }

'''
class ImageForm(ModelForm):
	class Meta:
		model = Image
		fields= "__all__"
'''