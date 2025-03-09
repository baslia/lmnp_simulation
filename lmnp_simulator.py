import csv
from collections import defaultdict


def calculer_resultat_lmnp_annuel(revenus_locatifs, expenses_file):
    """Calcule le résultat imposable annuel en LMNP au régime réel."""

    charges_annuelles = defaultdict(float)
    with open(expenses_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            annee = row["date"].split("-")[0]  # Extraire l'année de la date
            charges_annuelles[annee] += float(row["montant"])

    resultats_annuels = {}
    for annee, charges in charges_annuelles.items():
        resultats_annuels[annee] = revenus_locatifs.get(annee, 0) - charges

    return resultats_annuels


# Exemple d'utilisation
revenus_locatifs = {
    "2023": 15000,
    "2024": 16000,
}  # Revenus locatifs annuels par année
expenses_file = "expenses.csv"

resultats = calculer_resultat_lmnp_annuel(revenus_locatifs, expenses_file)
for annee, resultat in resultats.items():
    print(f"Résultat imposable en LMNP pour {annee} : {resultat} €")
