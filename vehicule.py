class Vehicule:

    def __init__(self, marque, modele, numero_chassis, nb_places, annee):
        
        if not isinstance(marque, str) or not marque.strip():
            raise ValueError("La marque doit être une chaîne non vide.")
        if not isinstance(modele, str) or not modele.strip():
            raise ValueError("Le modèle doit être une chaîne non vide.")
        
        if not self.chassis_valide(numero_chassis):
            raise ValueError("Numéro de châssis invalide.")
            
        if isinstance(nb_places, bool) or not isinstance(nb_places, int):
            raise TypeError("Le nombre de places doit être un entier.")
        if not (1 <= nb_places <= 80):
            raise ValueError("Le nombre de places est hors plage (1-80).")
            
        if isinstance(annee, bool) or not isinstance(annee, int):
            raise TypeError("L'année doit être un entier.")
        if annee <= 1850:
            raise ValueError("L'année est hors plage (>= 1850).")

        self._marque = marque.strip()
        self._modele = modele.strip()
        self._numero_chassis = numero_chassis
        self._nb_places = nb_places
        self._annee = annee
        self._disponible = True



    @property
    def marque(self):
        return self._marque

    @property
    def modele(self):
        return self._modele

    @property
    def numero_chassis(self):
        return self._numero_chassis

    @property
    def nb_places(self):
        return self._nb_places

    @property
    def annee(self):
        return self._annee

    @property
    def disponible(self):
        return self._disponible



    @staticmethod
    def chassis_valide(chaine):
        if not isinstance(chaine, str):
            return False
        return len(chaine) == 17 and chaine.isalnum()

    

    @classmethod
    def depuis_csv(cls, ligne):
        parties = ligne.strip().split(";")
        
        
        if cls.__name__ in ("VoitureElectrique", "Camion"):
            expected = 6
        else:
            expected = 5

        if len(parties) != expected:
            raise ValueError("Nombre de champs incorrect dans la ligne CSV.")

        if cls.__name__ == "VoitureElectrique":
            return cls(parties[0], parties[1], parties[2], int(parties[3]), int(parties[4]), int(parties[5]))
        elif cls.__name__ == "Camion":
            return cls(parties[0], parties[1], parties[2], int(parties[3]), int(parties[4]), float(parties[5]))
        else:
            return cls(parties[0], parties[1], parties[2], int(parties[3]), int(parties[4]))

    

    def to_dict(self):
        return {
            "type": "Vehicule",
            "marque": self.marque,
            "modele": self.modele,
            "numero_chassis": self.numero_chassis,
            "nb_places": self.nb_places,
            "annee": self.annee,
            "disponible": self.disponible
        }

    @classmethod
    def from_dict(cls, donnees):
        v = cls(
            donnees["marque"],
            donnees["modele"],
            donnees["numero_chassis"],
            donnees["nb_places"],
            donnees["annee"]
        )
        cls._restaurer_disponibilite(v, donnees)
        return v

    @staticmethod
    def _restaurer_disponibilite(vehicule, donnees):
        if not donnees.get("disponible", True):
            vehicule.louer()



    def louer(self):
        if not self._disponible:
            raise ValueError("Le véhicule est déjà loué.")
        self._disponible = False

    def restituer(self):
        if self._disponible:
            raise ValueError("Le véhicule est déjà disponible.")
        self._disponible = True

    def fiche_resume(self):
        return f"{self.nb_places} places"

    

    def __str__(self):
        etat = "disponible" if self.disponible else "loué"
        return f"{self.marque} {self.modele} ({self.numero_chassis}) - {etat}"

    def __repr__(self):
        return (f"Vehicule({self.marque!r}, {self.modele!r}, {self.numero_chassis!r}, "
                f"{self.nb_places!r}, {self.annee!r})")

    

    def __eq__(self, autre):
        if not isinstance(autre, Vehicule):
            return NotImplemented
        return self.numero_chassis == autre.numero_chassis

    def __hash__(self):
        return hash(self.numero_chassis)


class VoitureElectrique(Vehicule):
    

    def __init__(self, marque, modele, numero_chassis, nb_places, annee, autonomie_km):
        if isinstance(autonomie_km, bool) or not isinstance(autonomie_km, (int, float)):
            raise TypeError("L'autonomie doit être un entier.")
        if autonomie_km <= 0:
            raise ValueError("L'autonomie doit être strictement positive.")
            
        super().__init__(marque, modele, numero_chassis, nb_places, annee)
        self._autonomie_km = int(autonomie_km)

    @property
    def autonomie_km(self):
        return self._autonomie_km

    def to_dict(self):
        d = super().to_dict()
        d["type"] = "VoitureElectrique"
        d["autonomie_km"] = self.autonomie_km
        return d

    @classmethod
    def from_dict(cls, donnees):
        ve = cls(
            donnees["marque"],
            donnees["modele"],
            donnees["numero_chassis"],
            donnees["nb_places"],
            donnees["annee"],
            donnees["autonomie_km"]
        )
        cls._restaurer_disponibilite(ve, donnees)
        return ve

    def fiche_resume(self):
        return f"{super().fiche_resume()} [électrique, {self.autonomie_km} km]"

    def __repr__(self):
        return (f"VoitureElectrique({self.marque!r}, {self.modele!r}, {self.numero_chassis!r}, "
                f"{self.nb_places!r}, {self.annee!r}, {self.autonomie_km!r})")


class Camion(Vehicule):
    

    def __init__(self, marque, modele, numero_chassis, nb_places, annee, charge_utile_t):
        if isinstance(charge_utile_t, bool) or not isinstance(charge_utile_t, (int, float)):
            raise TypeError("La charge utile doit être un nombre.")
        if charge_utile_t <= 0:
            raise ValueError("La charge utile doit être strictement positive.")
            
        super().__init__(marque, modele, numero_chassis, nb_places, annee)
        self._charge_utile_t = float(charge_utile_t)

    @property
    def charge_utile_t(self):
        return self._charge_utile_t

    def to_dict(self):
        d = super().to_dict()
        d["type"] = "Camion"
        d["charge_utile_t"] = self.charge_utile_t
        return d

    @classmethod
    def from_dict(cls, donnees):
        c = cls(
            donnees["marque"],
            donnees["modele"],
            donnees["numero_chassis"],
            donnees["nb_places"],
            donnees["annee"],
            donnees["charge_utile_t"]
        )
        cls._restaurer_disponibilite(c, donnees)
        return c

    def fiche_resume(self):
        return f"{self.charge_utile_t} t de charge"

    def __repr__(self):
        return (f"Camion({self.marque!r}, {self.modele!r}, {self.numero_chassis!r}, "
                f"{self.nb_places!r}, {self.annee!r}, {self.charge_utile_t!r})")