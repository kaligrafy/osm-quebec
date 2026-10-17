# osmqc : importer les données officielles du Québec dans OpenStreetMap

Outils pour préparer, faire réviser et envoyer dans OpenStreetMap des
données ouvertes du gouvernement du Québec : adresses du Référentiel
québécois des adresses (RQA) et limites municipales des Découpages
administratifs (SDA), toutes deux du ministère des Ressources naturelles
et des Forêts (MRNF).

Le but est que la communauté puisse vérifier les **règles** appliquées
plutôt que de relire des milliers d'adresses une à une. Chaque
préparation produit des rapports de révision, lisibles sur GitHub
(voir Résultats).

Discussions : [compte-rendu de la rencontre du 16 octobre 2026](https://community.openstreetmap.org/t/148901),
[import du chemin du Gros-Cap](https://community.openstreetmap.org/t/148723).

## Résultats

État au 17 octobre 2026 (extrait OSM du 16 octobre). Rien n'a encore
été envoyé à OSM : ces résultats sont soumis à la révision de la
communauté. Pour chaque lieu, `rapports/LIEU/` contient :

- `README.md`, un commentaire rédigé : statistiques, exceptions à
  valider, questions en suspens;
- `regions.md`, `rues.md` et `adresses.md`, les rapports générés, avec
  leurs tableaux;
- les GeoJSON correspondants, que GitHub affiche sur une carte. Chaque
  objet porte ses propriétés (`statut` pour les adresses et les rues,
  `source` pour les limites, `coupure` pour les routes) : ce sont elles
  qui font foi. Les couleurs suivent la convention simplestyle, que tous
  les afficheurs ne respectent pas.

| Lieu | Municipalités | Limites : adresses mal placées dans OSM | Rues à renommer | Adresses prêtes | Adresses à revoir |
|---|---|---|---|---|---|
| [Îles-de-la-Madeleine](rapports/Iles_de_la_Madeleine/) | 2 | 3 sur 7 394 (0 après correction) | 28 segments | 7 235 | 131 |
| [La Petite-Nation (MRC de Papineau)](rapports/Petite-Nation/) | 25 | 23 sur 20 659 (0 après correction) | 44 segments | 19 403 | 1 729 |

## Licences

- Le code : licence MIT (fichier `LICENSE`).
- Les données d'entrée et leurs licences : voir
  [donnees/README.md](donnees/README.md).

## Installation

Python 3.11 ou plus récent, avec pyosmium (paquet `python3-osmium` de
Fedora ou Debian, ou `pip install osmium`). Les données sources
(RQA, Découpages administratifs, extrait d'OSM) ne sont pas incluses
dans ce dépôt, seulement les rapports de révision qui en découlent
(`rapports/`). La provenance des données sources, leur téléchargement et
leur organisation sont décrits dans [donnees/README.md](donnees/README.md).

## Utilisation

Chaque lieu est décrit par un fichier `lieux/LIEU.toml` (exemple :
`lieux/Iles_de_la_Madeleine.toml`). Trois sections, dans cet ordre :
les régions (limites municipales), les rues, les adresses (voir
« Ordre des étapes »).

```
python3 -m osmqc adresses extraire lieux/Iles_de_la_Madeleine.toml   # adresses du lieu, tirées du RQA

python3 -m osmqc regions comparer lieux/Iles_de_la_Madeleine.toml    # limites OSM contre MRNF
python3 -m osmqc regions preparer lieux/Iles_de_la_Madeleine.toml    # remplacement des limites
python3 -m osmqc regions envoyer lieux/Iles_de_la_Madeleine.toml --test

python3 -m osmqc adresses osm lieux/Iles_de_la_Madeleine.toml        # données OSM autour des adresses

python3 -m osmqc rues preparer lieux/Iles_de_la_Madeleine.toml       # noms de rue contre noms officiels
python3 -m osmqc rues envoyer lieux/Iles_de_la_Madeleine.toml --test

python3 -m osmqc adresses preparer lieux/Iles_de_la_Madeleine.toml   # import des adresses
python3 -m osmqc adresses envoyer lieux/Iles_de_la_Madeleine.toml --test
```

`--test` envoie au serveur de test d'OSM; `--reel` à OpenStreetMap, ce
qui est refusé tant que la discussion publique n'est pas inscrite dans
la section `groupe` correspondante du lieu. Pour l'authentification,
voir l'en-tête de `osmqc/envoi.py`.

Les fichiers d'envoi (`.osc`) et un CSV de toutes les adresses vont
dans `sortie/LIEU/` (hors du dépôt); les rapports de révision, dans
`rapports/LIEU/` (voir Résultats).

## Règles appliquées

### Ordre des étapes

1. **Les limites municipales** d'abord : la municipalité d'une adresse
   se déduit alors de la limite qui la contient, sans `addr:city` sur
   chaque nœud.
2. **Les rues** ensuite : une adresse n'est créée que si sa rue existe
   dans OSM sous son nom officiel.
3. **Les adresses** enfin.

### Régions

1. **Les limites du MRNF ont préséance** sur celles d'OSM (Découpages
   administratifs, 1/20 000).
2. **Des chemins propres.** Une limite ne partage jamais ses nœuds avec
   le littoral, une route ou un cours d'eau, même quand elle les suit :
   déplacer l'un déplacerait l'autre. Les chemins de limite créés ne
   portent que `boundary=administrative` et `admin_level`.
3. **Une limite commune est un seul chemin**, membre des relations des
   deux municipalités (rôles `outer` et `inner` selon le cas).
4. **Contour extérieur** : un contour qui ne borde aucune autre
   municipalité du lieu et forme à lui seul un anneau fermé (le large,
   autour d'îles) peut reprendre les chemins d'une relation parente au
   lieu d'être tracé d'après le MRNF (`exterieur =` dans le lieu). Aux
   Îles, ce sont des limites interprovinciales en mer, reprises de la
   Communauté maritime. Un contour ouvert est toujours tracé d'après le
   MRNF, pour se raccorder aux limites voisines par les mêmes nœuds.
5. **Ce qui sort des relations** : le littoral et les autres objets sont
   seulement retirés des relations, sans être modifiés. Une simple ligne
   de limite qui ne sert plus à aucune relation est supprimée, avec ses
   nœuds s'ils ne servent à rien d'autre dans OSM.
6. **Vérification** : le rapport compare la municipalité de chaque
   adresse du RQA selon le MRNF, les limites actuelles d'OSM et les
   limites proposées.
7. **Routes qui traversent les limites** : une route nommée doit être
   coupée là où elle traverse une limite, à moins de 25 m. Le rapport
   classe chaque croisement : déjà coupé, coupure à ajouter, coupure à
   déplacer, ou coupure devenue inutile (sur l'ancienne limite, entre
   deux segments aux étiquettes identiques). Rien n'est encore modifié.

### Rues

1. **Nom officiel** : l'odonyme recomposé du RQA (repris de la
   Commission de toponymie), dans l'ordre usuel (« 4e Rang Sud »), sans
   le discriminant des municipalités fusionnées (« Chemin du Gros-Cap »
   et non « Chemin du Gros-Cap (L'Étang-du-Nord) »).
2. **Renommage automatique** seulement quand le nom d'OSM ne diffère du
   nom officiel que par la casse, les accents, les tirets ou les espaces
   (« Chemin de la Martinique » devient « Chemin de La Martinique »).
   Tous les segments reliés qui portent ce nom sont renommés, trottoirs
   compris, même loin des adresses; une rue homonyme qui n'y est pas
   reliée n'est pas touchée.
3. **Autres écarts, rapportés seulement** : une voie proche qui porte un
   autre nom, une voie sans nom le long des adresses (candidate pour
   recevoir le nom officiel), ou aucune voie. Ils se règlent à la main ou
   par une section `[[rues.modifier]]` du lieu.
4. La préparation des adresses tient compte des renommages prévus.

### Adresses

1. **Une adresse par numéro de base et par rue.** Le RQA répète le
   point pour chaque logement d'un immeuble (2-1701, 329 1) : seul le
   numéro de base est créé. Un suffixe (120A) au même point que son
   numéro de base est fusionné; placé à plus de 5 m, il devient une
   adresse distincte.
2. **Adresses terminées** (`date_fin` remplie) : ignorées.
3. **Exclusions** : une liste explicite, avec la raison, dans le fichier
   du lieu (par exemple une adresse absente du rôle d'évaluation).
4. **La rue doit exister dans OSM** sous exactement son nom officiel
   (voir Rues), à moins de 300 m. Sinon, l'adresse n'est pas créée et
   passe « à revoir » : rue absente, sans nom ou écrite autrement dans
   OSM. Les rues se corrigent d'abord, les adresses suivent.
5. **Doublons** : une adresse OSM au même numéro, à moins de 30 m (ou
   un bâtiment ou terrain qui contient le point), n'est pas recréée.
   On y corrige `addr:street` s'il diffère du nom officiel et on y
   ajoute `addr:postcode` s'il manque. Rien d'autre n'est touché.
6. **Étiquettes créées** : `addr:housenumber`, `addr:street`,
   `addr:postcode`. Pas d'`addr:city` (voir l'ordre des étapes).
   Pas d'identifiant du RQA dans OSM.
7. **Interpolations CanVec** : une ligne `addr:interpolation` est
   supprimée avec ses nœuds, puisque les vraies adresses la remplacent,
   si ses deux extrémités portent le nom d'une rue importée, si elle passe
   à moins de 300 m d'une adresse de cette rue, si CanVec l'attribue à
   une municipalité du lieu, et si ses nœuds ne servent à rien d'autre et
   ne portent que des étiquettes CanVec.
8. **Position** : le point du RQA, sauf si une source plus précise est
   donnée (section `[adresses.positions]`, par exemple les portes d'entrée
   placées à la main sur l'imagerie). Le point de cette source est relié
   à l'adresse par le matricule, le lot, l'identifiant du RQA ou
   l'adresse elle-même; trop loin du point du RQA (150 m par défaut), il
   est ignoré. Le rapport indique la source retenue pour chaque adresse.

### Groupe de modifications

Chaque envoi porte `import=yes`, `source=` (la source et sa version),
le commentaire et le lien de la discussion publique. Un envoi est pour
l'instant un seul groupe (voir « À automatiser » pour le découpage).

## Traiter une nouvelle région

1. **Créer le fichier du lieu**, `lieux/NOM.toml`. Son nom (sans
   `.toml`) sert partout : `donnees/NOM/`, `sortie/NOM/`,
   `rapports/NOM/`. Choisir les municipalités, soit toutes celles d'une
   MRC (`mrc = "80"` dans `[regions]`), soit une liste de codes
   géographiques (`municipalites` dans `[rqa]`). Les codes viennent des
   Découpages administratifs du MRNF.
2. **Trouver les relations OSM** des municipalités :
   `python3 -m osmqc regions trouver lieux/NOM.toml` affiche la section
   `[regions.osm]` à copier dans le fichier. Une municipalité sans
   relation, ou rattachée ailleurs dans OSM, y est signalée.
3. **Lancer les étapes** dans l'ordre de la section Utilisation :
   extraction, régions, données OSM, rues, adresses.
4. **Lire les rapports** générés dans `rapports/NOM/` et ajouter au
   besoin des exclusions ou des renommages décidés à la main
   (`exclure`, `[[rues.modifier]]`), puis relancer.
5. **Rédiger le commentaire** `rapports/NOM/README.md` (statistiques,
   exceptions à valider, questions en suspens) et ajouter le lieu au
   tableau des Résultats.

### Le fichier d'un lieu

Toutes les sections possibles, d'après l'exemple des Îles (l'exclusion
vient de la Petite-Nation) :

```toml
nom = "Les Îles-de-la-Madeleine"

[rqa]
municipalites = ["01023", "01042"]   # codes géographiques
# odonymes = ["178477"]              # seqodo, pour se limiter à certaines rues

[regions]
# mrc = "80"                         # à la place de [rqa] municipalites : toute la MRC
osm = { "01023" = 8402197, "01042" = 8402196 }   # relations OSM à remplacer
exterieur = 8405826                  # facultatif : relation parente réutilisée

[regions.groupe]
comment = "Limites municipales d'après les Découpages administratifs du MRNF"
source = "Découpages administratifs (MRNF), version V2026-09"
discussion = "https://community.openstreetmap.org/t/..."

[adresses]
supprimer_interpolations = true
corriger_rue_existante = true
creer_si_rue_absente = false
exclure = [ { municipalite = "80135", rue = "Chemin du Tour-du-Lac", numero = "131", raison = "absent du rôle" } ]

[adresses.positions]                 # facultatif
fichier = "donnees/portes.geojson"
propriete = "matricule"              # propriété du GeoJSON
cle_rqa = "matricule"                # matricule, lot, ident ou adresse
ecart_max_m = 150
nom = "portes"

[[rues.modifier]]                    # renommages décidés à la main
type = "way"
id = 1221212557
tags = { name = "Chemin de Gros-Cap", alt_name = "Chemin du Gros-Cap" }
raison = "nom officiel du tronçon de Cap-aux-Meules"

[adresses.groupe]
comment = "Adresses des Îles-de-la-Madeleine d'après le Référentiel québécois des adresses"
source = "Référentiel québécois des adresses (MRNF), version AQ20261001"
discussion = "https://community.openstreetmap.org/t/..."
```

## Durées et usage des serveurs

Les données d'OSM sont lues dans un extrait local du Québec
(`.osm.pbf`, voir [donnees/README.md](donnees/README.md)), avec pyosmium,
plutôt que demandées à l'API d'OSM : les règles d'usage de l'API
découragent les téléchargements en masse. L'API ne sert plus qu'à de
petites lectures groupées : la version actuelle des objets à modifier,
juste avant d'écrire le fichier d'envoi. Sans extrait, l'outil se
rabat sur l'API pour une très petite zone seulement (au plus 20
tuiles) et refuse au-delà.

Mesures du 17 octobre 2026, avec l'extrait :

| Étape | Îles (7 400 adresses) | Petite-Nation (21 000 adresses) |
|---|---|---|
| Téléchargement de l'extrait du Québec (1,2 Go, Geofabrik) | ~1 min | (le même) |
| Téléchargement du RQA et des découpages (MRNF) | de 30 min à quelques heures, une fois | (les mêmes) |
| `adresses extraire` | ~40 s | ~40 s |
| `adresses osm` | ~55 s | ~55 s |
| `regions trouver` | ~1 s | ~1 s |
| `regions preparer` | ~2 min | ~2 min |
| `rues preparer` | ~20 s | ~20 s |
| `adresses preparer` | ~5 s | ~10 s |

La lecture de l'extrait prend environ 4 Go de mémoire. Chaque étape
relit l'extrait en entier une ou plusieurs fois : la durée dépend peu de
la taille du lieu.

Avant de préparer un envoi, mettre l'extrait à jour sur place avec les
changements publiés par OSM (quelques minutes) :

```
pyosmium-up-to-date donnees/quebec-latest.osm.pbf
```

## À automatiser

Liste au 17 octobre 2026, par ordre de priorité.

### Avant tout envoi

1. **Découper les gros envois.** L'API d'OSM refuse un groupe de
   modifications de plus de 10 000 objets; celui des adresses de la
   Petite-Nation en compte environ 72 000 (créations et suppressions
   d'interpolations). Découper, par exemple par municipalité, avec la
   même discussion inscrite sur chaque groupe.
2. **Reprise en cas d'échec.** Savoir ce qui est passé après un envoi
   interrompu ou refusé pour un conflit de version, pour ne rien envoyer
   deux fois.
3. **Fraîcheur de l'extrait.** Lancer `pyosmium-up-to-date`
   automatiquement, ou refuser de préparer un envoi à partir d'un extrait
   trop vieux.

### Régions

4. **Coupures de routes** : couper une route à la nouvelle limite,
   déplacer une coupure mal placée, fusionner celles devenues inutiles
   (aujourd'hui seulement rapportées).
5. **Relation de la MRC** : la reconstruire à partir des limites
   extérieures de ses municipalités, pour éviter les tracés doubles le
   long du contour.
6. **Relations manquantes ou mal rattachées** : créer celles qui
   n'existent pas (TNO aquatique), vérifier que chaque municipalité est
   membre de la bonne MRC (Notre-Dame-de-la-Salette).
7. **Anciennes municipalités** (niveau 9 ou 10) : simple à coder, mais il
   manque une source autorisée pour les tracés.

### Rues

8. **Nommer les voies sans nom** quand une seule voie dessert toutes les
   adresses d'une rue, si la communauté accepte la règle.
9. **`addr:place`** pour les adresses sans rue (Île du Canard-Blanc).
10. **Abréviations** (« St- » ou « Saint- ») : une règle, une fois
    tranché qui fait autorité.

### Adresses

11. **Portes d'entrée** de la Chaire Mobilité : prêt dans l'outil
    (section `[adresses.positions]`), il manque les données.
12. **Interpolations** : ne supprimer une ligne que si sa rue reçoit
    vraiment des adresses (aujourd'hui, une rue « à revoir » peut perdre
    son interpolation sans rien recevoir).
13. **Anomalies du RQA** : liste automatique des logements sans lot et
    des adresses absentes du rôle d'évaluation (comme le logement
    9999-2225 chemin du Lac-Gagnon Ouest ou le 34 chemin de la
    Pointe-à-Baptiste, à Duhamel), pour les signalements au MRNF.

## Tests

```
python3 -m unittest discover tests
```

Les tests (`tests/test_regles.py` et `tests/test_rues_coupures.py`)
vérifient les règles sur de petits exemples construits à la main, sans
données ni accès réseau :

| Groupe | Ce qui est vérifié |
|---|---|
| Géométrie | distances; point dans un polygone avec trou; assemblage de segments en anneaux fermés |
| Noms de rue | nom tiré de la forme recomposée du RQA, sans le discriminant (« Chemin du Gros-Cap »), dans l'ordre usuel (« 4e Rang Sud »); recomposition à partir des parties (« Rue d'Amiens », « Rue Sherbrooke Est »); comparaison insensible à la casse, aux accents et aux tirets |
| Regroupement des adresses | logements fusionnés au numéro de base; suffixe au même point fusionné; suffixe ailleurs gardé comme adresse distincte (120A); numéro sans adresse principale |
| Doublons | adresse OSM au même numéro à moins de 30 m, ou bâtiment qui contient le point, reconnue; numéro différent ou trop loin, non reconnue |
| Limites | trou d'une municipalité occupé par une autre : un seul arc, intérieur pour l'une et extérieur pour l'autre; deux municipalités voisines : un arc commun et un arc propre à chacune |
| Rues | nom identique déclaré conforme; différence de casse renommée sur toute la rue, segments reliés compris; tirets et accents (« Tour du Lac » devient « Tour-du-Lac »); autre nom signalé sans être renommé; voie sans nom proposée comme candidate; rue absente; chemin réclamé par deux noms officiels mis en conflit |
| Coupures de routes | coupure déjà sur la limite; coupure à ajouter; coupure à déplacer; cul-de-sac au bord de l'ancienne limite ignoré; coupure devenue inutile entre deux segments identiques; coupure qui sert à autre chose (un pont) ignorée |

Ils ne remplacent pas la révision des rapports : les vérifications sur
les données réelles (municipalité de chaque adresse avant et après le
remplacement des limites, entre autres) sont dans les rapports de
chaque lieu.
