# Trad — Pipeline de traduction FR → EN

Pipeline de traduction automatique français → anglais utilisant le modèle HuggingFace `Helsinki-NLP/opus-mt-fr-en`, avec évaluation de la qualité (BLEU, chrF).

## Structure du projet

```
src/
├── loaders/         # Chargement des données (CSV, JSON)
├── processors/      # Nettoyage et prétraitement
├── translators/     # Traduction via HuggingFace
├── evaluators/      # Évaluation (BLEU, chrF)
├── orchestrator/    # Coordination du pipeline
├── config.py        # Chemins (data/, output/)
└── main.py          # Point d'entrée
data/                # Fichiers source à traduire
output/              # Résultats traduits
tests/
```

## Installation

```bash
conda install pytorch -c pytorch
pip install -r requirements.txt
```

## Utilisation

```bash
python src/main.py
```

Le pipeline charge `data/sample02.json`, traduit la colonne `source`, sauvegarde le résultat dans `output/translated.csv` et affiche les scores de qualité.

## Auteur

billal
# outil_traduction
