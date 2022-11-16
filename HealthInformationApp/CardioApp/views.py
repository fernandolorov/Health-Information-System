from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group 
from django.contrib import messages
from django.forms import modelformset_factory
from django.core.paginator import Paginator


from CardioApp.forms import PatientForm, InvestigationForm, DiagnosisForm, ImageForm, CardiogramForm
from CardioApp.models import Patient, Investigation, Diagnosis, Images, Cardiogram
from CardioApp.cardiogramutilities import *

# Create your views here.

@permission_required("CardioApp.view_patient", login_url="accounts/login/")
def homepage(request):
	try:
		request.session['views_counter'] = request.session['views_counter'] + 1
	except:	
		request.session['views_counter'] = 1

	#We render the Patient or Staff homepage:
	groups = list(request.user.groups.all().values_list('name', flat = True))
	if "Patients" in groups:
		patient = Patient.objects.all().get(name=request.user.first_name, last_name = request.user.last_name)
		print(Diagnosis.objects.all().filter(patient=patient))
		context = {
			"patient" : patient,
			"diagnosis_list": Diagnosis.objects.all().filter(patient=patient),
			"investigations_list": Investigation.objects.all().filter(patient=patient),
			"cardiogram_list": Cardiogram.objects.all().filter(patient=patient),
		}
		return render(request, 'patient_homepage_template.html', context)
	else:
		context = {
			"patients_number": Patient.objects.count(), 
			"diagnosis_number" : Diagnosis.objects.count(), 
			"investigation_number" : Investigation.objects.count(),
			"cardiogram_number" : Cardiogram.objects.count(),
			}
		return render(request, 'homepage_template.html', context)

@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def patient_list(request):
	request.session['views_counter'] = request.session['views_counter'] + 1
	patient_list = Paginator(Patient.objects.get_queryset().order_by('id'), 10)
	page = request.GET.get('page', 1)
	try:
		paginator = patient_list.page(page)
	except:
		paginator = patient_list.page(1)
	context = {
		"patients_number": Patient.objects.count(),
		"paginator": paginator,
		}
	return render(request, 'patient_list_template.html', context)

@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def investigation_list(request):
	request.session['views_counter'] = request.session['views_counter'] + 1
	investigation_list = Paginator(Investigation.objects.get_queryset().order_by('id'), 10)
	page = request.GET.get('page', 1)
	try:
		paginator = investigation_list.page(page)
	except:
		paginator = investigation_list.page(1)
	context = {
		"investigations_number": Investigation.objects.count(), 
		"paginator": paginator,
		}
	return render(request, 'investigation_list_template.html', context)

@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def diagnosis_list(request):

	request.session['views_counter'] = request.session['views_counter'] + 1
	diagnosis_list = Paginator(Diagnosis.objects.get_queryset().order_by('id'), 10)
	page = request.GET.get('page', 1)
	try:
		paginator = diagnosis_list.page(page)
	except:
		paginator = diagnosis_list.page(1)

	context = {
		"diagnosis_number": Diagnosis.objects.count(),
		"diagnosis_list":  Diagnosis.objects.all(), 
		"paginator": paginator,
		}
	return render(request, 'diagnosis_list_template.html', context)

@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def cardiogram_list(request):

	request.session['views_counter'] = request.session['views_counter'] + 1
	cardiogram_list = Paginator(Cardiogram.objects.get_queryset().order_by('id'), 10)
	page = request.GET.get('page', 1)
	try:
		paginator = cardiogram_list.page(page)
	except:
		paginator = cardiogram_list.page(1)

	context = {
		"cardiogram_number": Cardiogram.objects.count(),
		"cardiogram_list":  Cardiogram.objects.all(), 
		"paginator": paginator,
		}
	return render(request, 'cardiogram_list_template.html', context)


