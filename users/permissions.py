from rest_framework.permissions import BasePermission

"""
BasePermission – DRF Basisklasse, gibt zwei Methoden vor:

    -> has_permission → prüft auf View-Ebene (darf der User die View überhaupt aufrufen?)
    -> has_object_permission → prüft auf Objekt-Ebene (darf der User dieses Objekt anfassen?)

"""


class IsOwner(BasePermission):
    """
    Prüft ob der eingeloggte User das Objekt selbst ist und die Rechte hat
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user