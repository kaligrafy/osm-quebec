# La Petite-Nation (MRC de Papineau) : commentaires

Toutes les municipalités de la MRC de Papineau (Outaouais) selon le
MRNF : 25 municipalités et le TNO aquatique (la rivière des Outaouais).
Rien n'a encore été envoyé à OSM.

Rapports générés : [régions](regions.md), [rues](rues.md) et
[adresses](adresses.md), avec leurs cartes ([regions.geojson](regions.geojson),
[rues.geojson](rues.geojson), [adresses.geojson](adresses.geojson)).
Configuration : [lieux/Petite-Nation.toml](../../lieux/Petite-Nation.toml).

Données : RQA version AQ20261001, Découpages administratifs V2026-09,
extrait OSM de Geofabrik du 16 octobre 2026.

## 1. Régions

### Constat

- Les 25 municipalités ont une relation de limite dans OSM, trouvée par
  son code (`ref:qc`). Deux particularités :
  - **Notre-Dame-de-la-Salette** est rattachée dans OSM à la MRC des
    Collines-de-l'Outaouais, alors que le MRNF la place dans Papineau;
  - le **TNO aquatique** de la MRC n'a pas de relation dans OSM.
- Les limites d'OSM sont surtout faites de chemins propres, mais huit
  municipalités du sud (Fassett, Montebello, Notre-Dame-de-Bonsecours,
  Papineauville, Plaisance, Thurso, Lochaber, Lochaber-Partie-Ouest)
  utilisent aussi le tracé de la rivière (`waterway=river`) : le cas à
  éviter.
- Avec les limites actuelles d'OSM, **23 adresses sur 20 659** tombent du
  mauvais côté ou hors de toute municipalité. Par exemple :
  - chemin de la Plage (Val-des-Bois), placé dans Notre-Dame-de-la-Salette;
  - chemin du Ruisseau (Notre-Dame-de-la-Salette), placé dans Val-des-Bois;
  - route 315 (Ripon), placée dans Montpellier;
  - chemin Monaghan (Mayo), placé dans Lochaber-Partie-Ouest;
  - 2112 et 2116 chemin du Tour-du-Lac (Lac-Simon), placés dans Duhamel.

### Remplacement proposé

- 71 chemins de limite neufs, d'après le MRNF (8 556 nœuds) : une limite
  commune à deux municipalités est un seul chemin, membre des deux
  relations.
- 25 relations modifiées; 87 chemins retirés des relations, dont 51
  simples lignes de limite devenues inutiles, supprimées. Les rivières ne
  sont pas touchées.
- Vérification : avec les limites proposées, les 20 659 adresses tombent
  dans la bonne municipalité.

### Routes qui traversent les limites

| Situation | Nombre |
|---|---|
| Déjà coupée au bon endroit | 22 |
| Coupure à déplacer | 39 |
| Coupure à ajouter | 140 |

