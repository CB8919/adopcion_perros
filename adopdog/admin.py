from django.contrib import admin
from .models import Perro, User_Adoptante

admin.site.register(Perro) # Para registrar un modelo en el panel de admin
admin.site.register(User_Adoptante)
