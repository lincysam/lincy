"""lincy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from.import views



urlpatterns = [
   # path('home/',include('doctorapp.urls')),
   # path('admin/', admin.site.urls),
    #path('reg/', views.doctor, name = 'doctor'),
    path('patientdetails', views.patientdetails, name = 'patientdetails'),
    path('doctordetails', views.doctordetails, name = 'doctordetails'),
    path('consultation', views.consulting, name = 'consult'),
    path('doctor_availability', views.doctoravail, name = 'consult'),
    path('doctor_schedule', views.doctorschedule, name = 'consult'),
    path('doctor_save', views.availsave, name = 'consult'),
    path('list', views.hosplist, name = 'eachlist'),
    path('doctordelete', views.deletelist, name = 'eachlist'),
    path('newdata', views.patientnewdata, name = 'eachlist'),
    path('doctorupdate', views.updatelist, name = 'eachlist'),
    path('doctor_update', views.availupdate, name = 'update'),
    path('booking', views.booking, name = 'booking'),
    path('patientbooklist', views.pbooklist, name = 'bookinglist'),
    path('patientstate', views.pstate, name = 'patientstate'),
    path('cancelpatient', views.cancelpatient, name = 'patientcancel'),
    path('doctorhome', views.doctorhome, name = 'doctorhome'),
    
]
