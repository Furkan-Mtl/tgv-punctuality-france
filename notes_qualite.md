# Notes qualité : régularité mensuelle des TGV

Source : [Régularité mensuelle TGV par liaisons](https://www.data.gouv.fr/datasets/regularite-mensuelle-tgv-par-liaisons), SNCF / AQST, fichier CSV mis à jour le 2 octobre 2026.

## Le jeu de données

- 12 907 lignes, 26 colonnes
- Période : janvier 2018 à septembre 2026
- 130 liaisons, deux services : National (11 339 lignes) et International (1 568 lignes)
- Une ligne = un mois, un service et une liaison (gare de départ, gare d'arrivée)

## Définition d'un train à l'heure (SNCF)

Un train est à l'heure si son retard à l'arrivée est inférieur à un seuil qui dépend de la durée du trajet :

| Durée du trajet | Seuil |
| --- | --- |
| Moins de 1 h 30 | 5 minutes |
| De 1 h 30 à 3 h | 10 minutes |
| Plus de 3 h | 15 minutes |

La SNCF précise que le taux global n'est pas la moyenne des liaisons. Il ne faut donc pas calculer un taux national en faisant la moyenne des taux par liaison : il faut repartir des nombres de trains.

## Anomalies trouvées et décisions

| Anomalie | Explication | Décision |
| --- | --- | --- |
| 2 colonnes entièrement vides (`Commentaire annulations`, `Commentaire retards au départ`) | Jamais renseignées | Supprimées |
| `Date` au format texte (« 2018-01 ») | Format de la source | Convertie en vraie date (premier jour du mois) |
| 42 doublons apparents (même mois, même liaison) | Pas de vrais doublons : la même liaison existe en service National et International le même mois (ex. Bellegarde – Paris Lyon depuis 2025) | Gardés ; la clé d'une ligne est mois + service + liaison (0 doublon avec cette clé) |
| 63 lignes avec plus de trains annulés que prévus | Avril, mai et juin 2020 (confinement) : 0 train prévu mais des annulations comptées | Gardées, mais exclues des taux |
| 10 lignes avec 0 train prévu et 0 annulé | Liaison qui ne circulait pas ce mois-là | Exclues des taux (73 lignes exclues au total, colonne `Valide_taux`) |
| 272 lignes où toutes les causes de retard valent 0 % | 192 mois sans aucun retard à l'arrivée ; 80 mois avec des retards mais des causes non renseignées | Exclues de l'analyse des causes (colonne `Causes_renseignees`) |
| 9 lignes où la somme des causes est entre 84 % et 99 % | Arrondis ou petites lacunes | Gardées, écart négligeable |
| 354 lignes de janvier à mars 2025 (118, 117 et 119 lignes, soit presque toutes les liaisons) avec plus de retards de plus de 60 min que de plus de 30 min | La colonne `Retard_30` vaut 0, et même une valeur négative (-4, Lausanne - Paris Lyon, janvier 2025). `Retard_60` n'est pas égale à `Retard_15` sur ces lignes (3 sur 354), donc ce n'est pas un simple décalage de colonnes. Erreur de la source | 2025 exclue de l'analyse des retards de plus de 30 et 60 minutes (Q8) ; trouvé grâce à un contrôle de cohérence (`Retard_60` ne peut pas dépasser `Retard_30`) |
| Colonne « Retard moyen trains en retard > 15 (si liaison concurrencée par vol) » | Égale au retard moyen de tous les trains à l'arrivée dans 2 135 lignes sur 12 907 : définition peu claire | Supprimée |

## Colonnes ajoutées

| Colonne | Contenu |
| --- | --- |
| `Liaison` | « Gare de départ - Gare d'arrivée » |
| `Valide_taux` | Vrai si des trains étaient prévus et si les annulations ne dépassent pas les trains prévus |
| `Causes_renseignees` | Vrai si au moins une cause de retard est renseignée |

Le nettoyage est fait par `preparer.py` ; les vérifications détaillées par `inspecter.py`.
