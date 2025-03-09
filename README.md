# Simulateur LMNP Régime Réel

Ce dépôt contient un script Python pour simuler le calcul du résultat imposable en LMNP au régime réel.

## Utilisation

1.  Assurez-vous d'avoir Python installé.
2.  Créez un fichier `expenses.csv` avec vos dépenses (catégorie, montant, date).
3.  Exécutez le script `lmnp_simulator.py`.

## Dépendances

* Python 3.6+

## Personnalisation

* Modifiez le fichier `expenses.csv` pour refléter vos propres dépenses.
* Ajustez la variable `revenus_locatifs` dans le script.
* Pour la prise en compte des amortissements, il faudrait rajouter une colonne dans le fichier *expenses.csv*, et rajouter le calcul de l'ammortissement dans la fonction *calculer\_resultat\_lmnp*.