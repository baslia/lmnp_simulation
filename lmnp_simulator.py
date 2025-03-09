import csv
from collections import defaultdict


def calculer_resultat_lmnp_annuel(data_file, amortissements_file):
    """Calcule le résultat imposable annuel en LMNP au régime réel avec amortissements."""

    donnees_annuelles = defaultdict(lambda: defaultdict(float))
    amortissements_details = defaultdict(
        lambda: defaultdict(lambda: defaultdict(float))
    )

    # Lecture des données principales
    with open(data_file, "r") as fichier_csv:
        lecteur_csv = csv.DictReader(fichier_csv)
        for ligne in lecteur_csv:
            annee = ligne["date"].split("-")[0]
            for cle, valeur in ligne.items():
                if cle != "date":
                    try:
                        donnees_annuelles[annee][cle] += float(valeur)
                    except ValueError:
                        pass

    # Lecture des détails des amortissements
    with open(amortissements_file, "r") as fichier_amortissements:
        lecteur_amortissements = csv.DictReader(fichier_amortissements)
        for ligne in lecteur_amortissements:
            annee = ligne["date"].split("-")[0]
            categorie = ligne["categorie"]
            composant = ligne["composant"]
            valeur = float(ligne["valeur"])
            duree = int(ligne["duree"])
            amortissements_details[annee][categorie][composant] = {
                "valeur": valeur,
                "duree": duree,
            }

    resultats_annuels = {}
    for annee, donnees in donnees_annuelles.items():
        loyers_annuels = donnees.get("loyers_annuels", 0)
        tranche_marginale_impots = donnees.get("tranche_marginale_impots", 0)
        taxes_annuelles = donnees.get("taxes_annuelles", 0)
        interets_annuels = donnees.get("interets_annuels", 0)
        charges_courantes_annuelles = donnees.get("charges_courantes_annuelles", 0)

        amortissements_totaux = 0
        for categorie, composants in amortissements_details[annee].items():
            for composant, details in composants.items():
                amortissements_totaux += details["valeur"] / details["duree"]

        charges_deductibles = (
            amortissements_totaux
            + taxes_annuelles
            + interets_annuels
            + charges_courantes_annuelles
        )

        resultat_imposable = loyers_annuels - charges_deductibles
        # Plafonnement de l'amortissement
        if amortissements_totaux > (
            loyers_annuels
            - (taxes_annuelles + interets_annuels + charges_courantes_annuelles)
        ):
            amortissements_totaux = loyers_annuels - (
                taxes_annuelles + interets_annuels + charges_courantes_annuelles
            )
            charges_deductibles = (
                amortissements_totaux
                + taxes_annuelles
                + interets_annuels
                + charges_courantes_annuelles
            )
            resultat_imposable = loyers_annuels - charges_deductibles

        impots = resultat_imposable * tranche_marginale_impots

        resultats_annuels[annee] = {
            "resultat_imposable": resultat_imposable,
            "impots": impots,
            "amortissements_totaux": amortissements_totaux,
        }

    return resultats_annuels


# Exemple d'utilisation
data_file = "data.csv"
amortissements_file = "amortissements.csv"
resultats = calculer_resultat_lmnp_annuel(data_file, amortissements_file)
for annee, resultat in resultats.items():
    print(
        f"Résultat imposable en LMNP pour {annee} : {resultat['resultat_imposable']} €"
    )
    print(f"Impôts estimés pour {annee}: {resultat['impots']} €")
    print(f"Amortissements totaux pour {annee}: {resultat['amortissements_totaux']} €")
