from django.db import models

class Perro(models.Model): # Hereda de models.Model, es para crear una tabla de BD de esta clase
    
    ESTADO_CHOICES = [ # Esos son los valores, son los parametros que tiene estado_adopción. (Lista de tuplas)
        ('disponible', 'Disponible'),# diponible, reservado y adoptado se guarda en la BD y son los únicos valores posibles
        ('reservado', 'Reservado'),# 
        ('adoptado', 'Adoptado'),
    ]
    nombre = models.CharField(max_length = 100)
    raza = models.CharField(max_length = 100)
    edad = models.CharField(max_length = 50) # cachorro, joven, adulto
    tamano = models.CharField(max_length = 50)  # Grande, mediano,pequeño
    peso = models.CharField(max_length = 100)
    salud = models.CharField(max_length = 200)
    vacunado = models.BooleanField(default = False ) # Por defecto False
    estado_de_adopcion = models.CharField(max_length = 10, choices = ESTADO_CHOICES, default = 'disponible') # Le pasamos la tupla y por default la dejamos en disponible
    temperamento = models.CharField(max_length = 200)
        

        # Método para cambiar el estado del perro a disponible, reservado o adoptado
    def cambiar_estado(self, nuevo_estado):
        
        if nuevo_estado in dict(self.ESTADO_CHOICES): # Si el nuevo_estado esta dentro de los parametros del choices lo guarda
            self.estado_de_adopcion = nuevo_estado
            self.save() # Para guardar el cambio en la BD
            return f"Nuevo estado: {self.estado_de_adopcion}"
        else:
            return("Estado no valido")

        # Métedo para mostrar la info del perro
    def mostrar_info(self):
        return (f"ID: {self.id}\nNombre: {self.nombre}\nRaza: {self.raza}\nEdad: {self.edad}\nTamaño: {self.tamano}\nPeso: {self.peso}kg\nSalud: {self.salud}\nVacunado: {self.vacunado}\nEstado: {self.estado_de_adopcion}\nTemperamento: {self.temperamento}")
    
    def __str__(self): # Para que muestre el objeto en formato de texto
        return f"{self.nombre}, {self.raza} - {self.estado_de_adopcion}"
    


# CLASE USUARIO_ADOPTANTE

class User_Adoptante(models.Model):
    
    nombre = models.CharField(max_length = 100)
    dni = models.CharField(max_length = 20, unique = True) # unique es para que sea único y no se repita
    email = models.EmailField(unique = True)

# Preferencia {Raza, edad(cachorro/joven/adulto), tamaño}
    preferencia_raza = models.CharField(max_length = 50, blank = True, null = True)
    preferencia_edad = models.CharField(max_length = 10, choices = [('cachorro', 'Cachorro'), ('joven', 'Joven'), ('adulto', 'Adulto')], blank = True, null = True)
    preferencia_tamano = models.CharField(max_length = 10, choices = [('pequeño', 'Pequeño'), ('mediano', 'Mediano'), ('grande', 'Grande')], blank = True, null = True)

    histo_adop = models.ManyToManyField('Perro', blank = True) # Relación de muchos a muchos

    def __str__(self):
        return f"{self.nombre}, {self.dni}"
        
        # Método para registrar a un usuario
    def registrarse(self):
        return f"Usuario registrado: {self.nombre}\nDNI: {self.dni}\nEmail: {self.email}\nPreferencias: {self.obtener_preferncias()}\nHistorial de adopción: {self.historial()}"
    
        # Método para modificar datos
    def modificar_datos(self, nuevo_nombre = None, nuevo_email = None, nueva_preferencia_raza = None, nueva_preferencia_edad = None, nueva_preferencia_tamano = None): #None para omitir si algún dato no se quiere modificar
        if nuevo_nombre:
            self.nombre = nuevo_nombre
        if nuevo_email:
            self.email = nuevo_email
        if nueva_preferencia_raza:    
            self.preferencia_raza = nueva_preferencia_raza
        if nueva_preferencia_edad:
            self.preferencia_edad = nueva_preferencia_edad
        if nueva_preferencia_tamano:
            self.preferencia_tamano = nueva_preferencia_tamano
        self.save()

        return f"Datos modificados:\nNombre: {self.nombre}\nDNI: {self.dni}\nEmail: {self.email}\nPreferencias: {self.obtener_preferencias()}"
        # Método para borrar los datos
    def borrar_datos(self):
        self.nombre = ""
        self.dni = ""
        self.email = ""
        self.preferencia_raza = ""
        self.preferencia_edad = ""
        self.preferencia_tamano = ""
        self.histo_adop.clear() # claer para limpiar el historial
        self.save()

        return f"Los datos fueron borrados correctamente"
        

        # Método para mostrar su historial de adopción si lo tiene, o simplemente mostrar todos los datos del usuario
    def historial(self):
        if not self.histo_adop.exists(): # Devuelve True si al menos hay un registro en la consulta y False si esta vacio
            return "No hay adopciones realizadas"
        else:
            historial = ""
            for perro in self.histo_adop.all(): # Me devuelve una QuerySet(Lista de Obetos) con los registros 
                historial += f"{perro.nombre} ID: {perro.id}\n"

            return f"Historial de adopciones:\n{historial} "
        
    def obtener_preferencias(self):
        return f"Raza: {self.preferencia_raza}, Edad: {self.preferencia_edad}, Tamaño: {self.preferencia_tamano}"
        
    def mostrar_user(self):
        print(f"Nombre: {self.nombre}\nDNI: {self.dni}\nEmail: {self.email}\nPreferencias: {self.obtener_preferencias()}\nHistorial de adopción: {self.historial()}")