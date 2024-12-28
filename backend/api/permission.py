from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied



class DPIListAccessPermission(BasePermission):
    def has_object_permission(self, request):
        user = request.user
        if hasattr(user, 'medecin'):
            return True 
        raise PermissionDenied("Vous n'avez pas la permission pour consulter cette DPI.")


class DPIAccessPermission(BasePermission):
    def has_object_permission(self, request, obj):
        user = request.user
        if hasattr(user, 'patient'):
            if request.method != 'GET' and obj.patient != user.patient:
                raise PermissionDenied("Vous n'avez pas la permission de modifier cette DPI.")
            return True
        elif hasattr(user, 'medecin'):
            medecin = user.medecin
            if obj.medecin_traitant != medecin :
                raise PermissionDenied("Vous n'avez pas la permission pour modifier cette DPI.")
            return True 
        # Sinon, l'accès est refusé
        raise PermissionDenied("Vous n'avez pas la permission pour consulter cette DPI.")
    
def has_permission(request, dpi=None, consultation=None ,bilan=None, examen=None, ordonnance=None):
    user = request.user
    if hasattr(user, 'medecin') and (dpi and user.medecin == dpi.medecin_traitant or 
                                                consultation and user.medecin == consultation.dpi.medecin_traitant or 
                                                    examen and user.medecin == examen.bilan.consultation.dpi.medecin_traitant or
                                                        ordonnance and user.medecin == ordonnance.consultation.dpi.medecin_traitant or 
                                                            bilan and user.medecin == bilan.consultation.dpi.medecin_traitant
                                                        ) :
        return True
    elif hasattr(user, 'patient') and (dpi and user.patient == dpi.patient or
                                                consultation and user.patient == consultation.dpi.patient or
                                                    examen and user.patient == examen.bilan.consultation.dpi.patient or
                                                        ordonnance and user.patient == ordonnance.consultation.dpi.patient or 
                                                            bilan and user.patient == bilan.consultation.dpi.patient
                                                ) and request.method == "GET" :    
        return True
    return False


def is_Infermier(request):
    if hasattr(request.user, 'infirmier') :
        return True
    return False

def is_Laboratory(request):
    if hasattr(request.user, 'laborantin') and request.method != "DELETE" and request.method != "POST" : 
        return True
    return False

def is_Radiologist(request):
    if hasattr(request.user, 'radiologue') and request.method != "DELETE" and request.method != "POST" :
        return True
    return False

def is_Pharmacien(request):
    if hasattr(request.user, 'pharmacien') and request.method != "DELETE" and request.method != "POST" :
        return True
    return False


