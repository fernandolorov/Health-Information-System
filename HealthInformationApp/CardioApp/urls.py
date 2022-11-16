from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
#from CardioApp.views import PatientDetail
#URL path / Corresponding view / Name used to refer to the view

urlpatterns = [ path('homepage', views.homepage, name='homepage'),
				path('patient/diagnosis/<str:diagnosis_id>', views.patient_diagnosis_detail, name = 'patient_diagnosis_detail'),
				path('patient/cardiogram/<str:cardiogram_id>', views.patient_cardiogram_detail, name = 'patient_cardiogram_detail'),
				path('patients', views.patient_list, name='patient_list'),
				path('newpatient', views.new_patient, name='newpatient'),
				path('patients/<str:patient_id>', views.patient_detail, name = 'patient_detail'),
				path('patients/<str:patient_id>/edit', views.edit_patient, name = 'edit_patient'),
				path('investigations', views.investigation_list, name='investigation_list'),
				path('newinvestigation', views.new_investigation, name='newinvestigation'),
				path('investigation/<str:investigation_id>', views.investigation_detail, name = 'investigation_detail'),
				path('investigation/<str:investigation_id>/edit', views.edit_investigation, name = 'edit_investigation'),
				path('diagnosis', views.diagnosis_list, name='diagnosis_list'),
				path('newdiagnosis', views.new_diagnosis, name='newdiagnosis'),
				path('diagnosis/<str:diagnosis_id>', views.diagnosis_detail, name = 'diagnosis_detail'),
				path('diagnosis/<str:diagnosis_id>/edit', views.edit_diagnosis, name = 'edit_diagnosis'),
				path('cardiogram', views.cardiogram_list, name='cardiogram_list'),
				path('newcardiogram', views.new_cardiogram, name='newcardiogram'),
				path('cardiogram/<str:cardiogram_id>', views.cardiogram_detail, name = 'cardiogram_detail'),
				path('cardiogram/<str:cardiogram_id>/edit', views.edit_cardiogram, name = 'edit_cardiogram'),
				path('accounts/', include('django.contrib.auth.urls')),
				] 

#path('login/', views.custom_login, name = 'custom_login'),
