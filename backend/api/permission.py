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
