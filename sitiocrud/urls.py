"""
URL configuration for sitiocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from tasks import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('citas/', views.citas, name='citas'),
    path('historial_citas/', views.historial_citas, name='historial_citas'),
    path('citas/<int:citas_id>/', views.citas_detalles, name='citas_detalles'),
    path('citas/create/', views.solicitar_citas, name='solicitar_citas'),    
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('aboutus/', views.aboutus, name='aboutus'),  
    path('oursp/', views.oursp, name='oursp'),    
    path('doctorbysp/', views.obtener_doctores_por_especialidad, name='obtener_doctores_por_especialidad'),
    path('gestiondr/', views.gestiondr, name='gestionar_dr'),
    path('update_doctor_status/', views.update_doctor_status, name='update_doctor_status'),
    path('doctor_status/', views.doctor_status, name='doctor_status'),
    path('manage/', views.manage, name='manage'),
    path('dr_datetime/', views.dr_datetime, name='dr_datetime'),
    

]
