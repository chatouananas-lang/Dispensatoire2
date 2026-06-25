import json

from vehicule import Vehicule, VoitureElectrique, Camion


_FABRIQUES = {
    "Vehicule": Vehicule,
    "VoitureElectrique": VoitureElectrique,
    "Camion": Camion,
}


def vehicule_depuis_dict(donnees):
    type_nom = donnees.get("type")
    if type_nom is None:
        raise ValueError("Champ 'type' absent du dictionnaire.")
    if type_nom not in _FABRIQUES:
        raise ValueError(f"Type de véhicule inconnu : {type_nom!r}")
    return _FABRIQUES[type_nom].from_dict(donnees)


def sauvegarder_flotte_json(vehicules, chemin):
    donnees = [v.to_dict() for v in vehicules]
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)


def charger_flotte_json(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        donnees = json.load(f)
    return [vehicule_depuis_dict(d) for d in donnees]   
