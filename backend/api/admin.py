from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Medecin)
admin.site.register(Administratif)
admin.site.register(Infirmier)
admin.site.register(Laborantin)
admin.site.register(Radiologue)
admin.site.register(Patient)
admin.site.register(DPI)
admin.site.register(Consultation)
admin.site.register(Ordonnance)
admin.site.register(BilanRadiologique)
admin.site.register(BilanBiologique)
admin.site.register(ExamenBiologique)
