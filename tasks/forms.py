from django import forms
from .models import Citas, Doctor, PerfilUsuario, DisponibilidadCita
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateTimeInput


class UserRegistrationForm(UserCreationForm):
    nombres = forms.CharField(max_length=50, required=True)
    apellidos = forms.CharField(max_length=50, required=True)
    edad = forms.IntegerField(required=True)
    direccion = forms.CharField(max_length=255, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('nombres','apellidos','edad', 'direccion')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()  

        perfil_usuario = PerfilUsuario.objects.create(
            user=user,
            nombres=self.cleaned_data['nombres'],
            apellidos=self.cleaned_data['apellidos'],
            edad=self.cleaned_data['edad'],
            direccion=self.cleaned_data['direccion']
        )
        if commit:
            perfil_usuario.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username','password1','password2','nombres', 'apellidos', 'edad', 'direccion']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control custom-select'})


class HoraInput(forms.TextInput):
    input_type = 'time' 

    def __init__(self, attrs=None):
        default_attrs = {'step': '1800'}  
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class CustomTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'pattern': '[\d\.\-]*'})        

class CreateAppointmentForm(forms.ModelForm):
        
    class Meta:
        model = Citas
        fields = ['Especialidad','Doctor','Calendario_de_disponibilidad','Hora','Consultorio','Nombre_del_paciente','Cédula_del_paciente','Teléfono_de_contacto','Síntomas','Información_relevante']
        widgets ={
            'Doctor': forms.Select(attrs={'class':'custom-select'}),
            'Especialidad': forms.Select(attrs={'class':'form-control custom-select'}),
            'Calendario_de_disponibilidad':forms.Select(attrs={'class':'custom-select'}),'Hora':forms.Select(attrs={'class': 'custom-select'}),'Consultorio':forms.Select(attrs={'class': 'custom-select form-control'}),
            'Nombre_del_paciente':forms.TextInput(attrs={'class':'custom-select', 'placeholder':'Indique nombre'}),'Consultorio':forms.Select(attrs={'class':'custom-select'}),
            'Cédula_del_paciente':forms.TextInput(attrs={'class':'custom-select', 'placeholder':'Indique numero de cédula'}),
            'Teléfono_de_contacto':forms.TextInput(attrs={'class':'custom-select', 'placeholder':'Indique numero de contacto'}),
            'Síntomas':forms.TextInput(attrs={'class':'custom-select', 'placeholder':'Mencione síntomas presentes'}),
            'Información_relevante':forms.Textarea(attrs={'class':'custom-select', 'placeholder':'...'}),
            
        }
    def __init__(self, *args, **kwargs):
        super(CreateAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['Especialidad'].empty_label = 'Seleccione una especialidad'
        self.fields['Doctor'].empty_label = 'Debe seleccionar una especialidad'
        self.fields['Hora'].empty_label = 'Debe seleccionar una fecha'                           
        self.fields['Consultorio'].empty_label = 'Debe seleccionar una fecha'             
        self.fields['Doctor'].widget.attrs['disabled'] = 'disabled' 
        self.fields['Consultorio'].widget.attrs['disabled'] = 'disabled'
        self.fields['Hora'].widget.attrs['disabled'] = 'disabled'
        self.fields['Calendario_de_disponibilidad'].widget.attrs['disabled'] = 'disabled'        
        self.fields['Calendario_de_disponibilidad'].empty_label = 'Debe seleccionar un doctor'


        

class GestionDr(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['Especialidad','nombre','activo']
        widgets ={
            'nombre': forms.Select(attrs={'class':'custom-select'}),
            'Especialidad': forms.Select(attrs={'class':'form-control, custom-select'}),'activo':forms.Select(attrs={'class':'form-control, custom-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(GestionDr, self).__init__(*args, **kwargs)
        self.fields['Especialidad'].empty_label = 'Seleccione una especialidad'
        self.fields['activo'].label = 'Estado'
        self.fields['nombre'].label = 'Doctor'
        self.fields['nombre'].empty_label = 'Debe seleccionar una especialidad'



class AddDoctor(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['Especialidad','nombre']
        widgets ={
                'nombre': forms.TextInput(attrs={'class': 'custom-select', 'placeholder': 'Indique el nombre del doctor a ser ingresado al sistema'}),
                'Especialidad': forms.Select(attrs={'class':'form-control, custom-select'})
            }
        
    def __init__(self, *args, **kwargs):
        super(AddDoctor, self).__init__(*args, **kwargs)        
        self.fields['Especialidad'].empty_label = 'Seleccione una especialidad'
        self.fields['nombre'].empty_label = 'Indique el nombre del doctor a ser ingresado al sistema'



class ManageAnalyst(forms.ModelForm):
    class HoraCustomField(forms.TimeField):
        widget = HoraInput

        def to_python(self, value):
            try:
                hora = super().to_python(value)
            except ValidationError:
                raise ValidationError(_("Ingrese una hora válida en formato HH:MM."))

            if hora is not None:
                return hora
            return hora

        def widget_attrs(self, widget):
            attrs = super().widget_attrs(widget)
            attrs.update({'placeholder': 'HH:MM'}) 
            return attrs

    hora = HoraCustomField(initial='08:00')

    class Meta:
        model = DisponibilidadCita
        fields = ['especialidad', 'doctor', 'fecha', 'hora', 'consultorio', 'cupos_disponibles']
        widgets ={
            'especialidad': forms.Select(attrs={'class': 'custom-select'}),
            'doctor': forms.Select(attrs={'class': 'custom-select'}),
            'fecha': forms.DateInput(format='%d-%m-%Y', attrs={'class': 'datepicker custom-select'}),
            'hora': forms.TimeInput(format='%H:%M', attrs={'class': 'custom-select'}), 
            'consultorio': forms.NumberInput(attrs={'class': 'custom-select'}),
            'cupos_disponibles': forms.NumberInput(attrs={'class': 'custom-select'})
        }

    def __init__(self, *args, **kwargs):
        super(ManageAnalyst, self).__init__(*args, **kwargs)
        self.fields['especialidad'].empty_label = 'Seleccione una especialidad'
        self.fields['doctor'].empty_label = 'Debe seleccionar una especialidad'
        self.fields['doctor'].widget.attrs['disabled'] = 'disabled' 


class ChangeStatus(forms.ModelForm):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Suspendida', 'Suspendida'),
        ('Reprogramada', 'Reprogramada'),
        ('Completada', 'Completada'),            
    ]        
    Estado = forms.ChoiceField(choices=ESTADOS)

    class Meta:
        model = Citas
        fields = ['Estado']


    def __init__(self, *args, **kwargs):
        super(ChangeStatus, self).__init__(*args, **kwargs)
        self.fields['Estado'].empty_label = 'Cambiar estado de cita'
        self.fields['Estado'].widget.attrs.update({'class': 'custom-select'})