# Limites municipales : Les Îles-de-la-Madeleine

Données OSM : extrait quebec-latest.osm.pbf du 2026-10-16.

Source : Découpages administratifs du MRNF (1/20 000). Règles : voir le [README](../../README.md#régions). Carte : [regions.geojson](regions.geojson) (bleu : MRNF; rouge : OSM actuel). Commentaires : [README](README.md).

## Limites actuelles dans OSM

| Municipalité | Relation | Anneaux | Chemins qui la forment |
|---|---|---|---|
| Les Îles-de-la-Madeleine | [8402197](https://www.openstreetmap.org/relation/8402197) | 5 | natural=coastline 417, limite seule 5 |
| Grosse-Île | [8402196](https://www.openstreetmap.org/relation/8402196) | 3 | natural=coastline 65, limite seule 2 |

## Limites officielles (MRNF)

| Municipalité | Code | Version | Polygones | Trous | Sommets |
|---|---|---|---|---|---|
| Les Îles-de-la-Madeleine | 01023 | V2026-09 | 1 | 3 | 5759 |
| Grosse-Île | 01042 | V2026-09 | 3 | 0 | 5717 |

## Adresses : municipalité selon chaque limite

| Limite | Bonne municipalité | Autre ou aucune |
|---|---|---|
| MRNF | 7394 | 0 |
| OSM actuel | 7391 | 3 |
| OSM après le remplacement proposé | 7394 | 0 |

| Adresse | Municipalité (RQA) | Selon le MRNF | Selon OSM |
|---|---|---|---|
| 127 Chemin du Parc | 01023 | 01023 | aucune |
| 50 Chemin du Quai | 01023 | 01023 | aucune |
| 998 Chemin Principal | 01042 | 01042 | 01023 |

## Remplacement proposé

| Élément | Nombre |
|---|---|
| Nœuds créés | 5714 |
| Chemins de limite créés | 5 |
| Relations modifiées | 2 |
| Chemins retirés des relations | 487 |
| dont supprimés (simples lignes de limite inutilisées) | 2 |
| Nœuds supprimés | 1 |

- arc de 22 sommets (01023 inner, 01042 outer) : 1 chemin(s) neuf(s)
- arc de 5628 sommets (01023 inner, 01042 outer) : 3 chemin(s) neuf(s)
- arc de 67 sommets (01023 inner, 01042 outer) : 1 chemin(s) neuf(s)
- anneau extérieur de 42 sommets (01023) : 7 chemins de la relation 8405826 réutilisés

Chemins supprimés : [600699235](https://www.openstreetmap.org/way/600699235), [600699240](https://www.openstreetmap.org/way/600699240).

Le littoral et les autres objets retirés des relations ne sont pas modifiés : seule leur appartenance aux limites change.

## Routes qui traversent les limites

Une route nommée doit être coupée là où elle traverse une limite municipale, pour que chaque côté garde son nom (à moins de 25 m). Rien n'est encore modifié : ces cas sont à valider.

| Situation | Nombre |
|---|---|
| déjà coupée | 1 |
| coupure à déplacer | 1 |
| coupure à ajouter | 0 |
| coupure devenue inutile | 1 |

| Situation | Rue | Chemin | Position | Écart |
|---|---|---|---|---|
| coupure devenue inutile | Chemin de la Grave | [1217383411](https://www.openstreetmap.org/way/1217383411) | 47.23693, -61.82790 | 13 m |
| coupure à déplacer | Route 199 | [27708492](https://www.openstreetmap.org/way/27708492) | 47.57047, -61.49746 | 355 m |