@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def new_patient(request):
	request.session['views_counter'] = request.session['views_counter'] + 1
	if request.method == "POST":
		patient_form = PatientForm(request.POST)
		context = {}

		if patient_form.is_valid():
			
			name = patient_form.cleaned_data['name']
			middle_name = patient_form.cleaned_data['middle_name']
			last_name = patient_form.cleaned_data['last_name']
			gender = patient_form.cleaned_data['gender']
			birth_date = patient_form.cleaned_data['birth_date']
			nationality = patient_form.cleaned_data['nationality']
			email = patient_form.cleaned_data['email']
			visit_date = patient_form.cleaned_data['visit_date']

			#Save it in the new database
			patient = Patient(name=name, middle_name=middle_name, last_name=last_name, gender=gender, birth_date=birth_date, nationality=nationality, email=email, visit_date=visit_date)
			patient.save()

			#Create the new user:
			password = name + "_" + last_name
			user = User.objects.create_user(username=email, password=password, email=email, first_name=name, last_name=last_name)
			user.save()
			group = Group.objects.get(name='Patients') 
			group.user_set.add(user)
			group.save()

			#Redirect to a new url
			return HttpResponseRedirect(reverse('patient_list') )
	else:
		patient_form = PatientForm()
		context = {"form": patient_form}
	return render(request, 'new_patient_template.html', context)


@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def new_investigation(request):
	request.session['views_counter'] = request.session['views_counter'] + 1
	if request.method == "POST":
		investigation_form = InvestigationForm(request.POST)
		context = {}

		if investigation_form.is_valid():

			patient = investigation_form.cleaned_data['patient']
			temperature = investigation_form.cleaned_data['temperature']
			heart_rate = investigation_form.cleaned_data['heart_rate']
			symptoms = investigation_form.cleaned_data['symptoms']
			experienced_before = investigation_form.cleaned_data['experienced_before']

			#Save it in the database
			investigation = Investigation(patient=patient, temperature=temperature, heart_rate=heart_rate, symptoms=symptoms, experienced_before=experienced_before)
			investigation.save()
			
			#Redirect to a new url
			return HttpResponseRedirect(reverse('investigation_list') )
	else:
		investigation_form = InvestigationForm()
		
		context = {
			"form": investigation_form
			}

	return render(request, 'new_investigation_template.html', context)

@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def new_diagnosis(request):
	request.session['views_counter'] = request.session['views_counter'] + 1
	#Here we can define the number of photos to upload
	ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=2)
	
	if request.method == "POST":
		formset = ImageFormSet(request.POST, request.FILES, queryset = Images.objects.none())	
		diagnosis_form = DiagnosisForm(request.POST)
		
		if diagnosis_form.is_valid() and formset.is_valid():
	
			diagnosis = diagnosis_form.save(commit=False)
			diagnosis.user = request.user
			diagnosis.save()
			for form in formset.cleaned_data:
				if form:
					image = form['image']
					photo = Images(diagnosis=diagnosis, image=image)
					photo.save()
				messages.success(request, "Success!")
			return HttpResponseRedirect(reverse('diagnosis_list'))

		else:
			print(diagnosis_form.errors, formset.errors)
	else:
		diagnosis_form = DiagnosisForm()
		formset = ImageFormSet(queryset=Images.objects.none())

		context = {
			"diagnosis_form": diagnosis_form,
			"image_form": formset,
			}
	return render(request, 'new_diagnosis_template.html', context)


@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def new_cardiogram(request):
	request.session['views_counter'] = request.session['views_counter'] + 1
	if request.method == "POST":
		cardiogram_form = CardiogramForm(request.POST, request.FILES)
		
		if cardiogram_form.is_valid():
			cardio_file = cardiogram_form.cleaned_data['cardiogram']
			patient = cardiogram_form.cleaned_data['patient']
			cardiogram = Cardiogram(patient=patient, cardiogram=cardio_file)
			cardiogram.save()
			return HttpResponseRedirect(reverse('cardiogram_list'))
			
		else:
			print(cardiogram_form.errors)
			return HttpResponseRedirect(reverse('cardiogram_list'))
	else:
		cardiogram_form = CardiogramForm()

		context = {
			"cardiogram_form": cardiogram_form,
			}
	return render(request, 'new_cardiogram_template.html', context)


@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def patient_detail(request, patient_id = "not_found"):
	request.session['views_counter'] = request.session['views_counter'] + 1
	if request.method == "POST":
		if request.POST.get("delete") is not None:
			patient = Patient.objects.all().get(id=patient_id)
			user = User.objects.get(username = patient.email)
			#Patient.objects.all().get(id=patient_id).delete()
			patient.delete()
			user.delete()
		return HttpResponseRedirect(reverse('patient_list'))
	else:
		patient = Patient.objects.all().get(id=patient_id)
		context = {
			"patient":  patient,
			"diagnosis_list": Diagnosis.objects.all().filter(patient=patient),
			"investigations_list": Investigation.objects.all().filter(patient=patient),
			"cardiogram_list": Cardiogram.objects.all().filter(patient=patient),
			}
		return render(request, 'patient_detail_template.html', context)

