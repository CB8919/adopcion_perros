from django.shortcuts import render, redirect  # render(para mostrar plantillas HTML), redirect(para redirigir a otra vista)
from django.contrib import messages  # para mostrar mensajes al usuario
from django.contrib.auth import logout  # para cerrar sesión aunque no se uza en el código
from .models import Perro  # se importa el objeto perro que está en la BD
from .services import Sistem_Adopcion  # es la clase que contiene la lógica

sistema = Sistem_Adopcion()

# Vista a la página principal
def vista_index(request):
    return render(request, "adopdog/index.html")

# Vista para cargar un perro
def vista_agregar_perro(request):
    if request.method == "POST":
        datos_perro = {
            "nombre": request.POST.get("nombre"),
            "raza": request.POST.get("raza"),
            "edad": request.POST.get("edad"),
            "tamano": request.POST.get("tamano"),
            "peso": request.POST.get("peso"),
            "salud": request.POST.get("salud"),
            "vacunado": request.POST.get("vacunado") == "on",
            "temperamento": request.POST.get("temperamento"),
            "estado_de_adopcion": "disponible",
        }

        sistema.cargar_perro(datos_perro)  # Llamamos al método del sistema para guardar al perro
        messages.success(request, "Perro registrado correctamente", extra_tags="agregar_perro")
        return redirect("vista_index")

    return render(request, "adopdog/index.html")

# Vista para eliminar un perro
def vista_eliminar_perro(request):
    if request.method == "POST":
        id_perro = request.POST.get("id")

        if sistema.eliminar_perro(id_perro):
            messages.success(request, "Perro eliminado correctamente.", extra_tags="eliminar_perro")
        else:
            messages.error(request, "No se encontró un perro con ese ID.", extra_tags="eliminar_perro")

        return redirect("vista_index")

    return redirect("vista_index")

# Vista para registrar un usuario
def vista_registrar_user(request):
    if request.method == "POST":
        datos_usuario = {
            "nombre": request.POST.get("nombre"),
            "dni": request.POST.get("dni"),
            "email": request.POST.get("email"),
        }
        sistema.registrar_user(datos_usuario)
        messages.success(request, "Usuario registrado con éxito", extra_tags="registrar_user")
        return redirect("vista_index")

    return render(request, "adopdog/index.html")

# Vista para postular un perro
def vista_postular_perro(request):
    if request.method == "POST":
        id_perro = request.POST.get("id_perro")
        nombre_postulante = request.POST.get("nombre")
        email_postulante = request.POST.get("email")

        if sistema.postular_perro(id_perro, nombre_postulante, email_postulante):
            messages.success(request, "Postulación enviada con éxito.", extra_tags="postular_perro")
        else:
            messages.error(request, "No se pudo postular, perro no encontrado.", extra_tags="postular_perro")

        return redirect("vista_listado_perros")

    return render(request, "adopdog/index.html")

# Vista para confirmar una adopción
def vista_confirmar_adopcion(request):
    if request.method == "POST":
        id_perro = request.POST.get("id_perro")

        try:
            perro = Perro.objects.get(id=id_perro)
            perro.adoptado = True
            perro.save()

            if sistema.confirmar_adop(id_perro):
                messages.success(request, "Adopción confirmada.", extra_tags="confirmar_adopcion")
            else:
                messages.error(request, "No se encontró un perro con ese ID.", extra_tags="confirmar_adopcion")
        except Perro.DoesNotExist:
            messages.error(request, "No se encontró un perro con ese ID.", extra_tags="confirmar_adopcion")

        return redirect("vista_index")

    return redirect("vista_index")

# Vista para preferencia de perros
def vista_preferencia_perros(request):
    filtros = {}  # Diccionario para los filtros

    # Tomo los valores del formulario GET
    raza = request.GET.get("raza")
    edad = request.GET.get("edad")
    tamano = request.GET.get("tamano")
    salud = request.GET.get("salud")
    vacunado = request.GET.get("vacunado")
    temperamento = request.GET.get("temperamento")

    # Se agrega al diccionario solo si se seleccionó una opción
    if raza:
        filtros["raza"] = raza
    if edad:
        filtros["edad"] = edad
    if tamano:
        filtros["tamano"] = tamano
    if salud:
        filtros["salud"] = salud
    if vacunado is not None:
        filtros["vacunado"] = True
    if temperamento:
        filtros["temperamento"] = temperamento

    filtros["estado_de_adopcion"] = "disponible"

    perros_filtrados = Perro.objects.filter(**filtros)

    return render(request, "adopdog/preferencia_perros.html", {
        "perros": perros_filtrados
    })

# Vista listado de perros
def vista_listado_perros(request):
    if request.method == "POST":
        perros = Perro.objects.all()
        return render(request, "adopdog/listado_perros.html", {"perros": perros})

    return render(request, "adopdog/index.html")

# Vista para salir
def vista_salir(request):
    logout(request)
    return redirect("vista_index")






# Create your views here.
