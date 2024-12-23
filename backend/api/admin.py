from django.contrib import admin

from .models import Patient, DPI, Consultation, BilanBiologique, ExamenBiologique , Medecin , Infirmier , Laborantin , Radiologue , Administratif , BilanRadiologique

# Register your models here.
admin.site.register(Medecin)
admin.site.register(Patient)
admin.site.register(DPI)
admin.site.register(Consultation)
admin.site.register(BilanRadiologique)
admin.site.register(BilanBiologique)
admin.site.register(ExamenBiologique)
