import pandas as pd

df = pd.read_csv("regularite-mensuelle-tgv.csv", sep=";", encoding="utf-8")

# 1. Colonnes vides ou inutilisables
df = df.drop(columns=[
    "Commentaire annulations",
    "Commentaire retards au départ",
    "Retard moyen trains en retard > 15 (si liaison concurrencée par vol)",
])

# 2. Noms courts
df = df.rename(columns={
    "Gare de départ": "Depart",
    "Gare d'arrivée": "Arrivee",
    "Durée moyenne du trajet": "Duree_min",
    "Nombre de circulations prévues": "Prevus",
    "Nombre de trains annulés": "Annules",
    "Nombre de trains en retard au départ": "Retard_depart",
    "Retard moyen des trains en retard au départ": "Retard_moy_retardes_depart",
    "Retard moyen de tous les trains au départ": "Retard_moy_tous_depart",
    "Nombre de trains en retard à l'arrivée": "Retard_arrivee",
    "Retard moyen des trains en retard à l'arrivée": "Retard_moy_retardes_arrivee",
    "Retard moyen de tous les trains à l'arrivée": "Retard_moy_tous_arrivee",
    "Commentaire retards à l'arrivée": "Commentaire_arrivee",
    "Nombre trains en retard > 15min": "Retard_15",
    "Nombre trains en retard > 30min": "Retard_30",
    "Nombre trains en retard > 60min": "Retard_60",
    "Prct retard pour causes externes": "Cause_externes",
    "Prct retard pour cause infrastructure": "Cause_infrastructure",
    "Prct retard pour cause gestion trafic": "Cause_gestion_trafic",
    "Prct retard pour cause matériel roulant": "Cause_materiel",
    "Prct retard pour cause gestion en gare et réutilisation de matériel": "Cause_gare",
    "Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH, correspondances)": "Cause_voyageurs",
})

# 3. Vraie date et nom de la liaison
df["Date"] = pd.to_datetime(df["Date"] + "-01")
df["Liaison"] = df["Depart"] + " - " + df["Arrivee"]

# 4. Indicateurs de validité
causes = [c for c in df.columns if c.startswith("Cause_")]
df["Valide_taux"] = (df["Prevus"] > 0) & (df["Annules"] <= df["Prevus"])
df["Causes_renseignees"] = df[causes].sum(axis=1) > 0

# 5. Contrôles qualité
print("Lignes, colonnes :", df.shape)
print("Période :", df["Date"].min().date(), "au", df["Date"].max().date())
print("Doublons (mois + service + liaison) :", df.duplicated(["Date", "Service", "Depart", "Arrivee"]).sum())
print("Lignes exclues des taux :", (~df["Valide_taux"]).sum())
print("Lignes exclues de l'analyse des causes :", (~df["Causes_renseignees"]).sum())

# 6. Enregistrement : toujours en dernier
df.to_excel("tgv_regularite.xlsx", index=False)
print("Fichier tgv_regularite.xlsx créé, dernières colonnes :", df.columns[-3:].tolist())