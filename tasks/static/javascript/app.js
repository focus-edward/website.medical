$(document).ready(function(){
    $('#id_Especialidad').change(function(){
        var especialidad_id = $(this).val();
        if (especialidad_id) {
            $.ajax({
                url: '/doctorbysp/',
                data: {
                    'especialidad_id': especialidad_id
                },
                dataType: 'json',
                success: function(data){
                    $('#id_Doctor').empty().append($('<option>', {
                        value: '',
                        text: 'Seleccione un doctor'
                    }));
                    $.each(data, function(index, doctor){
                        $('#id_Doctor').append($('<option>', {
                            value: doctor.id,
                            text: doctor.nombre
                        }));
                    });
                    $('#id_Doctor').removeAttr('disabled');  // Habilitar el campo Doctor
                }
            });
        } else {
            $('#id_Doctor').empty().attr('disabled', 'disabled');  // Limpiar y deshabilitar el campo Doctor si no se selecciona una especialidad
        }
    });

    $('#id_Doctor').change(function(){
        var doctor_id = $(this).val();
        if (doctor_id) {
            $.ajax({
                url: '/dr_datetime/',
                data: {
                    'doctor_id': doctor_id
                },
                dataType: 'json',
                success: function(data){
                    if (data.length === 0) {
                        $('#id_Calendario_de_disponibilidad').empty().append($('<option>', {
                            value: '',
                            text: 'En este momento este doctor no tiene fechas disponibles'
                        })).attr('disabled', 'disabled');
                    } else {
                        $('#id_Calendario_de_disponibilidad').empty().append($('<option>', {
                            value: '',
                            text: 'Seleccione una fecha'
                        }));
                        $.each(data, function(index, disponibilidad){
                            $('#id_Calendario_de_disponibilidad').append($('<option>', {
                                value: disponibilidad.id,
                                text: disponibilidad.Calendario_de_disponibilidad
                            }));
                        });
                        $('#id_Calendario_de_disponibilidad').removeAttr('disabled');
                    }
                }
            });
        } else {
            $('#id_Calendario_de_disponibilidad').empty().attr('disabled', 'disabled');  
        }
    });

    $('#id_Calendario_de_disponibilidad').change(function(){
        var fecha_id = $(this).val();
        if (fecha_id) {
            $.ajax({
                url: '/dr_datetime/',
                data: {
                    'fecha_id': fecha_id
                },
                dataType: 'json',
                success: function(data){
                    $('#id_Hora').empty().append($('<option>', {
                        value: '',
                        text: 'Seleccione una hora disponible'
                    }));
                    $.each(data, function(index, disponibilidad){
                        $('#id_Hora').append($('<option>', {
                            value: disponibilidad.id,
                            text: disponibilidad.Hora
                        }));
                    });
                    $('#id_Hora').removeAttr('disabled'); 
                }
            });
        } else {
            $('#id_Hora').empty().attr('disabled', 'disabled');  
        }
    });

    $('#id_Hora').change(function(){
        var hora_id = $(this).val();
        if (hora_id) {
            $.ajax({
                url: '/dr_datetime/',
                data: {
                    'hora_id': hora_id
                },
                dataType: 'json',
                success: function(data){
                    $('#id_Consultorio').empty().append($('<option>', {
                        value: '',
                        text: 'Seleccione el consultorio'
                    }));                    
                    $.each(data, function(index, disponibilidad){
                        $('#id_Consultorio').append($('<option>', {
                            value: disponibilidad.id,
                            text: disponibilidad.Consultorio
                        }));
                    });
                    $('#id_Consultorio').removeAttr('disabled'); 
                }
            });
        } else {
            $('#id_Consultorio').empty().attr('disabled', 'disabled');  
        }
    });
});

