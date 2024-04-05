from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CreateAppointmentForm, GestionDr, AddDoctor, ManageAnalyst, ChangeStatus
from .models import Citas, Esp, Doctor, PerfilAnalista, PerfilUsuario, DisponibilidadCita
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import *
from django.http import JsonResponse, HttpResponseRedirect
from .forms import UserRegistrationForm


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('citas')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Las contraseñas no coinciden'
            })
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def citas (request):
    user = request.user
    perfil_usuario = PerfilUsuario.objects.filter(user=user).first()
    perfil_analista = PerfilAnalista.objects.filter(user=user).first()
    if perfil_usuario:
        citas = Citas.objects.filter(user=request.user, datecompleted__isnull=True)
        header_text = "Citas Medicas Pendientes"
    elif perfil_analista:
        citas = Citas.objects.filter(datecompleted__isnull=True).order_by('-datecompleted')
        header_text = "Citas Medicas Activas"
    else:
        # El usuario no tiene ningún perfil específico
        citas = None
        header_text = "No tienes permisos para ver las citas activas."

    return render (request, 'citas.html', {'citas':citas,'header_cita':header_text})


@login_required
def historial_citas (request):
    user = request.user
    perfil_usuario = PerfilUsuario.objects.filter(user=user).first()
    perfil_analista = PerfilAnalista.objects.filter(user=user).first()
    if perfil_usuario:
        citas = Citas.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
        header_text = "Historial de Citas Medicas Previas"
    elif perfil_analista:
        citas = Citas.objects.exclude(Estado='Pendiente').order_by('-created')
        header_text = "Historial de Citas Medicas para Analistas"
    else:
        # El usuario no tiene ningún perfil específico
        citas = None
        header_text = "No tienes permisos para ver el historial de citas."

    return render(request, 'citas.html', {'citas': citas, 'header_cita': header_text})


@login_required
def solicitar_citas(request):
    if request.method == 'POST':
        form = CreateAppointmentForm(request.POST)
        if form.is_valid():

            nueva_cita = form.save(commit=False)
            nueva_cita.user = request.user
            nueva_cita.fecha = nueva_cita.Calendario_de_disponibilidad.fecha
            nueva_cita.Hora = nueva_cita.Calendario_de_disponibilidad.hora
            nueva_cita.save()

            disponibilidad = nueva_cita.Calendario_de_disponibilidad
            if disponibilidad.cupos_disponibles > 1:
                disponibilidad.cupos_disponibles -= 1
                disponibilidad.save()
            elif disponibilidad.cupos_disponibles == 1:
                disponibilidad.delete()

            return redirect('citas')

    else:
        form = CreateAppointmentForm()

    return render(request, 'solicitar_citas.html', {
        'form': form,
    })
       