Les coupures à ajouter touchent surtout les routes numérotées et les
grands chemins : autoroute Guy-Lafleur (6), chemin Townline (5), chemin
du Lac-Gagnon Est (4), routes 309, 315 et 323. Liste complète dans
[regions.md](regions.md#routes-qui-traversent-les-limites).

### Questions en suspens

1. **Contour de la MRC.** Ici, les limites extérieures (avec les MRC
   voisines et l'Ontario) sont aussi tracées d'après le MRNF. Les
   municipalités voisines, hors de la MRC, gardent pour l'instant leurs
   anciens chemins : il y aura des tracés doubles le long du contour tant
   qu'elles ne sont pas traitées. Faut-il traiter la MRC voisine en même
   temps, ou mettre à jour aussi la relation de la MRC (7572164)?
2. **Notre-Dame-de-la-Salette** : corriger son rattachement à la MRC de
   Papineau dans OSM?
3. **TNO aquatique** : créer sa relation, ou laisser la rivière hors des
   municipalités comme aujourd'hui?
4. **Coupures** : 140 à ajouter et 39 à déplacer. Les automatiser une
   fois la règle validée?

## 2. Rues

| Situation | Rues | Adresses |
|---|---|---|
| Conforme | 1 253 | 19 374 |
| À renommer (casse, accents, tirets) | 32 | 734 |
| Nom différent dans OSM | 57 | 408 |
| Voie sans nom dans OSM | 30 | 112 |
| Absente d'OSM | 73 | 269 |

- **Renommage proposé : 44 segments**, par exemple « Chemin du Tour du
  Lac » qui devient « Chemin du Tour-du-Lac » (310 adresses), « Rue De La
  Forge » qui devient « Rue de la Forge », « Rang Des Sources » qui
  devient « Rang des Sources », « Impasse L P Lesage » qui devient
  « Impasse L.-P.-Lesage ».

### Exceptions à valider

- **Abréviations « St- » du RQA** contre « Saint- » dans OSM : « Rue
  St-Julien » et « Rue St-Denis » (Papineauville), « Chemin St-Pierre »
  (Saint-André-Avellin, Ripon). Le RQA les donne comme officielles.
- **Point cardinal** : « Route 321 Sud » (RQA) contre « Route 321 »
  (OSM), 60 adresses.
- **Ordinaux** : « 1re Avenue » (RQA) contre « 1e Avenue » (OSM).
- **Générique** : « Rue Sainte-Julie Est » (RQA) contre « Rang
  Sainte-Julie Est » (OSM).
- **Voies sans nom** le long des adresses (30 rues), par exemple Impasse
  des Conifères (Val-des-Bois, 20 adresses), Chemin des Chênes-Rouges.
- **Rues absentes** (73 rues, 269 adresses), dont l'**Île du
  Canard-Blanc** (lac Simon, 103 adresses), une île sans route.

### Questions en suspens

1. **« St- » ou « Saint- »?** Le RQA et OSM divergent; la Commission de
   toponymie tranche normalement. À vérifier avant de toucher à ces
   rues.
2. **Adresses d'une île** (Île du Canard-Blanc) : dans OSM, une adresse
   sans rue utilise `addr:place` plutôt que `addr:street`. Faut-il
   traiter ces cas ainsi?
3. **Nommer les voies sans nom** d'après le RQA : par règle, ou à la main?

## 3. Adresses

| Résultat | Nombre |
|---|---|
| Nouvelles, prêtes à créer | 19 403 |
| Déjà dans OSM, corrigées | 174 |
| Déjà dans OSM, inchangées | 52 |
| À revoir, non créées | 1 729 |
| Exclues | 1 |

- Les chiffres tiennent compte des renommages de rues prévus.
- Logements et suffixes fusionnés : 1 263 adresses en avaient; 676
  numéros n'ont pas d'adresse principale au RQA (on prend le point d'un
  logement ou d'un suffixe).
- Exclusion : le 131 chemin du Tour-du-Lac (Duhamel), absent du rôle
  d'évaluation.
- **3 908 lignes d'interpolation CanVec supprimées** (48 254 nœuds),
  seulement celles des rues importées, à moins de 300 m d'une adresse de
  la même rue et attribuées à une municipalité de la MRC.
- **Positions peu précises** : parmi les nouvelles adresses, seulement
  3 528 sont de qualité « Bâtiment »; 9 504 sont « Géocodée », 6 000
  « Incertaine », 302 « Centre lot » et 68 « Front lot ». Le point est
  souvent au bord de la route plutôt que sur le bâtiment.

### Questions en suspens

1. **Précision** : avec 80 % de points « Géocodée » ou « Incertaine »,
   l'import vaut-il mieux que les interpolations qu'il remplace? Les
   numéros deviennent exacts, mais la position reste approximative. Les
   portes d'entrée de la Chaire Mobilité couvrent l'est du Québec, pas
   l'Outaouais.
2. **Ampleur** : 19 403 nœuds et 3 908 interpolations supprimées en un
   seul envoi, ou par municipalité?

## 4. Prochaines étapes

1. Régler les questions des limites (contour de la MRC, TNO,
   Notre-Dame-de-la-Salette), puis discussion publique.
2. Noms de rue : appliquer les renommages sûrs, trancher les autres.
3. Adresses, probablement municipalité par municipalité.
