# Données d'entrée

Ce répertoire contient les données utilisées par `osmqc`. Seul ce
fichier est dans le dépôt : le reste est téléchargé ou produit, trop
volumineux ou régénérable. Les commandes ci-dessous se lancent depuis
la racine du dépôt.

## Sources officielles

Les deux sources viennent du ministère des Ressources naturelles et des
Forêts du Québec (MRNF), Direction générale de l'information
géospatiale. Licence CC BY 4.0, avec une [permission explicite pour
OpenStreetMap](https://wiki.openstreetmap.org/wiki/FR:Minist%C3%A8re_des_Ressources_naturelles_et_des_For%C3%AAts) :
l'attribution par la page des contributeurs d'OSM suffit, et le MRNF
renonce à la clause qui serait incompatible avec la licence ODbL. La
permission couvre notamment le Référentiel québécois des adresses, les
Découpages administratifs, le Référentiel québécois sur les bâtiments,
le réseau routier et l'imagerie orthorectifiée.

| Fichier | Contenu | Téléchargement |
|---|---|---|
| `RQA_CSV.zip` | Référentiel québécois des adresses (RQA), fichier complet : un seul `RQA.csv` d'environ 3 Go, une ligne par adresse ou logement. Mis à jour chaque mois. | <https://diffusion.mern.gouv.qc.ca/diffusion/RGQ/Vectoriel/Theme/Local/RQA/CSV/RQA_CSV.zip> (environ 800 Mo) |
| `SDA.gpkg` | Découpages administratifs à 1/20 000 (SDA) : municipalités (`munic_s`), MRC (`mrc_s`), régions, arrondissements. | <https://diffusion.mern.gouv.qc.ca/diffusion/RGQ/Vectoriel/Theme/Local/SDA_20k/GPKG/SDA.gpkg.zip> (environ 100 Mo, à décompresser) |

Le serveur du MRNF est lent et coupe souvent les transferts. `curl -C -`
reprend là où le transfert s'est arrêté :

```
curl -C - --retry 20 --retry-all-errors -o donnees/RQA_CSV.zip https://diffusion.mern.gouv.qc.ca/diffusion/RGQ/Vectoriel/Theme/Local/RQA/CSV/RQA_CSV.zip
curl -C - --retry 20 --retry-all-errors -o donnees/SDA.gpkg.zip https://diffusion.mern.gouv.qc.ca/diffusion/RGQ/Vectoriel/Theme/Local/SDA_20k/GPKG/SDA.gpkg.zip
unzip -d donnees donnees/SDA.gpkg.zip
```

Les chemins peuvent aussi être donnés par les variables `$OSMQC_RQA` et
`$OSMQC_SDA`.

Documentation du RQA (champs, qualité de positionnement) : guide
d'utilisation publié par le MRNF avec le jeu de données, sur
[Données Québec](https://www.donneesquebec.ca/recherche/dataset/referentiel-quebecois-des-adresses).

### Champs du RQA utilisés

| Champ | Usage |
|---|---|
| `code_municipalite`, `nom_municipalite` | municipalité de l'adresse |
| `seqodo`, `odonyme_recompose_normal`, `discriminant_odonyme` | rue et nom officiel (sans le discriminant des municipalités fusionnées) |
| `numero_municipal`, `numero_municipal_suffixe`, `numero_unite` | numéro, suffixe (120A), logement (2-1701) |
| `code_postal` | `addr:postcode` |
| `longitude`, `latitude`, `qualite_positionnement_geometrique` | position et sa qualité (Bâtiment, Géocodée, Incertaine, Centre lot, Front lot) |
| `numero_lot`, `matricule_unite_evaluation`, `identifiant_unique_adresse` | appariement avec une autre source de positions |
| `date_fin` | adresse qui n'existe plus |

## Données OpenStreetMap

© les contributeurs d'OpenStreetMap, licence ODbL.

| Fichier | Contenu | Téléchargement |
|---|---|---|
| `quebec-latest.osm.pbf` | Extrait d'OSM pour le Québec, au format PBF, publié chaque jour par Geofabrik | <https://download.geofabrik.de/north-america/canada/quebec-latest.osm.pbf> (environ 1,2 Go) |

```
curl -L -o donnees/quebec-latest.osm.pbf https://download.geofabrik.de/north-america/canada/quebec-latest.osm.pbf
pyosmium-up-to-date donnees/quebec-latest.osm.pbf     # mise à jour, avant chaque préparation
```

Le `-L` est nécessaire : Geofabrik redirige vers un fichier daté. Le
chemin peut aussi être donné par `$OSMQC_PBF`. Sans extrait, l'outil
demande les données à l'API d'OSM, pour une très petite zone seulement.

La version actuelle des objets à modifier est relue dans OSM (API) au
moment de la préparation, pour partir de leur dernière version.

## Fichiers produits pour chaque lieu

Tirés des sources ci-dessus, dans `donnees/LIEU/` :

| Fichier | Produit par | Contenu |
|---|---|---|
| `rqa.csv` | `adresses extraire` | lignes du RQA pour les municipalités du lieu |
| `osm.json` | `adresses osm` | objets OSM autour des adresses : nœuds d'adresse, rues, bâtiments, interpolations |
| `osm_limites.json` | `regions preparer` | routes le long des limites (celles qui les traversent) |
| `osm_source.txt` | `adresses osm`, `regions preparer` | provenance et date des données OSM, reprises dans les rapports |

Pour repartir de données à jour, effacer ces fichiers et relancer les
étapes.

## Sources facultatives

Positions plus précises des adresses, par exemple les portes d'entrée
placées à la main sur l'imagerie par la Chaire Mobilité de Polytechnique
Montréal : un fichier GeoJSON de points, déclaré dans la section
`[adresses.positions]` du lieu (voir le [README](../README.md)). Sa
licence doit permettre l'usage dans OSM.
