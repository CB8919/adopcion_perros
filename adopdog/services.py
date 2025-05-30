from .models import Perro, User_Adoptante
from django.db.models import Q

class Sistem_Adopcion:
    def __init__(self):
        
        self.list_usuario = []
        self.list_perro = []
        self.list_perro_adoptados = []
    
    # Método para agregar un nuevo perro a la lista de adopción
    def cargar_perro(self, datos_perro):
        
        perro = Perro(**datos_perro)
        perro.save()
        #self.list_perro.append(perro)
        return perro

    # Método para eliminar un perro de la lista o ponerlo como adoptado
    def eliminar_perro(self, id_perro):
        
        try:

            perro = Perro.objects.get(id = id_perro) #.objects.get()Busca un Obejeto de la tabla perro en donde id sea = id_perro
            perro.delete()
            print(f"Se eliminó el perro ID: {id_perro}")
            return True
        except Perro.DoesNotExist:
            print(f"No se encontró ese ID: {id_perro}")
            return False 

    # Método para registrar un usuario en una base de datos
    def registrar_user(self, datos_usuario):
        
        user = User_Adoptante(**datos_usuario)
        user.save()
        return user

    # Método para cambiar el estado de un perro a adoptado
    def confirmar_adop(self, id_perro):
        
        try:
            perro = Perro.objects.get(id = id_perro, estado_de_adopcion = "disponible")
            perro.estado_de_adopcion = "adoptado"
            perro.save()
            print(f"El perro ID: {id_perro} fue adoptado con éxito.")
            return True
        except Perro.DoesNotExist:
            print(f"No se encontró ese ID: {id_perro}")
            return False
    def postular_perro(self, id_perro, nombre_postulante, email_postulante):
        
        for perro in self.list_perro:
            if perro.id == int(id_perro):
                postulacion = {
                    "id_perro": perro.id,
                    "nombre_postulante": nombre_postulante,
                    "email_postulante": email_postulante
                }
                self.list_postulaciones.append(postulacion)
                print(f"{nombre_postulante} postuló para el perro ID {id_perro}.")
                return True
        print(f"No se encontró el perro con ID: {id_perro} para postular.")
        return False

    # Método para filtra preferncias del usuario a la hora de adoptar
    def preferencia_perro(self, opcion, valor):
        
        filtrado = {opcion: valor, "estado_de_adopcion": "disponible"}
        perros_filtrados = Perro.objects.filter(**filtrado) 
        
        return perros_filtrados

    # Método que retorna o muestra una lista de perros disponibles con sus estados
    def listado_perro(self):

        perros = Perro.objects.all()
        if not perros:
            print("No hay perros registrados hasta el momento")
            return []
    
        for i, perro in enumerate(perros, 1):
            print(
                f"{i}. ID: {perro.id}\nNombre: {perro.nombre}\nRaza: {perro.raza}\nEdad: {perro.edad}"
                f"\nTamaño: {perro.tamano}\nPeso: {perro.peso}\nSalud: {perro.salud}\nVacunado: {perro.vacunado}"
                f"\nEstado de adopción: {perro.estado_de_adopcion}\nTemperamento: {perro.temperamento}\n"
            )
        return perros