@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def diagnosis_detail(request, diagnosis_id = "not_found"):
	request.session['views_counter'] = request.session['views_counter'] + 1
	if request.method == "POST":
		if request.POST.get("delete") is not None:
			Diagnosis.objects.all().get(id=diagnosis_id).delete()
		return HttpResponseRedirect(reverse('diagnosis_list'))
	else:
		diagnosis = Diagnosis.objects.all().get(id=diagnosis_id)
		context = {
			"diagnosis": diagnosis,
			"images": Images.objects.all().filter(diagnosis_id = diagnosis_id),
			}
		return render(request, 'diagnosis_detail_template.html', context)


@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def cardiogram_detail(request, cardiogram_id = "not_found"):

	request.session['views_counter'] = request.session['views_counter'] + 1
	if request.method == "POST":
		if request.POST.get("filter") is not None:
			cardiogram = Cardiogram.objects.all().get(id=cardiogram_id)
			graph_div = time_plot(cardiogram.cardiogram, filter=True)
			context = {
			"cardiogram": cardiogram,
			"graph_div": graph_div,
			}
			return render(request, 'cardiogram_detail_template.html', context)
		elif request.POST.get("find_points") is not None:
			cardiogram = Cardiogram.objects.all().get(id=cardiogram_id)
			graph = points_plot(cardiogram.cardiogram)
			context = {
			"cardiogram": cardiogram,
			"graph_div": graph[0],
			"heartrate": graph[1],
			}
			return render(request, 'cardiogram_detail_template.html', context)
			
		elif request.POST.get("delete") is not None:
			Cardiogram.objects.all().get(id=cardiogram_id).delete()
		return HttpResponseRedirect(reverse('cardiogram_list'))
	else:
		cardiogram = Cardiogram.objects.all().get(id=cardiogram_id)
		graph_div = time_plot(cardiogram.cardiogram)
		context = {
			"cardiogram": cardiogram,
			"graph_div": graph_div,
			}
		return render(request, 'cardiogram_detail_template.html', context)

@permission_required("CardioApp.view_patient", login_url="accounts/login/")
def patient_diagnosis_detail(request, diagnosis_id = "not_found"):
	request.session['views_counter'] = request.session['views_counter'] + 1

	diagnosis = Diagnosis.objects.all().get(id=diagnosis_id)
	context = {
		"diagnosis": diagnosis,
		"images": Images.objects.all().filter(diagnosis_id = diagnosis_id),
		}
	return render(request, 'patient_diagnosis_detail_template.html', context)

@permission_required("CardioApp.view_patient", login_url="accounts/login/")
def patient_cardiogram_detail(request, cardiogram_id = "not_found"):

	request.session['views_counter'] = request.session['views_counter'] + 1
	
	cardiogram = Cardiogram.objects.all().get(id=cardiogram_id)
	graph_div = time_plot(cardiogram.cardiogram, filter=True)
	graph = points_plot(cardiogram.cardiogram)
	context = {
	"cardiogram": cardiogram,
	"graph_div": graph[0],
	"heartrate": graph[1],
	}
	return render(request, 'patient_cardiogram_detail_template.html', context)



@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def investigation_detail(request, investigation_id = "not_found"):
	request.session['views_counter'] = request.session['views_counter'] + 1
	if request.method == "POST":
		if request.POST.get("delete") is not None:
			Investigation.objects.all().get(id=investigation_id).delete()
		return HttpResponseRedirect(reverse('investigation_list'))
	else:

		investigation = Investigation.objects.all().get(id=investigation_id)
		context = {
			"investigation": investigation,
			}
		return render(request, 'investigation_detail_template.html', context)

@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def edit_patient(request,patient_id = "not_found"):
	request.session['views_counter'] = request.session['views_counter'] + 1
	if request.method == "POST":
		patient_form = PatientForm(request.POST)

		if patient_form.is_valid():
			patient = Patient.objects.all().get(id=patient_id)

			#Save it in the database
			patient.name = patient_form.cleaned_data['name']
			patient.middle_name = patient_form.cleaned_data['middle_name']
			patient.last_name = patient_form.cleaned_data['last_name']
			patient.gender = patient_form.cleaned_data['gender']
			patient.birth_date = patient_form.cleaned_data['birth_date']
			patient.nationality = patient_form.cleaned_data['nationality']
			patient.email = patient_form.cleaned_data['email']
			patient.visit_date = patient_form.cleaned_data['visit_date']
			patient.save()

			#Redirect to a new url
			return HttpResponseRedirect(reverse('patient_list'))
	else:
		patient = Patient.objects.all().get(id=patient_id)
		context = {
			"form": PatientForm(instance = patient),
			"patient": patient
			}
		return render(request, 'edit_patient_template.html', context)

