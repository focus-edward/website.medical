from django.db import models
from django.contrib.auth.models import User
from datetime import time



class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.TextField(max_length=50, null=True)
    apellidos = models.TextField(max_length=50, null=True)
    edad = models.IntegerField(null=True)
    direccion = models.CharField(max_length=254,null=True)

    def __str__(self):
        return self.user.username  
    
    def is_usuario(self):
        return True

    def is_analista(self):
        return False


class PerfilAnalista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username     

    def is_usuario(self):
        return False

    def is_analista(self):
        return True


 
class Paciente(models.Model):
    user = models.ForeignKey(PerfilUsuario, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=100)
    cedula = models.TextField(max_length=11)
    edad = models.IntegerField(null=True)


class Esp(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    


class Doctor(models.Model):
    nombre = models.CharField(max_length=100)
    Especialidad = models.ForeignKey(Esp, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    

    
class DisponibilidadCita(models.Model):
    fecha = models.CharField(max_length=12)
    hora = models.TimeField()
    cupos_disponibles = models.PositiveIntegerField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Esp, on_delete=models.SET_NULL, null=True)    
    consultorio = models.IntegerField(null=True)

def __str__(self):
    return str(self.fecha)   


class Citas(models.Model):
    Especialidad = models.ForeignKey(Esp, on_delete=models.SET_NULL, null=True)
    Doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    Calendario_de_disponibilidad = models.ForeignKey(DisponibilidadCita, on_delete=models.SET_NULL, null=True)
    fecha = models.CharField(max_length=12, default='01/01/2024')
    Hora = models.CharField(max_length=12)
    Consultorio = models.CharField(max_length=3)
    Estado = models.TextField(default='Pendiente')
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)
    Nombre_del_paciente = models.TextField(max_length=100)
    Cédula_del_paciente = models.TextField(max_length=11)
    edad = models.IntegerField(null=True)
    Teléfono_de_contacto = models.TextField(max_length=20)
    Síntomas = models.TextField(max_length=100)
    Información_relevante = models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Cita de {self.Nombre_del_paciente} con Dr. {self.Doctor.nombre}"
    


    

