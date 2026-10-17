# Positions plus précises des adresses, par exemple les portes d'entrée
# placées à la main sur l'imagerie (données de la Chaire Mobilité), lues
# dans un fichier GeoJSON de points.
#
# Chaque point est relié à une adresse du RQA par une clé, au choix :
#   matricule  matricule de l'unité d'évaluation (rôle foncier)
#   lot        numéro de lot
#   ident      identifiant_unique_adresse du RQA
#   adresse    « numéro|nom de rue|code municipalité »
# Sans correspondance, ou si le point est trop loin de celui du RQA (ce
# qui trahit une erreur d'appariement), on garde le point du MRNF.

import json

from . import geo
from .adresses import cle_nom


def cle_rqa(a, champ):
    if champ == "matricule":
        return a.matricule
    if champ == "lot":
        return a.lot.split(",")[0] if a.lot else ""
    if champ == "ident":
        return a.ident
    if champ == "adresse":
        return "%s|%s|%s" % (a.numero, cle_nom(a.rue), a.municipalite)
    raise ValueError("clé inconnue : %s" % champ)


class Positions:
    def __init__(self, conf):
        """conf : section [positions] du lieu (fichier, propriete, cle_rqa,
        ecart_max_m, nom)."""
        self.champ = conf.get("cle_rqa", "matricule")
        self.ecart_max = conf.get("ecart_max_m", 150)
        self.nom = conf.get("nom", "portes")
        self.points = {}
        prop = conf["propriete"]
        with open(conf["fichier"], encoding="utf-8") as fh:
            for f in json.load(fh)["features"]:
                g = f.get("geometry") or {}
                if g.get("type") != "Point":
                    continue
                v = f.get("properties", {}).get(prop)
                if v not in (None, ""):
                    self.points.setdefault(str(v).strip(), tuple(g["coordinates"][:2]))

    def position(self, a):
        """(point, source, remarque) pour une adresse du RQA."""
        cle = cle_rqa(a, self.champ)
        p = self.points.get(cle) if cle else None
        if p is None:
            return a.point, "RQA", ""
        d = geo.distance(p, a.point)
        if d > self.ecart_max:
            return a.point, "RQA", "point %s ignoré, à %.0f m du RQA" % (self.nom, d)
        return p, self.nom, "%.0f m du point RQA" % d if d >= 1 else ""


class Aucune:
    """Pas de source de positions : toujours le point du MRNF."""

    def position(self, a):
        return a.point, "RQA", ""
