
from vehicule import Vehicule


class Flotte:
    def __init__(self):
        self._vehicules = []

    def _est_vehicule(self, obj):
        """Vérifie duck typing sans isinstance."""
        return (hasattr(obj, 'marque') and
                hasattr(obj, 'modele') and
                hasattr(obj, 'numero_chassis') and
                hasattr(obj, 'disponible'))

    def ajouter(self, vehicule):
        if not self._est_vehicule(vehicule):
            raise TypeError(f"Un Vehicule est attendu, reçu : {type(vehicule).__name__}")
        if vehicule in self:
            raise ValueError(f"Véhicule déjà présent : {vehicule.numero_chassis}")
        self._vehicules.append(vehicule)

    def retirer(self, vehicule):
        if not self._est_vehicule(vehicule):
            raise TypeError(f"Un Vehicule est attendu, reçu : {type(vehicule).__name__}")
        if vehicule not in self:
            raise KeyError(f"Véhicule introuvable : {vehicule.numero_chassis}")
        self._vehicules.remove(vehicule)

    def __len__(self):
        return len(self._vehicules)

    def __contains__(self, item):
        if self._est_vehicule(item):
            return any(v == item for v in self._vehicules)
        if isinstance(item, str):
            return any(v.numero_chassis == item for v in self._vehicules)
        return False

    def __iter__(self):
        return iter(self._vehicules)

    def trouver_par_chassis(self, numero_chassis):
        for v in self._vehicules:
            if v.numero_chassis == numero_chassis:
                return v
        raise KeyError(f"Véhicule introuvable : {numero_chassis}")

    def vehicules_disponibles(self):
        return [v for v in self._vehicules if v.disponible]

    @property
    def nombre_disponibles(self):
        return len(self.vehicules_disponibles())

    def __repr__(self):
        return f"Flotte({self._vehicules!r})"