$(document).ready(function(){
    // Evento change para la especialidad
    $('#id_Especialidad').change(function(){
        var especialidad_id = $(this).val();
        if (especialidad_id) {
            $.ajax({
                url: '/doctorbysp/',  
                data: {
                    'especialidad_id': especialidad_id
                },
                dataType: 'json',
                success: function(data){
                    $('#id_nombre').empty().append($('<option>', {
                        value: '',
                        text: 'Seleccione un doctor'
                    }));
                    $.each(data, function(index, doctor){
                        $('#id_nombre').append($('<option>', {
                            value: doctor.nombre, 
                            text: doctor.nombre  
                        }));
                    });
                    $('#id_nombre').removeAttr('disabled');  // Habilitar el campo Doctor
                }
            });
            // Limpiar y deshabilitar el campo de activo cuando se cambia la especialidad
            $('#id_activo').empty().attr('disabled', 'disabled');
        } else {
            $('#id_nombre').empty().attr('disabled', 'disabled');  // Limpiar y deshabilitar el campo Doctor si no se selecciona una especialidad
            $('#id_activo').empty().attr('disabled', 'disabled'); // Limpiar y deshabilitar el campo "activo" si no hay doctor seleccionado
        }
    });

    // Evento change para el nombre del doctor
    $('#id_nombre').change(function(){
        var doctor_nombre = $(this).val();
        if (doctor_nombre) {
            $.ajax({
                url: '/doctor_status/',
                data: {
                    'doctor_nombre': $('#id_nombre').val() 
                },
                dataType: 'json',
                success: function(data){
                    $('#id_activo').empty(); // Limpiar las opciones anteriores
                    // Agregar opciones para el estado activo e inactivo
                    $('#id_activo').append($('<option>', {
                        value: '1',
                        text: 'Activo' 
                    }));
                    $('#id_activo').append($('<option>', {
                        value: '0',
                        text: 'Inactivo' 
                    }));
                    $('#id_activo').val(data.activo ? '1' : '0');  // Seleccionar el estado activo o inactivo según los datos recibidos
                    $('#id_activo').removeAttr('disabled'); // Habilitar el campo "activo"
                }
            });
        } else {
            $('#id_activo').empty().attr('disabled', 'disabled'); // Limpiar y deshabilitar el campo "activo" si no hay doctor seleccionado
        }
    });
    $('#id_activo').change(function(){
        var doctor_id = $('#id_nombre').val();  // Obtener el ID del doctor seleccionado
        var estado = $(this).val();  // Obtener el estado seleccionado
        // Realizar la solicitud AJAX para actualizar el estado del doctor
        var csrftoken = $('[name=csrfmiddlewaretoken]').val();
        $('#id_activo').change(function(){
            var doctor_id = $('#id_nombre').val();  // Obtener el ID del doctor seleccionado
            var estado = $(this).val();  // Obtener el estado seleccionado
            // Realizar la solicitud AJAX para actualizar el estado del doctor
            var csrftoken = $('[name=csrfmiddlewaretoken]').val();
            $.ajax({
                url: '/update_doctor_status/',
                type: 'POST',
                data: {
                    'doctor_id': doctor_id,
                    'nuevo_estado': estado,
                    'csrfmiddlewaretoken': csrftoken
                },
                dataType: 'json',
                success: function(data){
                    showMessage('Proceso completado exitosamente.', 'success');
                },
                error: function(xhr, errmsg, err){
                    alert('¡Ocurrió un error al actualizar el estado del doctor!');
                }
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('myForm');
    var cedulaField = form.querySelector('input[name="Cédula_del_paciente"]');
    var telefonoField = form.querySelector('input[name="Teléfono_de_contacto"]');
    var nonNumericsPattern = /[^0-9.\-]/;  // Expresión regular para caracteres no numéricos

    cedulaField.addEventListener('input', function (event) {
        var value = event.target.value;
        if (nonNumericsPattern.test(value)) {
            event.target.value = value.replace(nonNumericsPattern, ''); // Elimina caracteres no numéricos
        }
        if (value.length > 10) {
            event.target.value = value.slice(0, 10); // Limita la longitud máxima a 10 caracteres
        }
    });

    telefonoField.addEventListener('input', function (event) {
        var value = event.target.value;
        if (nonNumericsPattern.test(value)) {
            event.target.value = value.replace(nonNumericsPattern, ''); // Elimina caracteres no numéricos
        }
        if (value.length > 30) {
            event.target.value = value.slice(0, 30); // Limita la longitud máxima a 30 caracteres
        }
    });
});

$(document).ready(function() {
    $('.datepicker').datepicker({
        dateFormat: 'dd/mm/yy',
        altField: '#id_fecha'  
    });
});

