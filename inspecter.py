import pandas as pd

df = pd.read_excel("tgv_regularite.xlsx")
cols = ["Date", "Service", "Liaison", "Prevus", "Annules", "Retard_arrivee"]

print("=== Doublons : quelques exemples ===")
dup = df[df.duplicated(["Date", "Depart", "Arrivee"], keep=False)]
print(dup.sort_values(["Liaison", "Date"])[cols].head(6).to_string())
print("Lignes doublons entièrement identiques :", df.duplicated().sum())

print("\n=== Annulés > prévus ===")
pb = df[df["Annules"] > df["Prevus"]]
print(pb[cols].head(6).to_string())
print("Mois concernés :", pb["Date"].dt.strftime("%Y-%m").value_counts().head(5).to_dict())
print("Mêmes lignes que 'retards > circulés' :",
      pb.index.equals(df[df["Retard_arrivee"] > df["Prevus"] - df["Annules"]].index))

print("\n=== Somme des causes ≠ 100 % ===")
causes = [c for c in df.columns if c.startswith("Cause_")]
somme = df[causes].sum(axis=1)
ecart = df[(somme - 100).abs() > 1]
print("Dont somme = 0 :", (somme[ecart.index] == 0).sum())
print("Dont retards à l'arrivée = 0 :", (ecart["Retard_arrivee"] == 0).sum())
print("Exemples de sommes :", somme[ecart.index].round(1).value_counts().head(5).to_dict())