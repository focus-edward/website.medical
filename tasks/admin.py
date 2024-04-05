from django.contrib import admin
from .models import Citas, Doctor, PerfilAnalista, PerfilUsuario, Esp, DisponibilidadCita


# Register your models here.



class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Citas, TasksAdmin)
admin.site.register(Doctor)
admin.site.register(PerfilUsuario)
admin.site.register(PerfilAnalista)
admin.site.register(Esp)
admin.site.register(DisponibilidadCita)