@login_required
def obtener_doctores_por_especialidad(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
        especialidad_id = request.GET.get('especialidad_id')
        if especialidad_id:
            doctores = Doctor.objects.filter(Especialidad_id=especialidad_id)
            data = [{'id': Doctor.id, 'nombre': Doctor.nombre} for Doctor in doctores]
            return JsonResponse(data, safe=False)
    return JsonResponse({}, status=400)

@login_required
def dr_datetime(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
        doctor_id = request.GET.get('doctor_id')
        fecha_id = request.GET.get('fecha_id')
        hora_id =  request.GET.get('hora_id')
        if doctor_id:
            disponibilidades = DisponibilidadCita.objects.filter(doctor_id=doctor_id)
            data = [{'id': DisponibilidadCita.id, 'Calendario_de_disponibilidad': DisponibilidadCita.fecha} for DisponibilidadCita in disponibilidades]
            return JsonResponse(data, safe=False)
        elif fecha_id:
            disponibilidades = DisponibilidadCita.objects.filter(id=fecha_id)
            data = [{'id': disponibilidad.id, 'Hora': disponibilidad.hora} for disponibilidad in disponibilidades]
            return JsonResponse(data, safe=False)  
        elif hora_id:
            disponibilidades = DisponibilidadCita.objects.filter(id=hora_id)
            data = [{'id': disponibilidad.id, 'Consultorio': disponibilidad.consultorio} for disponibilidad in disponibilidades]
            return JsonResponse(data, safe=False)         
              
    return JsonResponse({}, status=400)

@login_required
def doctor_status(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
        doctor_nombre = request.GET.get('doctor_nombre')
        if doctor_nombre:
            try:
                doctor = Doctor.objects.get(nombre=doctor_nombre)
                return JsonResponse({'activo': doctor.activo})
            except Doctor.DoesNotExist:
                return JsonResponse({'error': 'Doctor no encontrado'}, status=404)
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)
         
@login_required         
def citas_detalles(request, citas_id):
    citas = get_object_or_404(Citas, pk=citas_id)
    if request.method == 'POST':
        try:
            form = ChangeStatus(request.POST, instance=citas)
            if form.is_valid():
                citas = form.save(commit=False)
                if citas.Estado in ['Pendiente', 'Reprogramada']:
                    citas.datecompleted = None
                elif citas.Estado in ['Suspendida', 'Completada']:
                    citas.datecompleted = timezone.now()
                citas.save()
                message = 'Estado actualizado exitosamente'
                return render(request, 'citas_detalles.html', {'citas': citas, 'form': form, 'message': message})
            else:
                return render(request,'citas_detalles.html', {'citas': citas, 'form': form, 'error':'Error en los datos ingresados'})
        except ValueError:
            return render(request,'citas_detalles.html', {'citas': citas, 'form': form, 'error':'Error actualizando estado'})                 
    else:
        form = ChangeStatus(instance=citas)
        return render(request, 'citas_detalles.html', {'citas': citas, 'form': form})          


@login_required
def signout(request):
    logout(request)
    return redirect ('home')


def signin (request):
        if request.method == 'GET':
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                })
        else:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'signin.html', {
                    'form': AuthenticationForm,
                    'error':'Username or password is incorrect'
                    })       
            else:
                login(request, user)
                return redirect('citas')
            
    

@login_required
def gestiondr(request):
    form = GestionDr()
    form2 = AddDoctor()
    if request.method == 'GET':
        return render(request, 'gestion.html', {'form': form, 'form2':form2})
    elif request.method == 'POST':
        if 'formone' in request.POST:
            form = GestionDr(request.POST)
            if form.is_valid():
                doctor_nombre = form.cleaned_data['nombre']
                nuevo_estado = form.cleaned_data['activo']
                doctor, creado = Doctor.objects.get_or_create(nombre=doctor_nombre, Especialidad=form.cleaned_data['Especialidad'])
                doctor.activo = nuevo_estado
                doctor.save()
                return render(request, 'gestion.html', {'form': form, 'form2':form2, 'message': 'Estado de doctor actualizado exitosamente'})

            else:
                return render(request, 'gestion.html', {'form': form, 'form2':form2, 'error': 'Por favor revise los datos ingresados'})
        elif 'formtwo' in request.POST:
            form2 = AddDoctor(request.POST)
            if form2.is_valid():
                doctor_nombre = form2.cleaned_data['nombre']
                doctor, creado = Doctor.objects.get_or_create(nombre=doctor_nombre, Especialidad=form2.cleaned_data['Especialidad'])
                doctor.save()
                return render(request, 'gestion.html', {'form': form, 'form2':form2, 'message2': 'Doctor agregado exitosamente al sistema'})

            else:
                return render(request, 'gestion.html', {'form': form, 'form2':form2, 'error2': 'Por favor revise los datos ingresados'})            
        else:
            return HttpResponseRedirect('/gestiondr/')





@login_required
def update_doctor_status(request):
    if request.method == 'POST' and request.is_ajax():
        doctor_id = request.POST.get('doctor_id')
        nuevo_estado = request.POST.get('nuevo_estado')
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            doctor.activo = nuevo_estado
            doctor.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Doctor.DoesNotExist:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required
def manage(request):
    form = ManageAnalyst
    if request.method == 'GET':
        return render(request, 'manage.html', {'form': form})
    else:
        try:
            form = ManageAnalyst(request.POST)
            if form.is_valid():
                new = form.save(commit=False)
                new.save()
                return render(request, 'manage.html',{
                    'form': form,
                    'message': 'Fecha ingresada exitosamente.'
                })  
            else:
                return render(request, 'manage.html',{
                    'form': form,
                    'error': 'Por favor revise los datos ingresados'
                })  
        except ValueError:
            return render(request, 'manage.html',{
                'form': ManageAnalyst(),
                'error': 'Por favor revise los datos ingresados'
            })    

       

def aboutus(request):
    return render(request, 'aboutus.html')

def oursp(request):
    return render(request, 'oursp.html')