@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def edit_investigation(request, investigation_id = "not_found"):
	request.session['views_counter'] = request.session['views_counter'] + 1
	if request.method == "POST":
		investigation_form = InvestigationForm(request.POST)

		if investigation_form.is_valid():

			investigation = Investigation.objects.all().get(id=investigation_id)
			
			investigation.patient = investigation_form.cleaned_data['patient']
			investigation.temperature = investigation_form.cleaned_data['temperature']
			investigation.heart_rate = investigation_form.cleaned_data['heart_rate']
			investigation.symptoms = investigation_form.cleaned_data['symptoms']
			investigation.experienced_before = investigation_form.cleaned_data['experienced_before']
			
			#Save it in the database
			investigation.save()

			#Redirect to a new url
			return HttpResponseRedirect(reverse('investigation_list'))
	else:
		investigation = Investigation.objects.all().get(id=investigation_id)
		context = {
			"form": InvestigationForm(instance = investigation),
			"investigation": investigation
			}
		return render(request, 'edit_investigation_template.html', context)

@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def edit_diagnosis(request, diagnosis_id = "not_found"):
	request.session['views_counter'] = request.session['views_counter'] + 1
	
	#Here we can define the number of photos to upload
	#ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=2)
	
	if request.method == "POST":
		#formset = ImageFormSet(request.POST, request.FILES, queryset = Images.objects.none())	
		diagnosis_form = DiagnosisForm(request.POST)

		#if diagnosis_form.is_valid() and formset.is_valid():
		if diagnosis_form.is_valid():
			diagnosis = Diagnosis.objects.all().get(id=diagnosis_id)
			#Save it in the database	

			diagnosis.patient = diagnosis_form.cleaned_data['patient']
			diagnosis.diagnosis = diagnosis_form.cleaned_data['diagnosis']
			diagnosis.aditional_comments = diagnosis_form.cleaned_data['aditional_comments']
			diagnosis.diagnosis_date = diagnosis_form.cleaned_data['diagnosis_date']

			diagnosis.save()
			return HttpResponseRedirect(reverse('diagnosis_list'))
			
		else:
			#print(diagnosis_form.errors, formset.errors)
			print(diagnosis_form.errors)
			#Redirect to a new url
			return HttpResponseRedirect(reverse('diagnosis_list'))
	else:
		diagnosis = Diagnosis.objects.all().get(id=diagnosis_id)
		#images = Images.objects.all().filter(diagnosis_id=diagnosis_id)
		context = {
			"image_form": ImageForm(),
			"diagnosis_form": DiagnosisForm(instance = diagnosis)
			}
		return render(request, 'edit_diagnosis_template.html', context)


@permission_required("CardioApp.change_patient", login_url="accounts/login/")
def edit_cardiogram(request, cardiogram_id = "not_found"):
	request.session['views_counter'] = request.session['views_counter'] + 1
	
	if request.method == "POST":

		cardiogram_form = CardiogramForm(request.POST, request.FILES)
		
		if cardiogram_form.is_valid():
			#Load the existing cardiogram
			cardiogram = Cardiogram.objects.all().get(id=cardiogram_id)	
			#Update the existing cardiogram
			cardiogram.patient = cardiogram_form.cleaned_data['patient']
			cardiogram.cardiogram = cardiogram_form.cleaned_data['cardiogram']
			cardiogram.save()
			return HttpResponseRedirect(reverse('cardiogram_list'))	
		else:
			print(cardiogram_form.errors)
			return HttpResponseRedirect(reverse('cardiogram_list'))
	else:
		cardiogram = Cardiogram.objects.all().get(id=cardiogram_id)
		#images = Images.objects.all().filter(diagnosis_id=diagnosis_id)
		context = {
			"cardiogram_form": CardiogramForm(instance = cardiogram)
			}
		return render(request, 'edit_cardiogram_template.html', context)