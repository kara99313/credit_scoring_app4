#!/usr/bin/env python3
"""
Script de débogage pour identifier les problèmes de types de données
"""

import pandas as pd
import numpy as np

# Chargement des données
data = pd.read_csv("data/processed/credit_cleaned.csv")

print("🔍 ANALYSE DES TYPES DE DONNÉES")
print("=" * 40)

print(f"Shape des données: {data.shape}")
print("\nTypes de données:")
print(data.dtypes)

print("\n📊 ÉCHANTILLON DES DONNÉES:")
print(data.head())

print("\n🔢 VARIABLES NUMÉRIQUES:")
numerical_cols = data.select_dtypes(include=[np.number]).columns.tolist()
print(f"Colonnes numériques: {numerical_cols}")

print("\n📝 VARIABLES TEXTUELLES:")
text_cols = data.select_dtypes(include=['object']).columns.tolist()
print(f"Colonnes textuelles: {text_cols}")

print("\n🔍 ANALYSE SPÉCIFIQUE:")
print(f"Type de 'taux_endettement': {data['taux_endettement'].dtype}")
print(f"Valeurs uniques de 'taux_endettement': {data['taux_endettement'].unique()}")

print(f"\nType de 'montant': {data['montant'].dtype}")
print(f"Échantillon 'montant': {data['montant'].head()}")

print(f"\nType de 'age': {data['age'].dtype}")
print(f"Échantillon 'age': {data['age'].head()}")

# Test de conversion
print("\n🧪 TEST DE CONVERSION:")
try:
    taux_mapping = {
        'inferieur a 20%': 15,
        'compris entre 20% et 25%': 22.5,
        'compris entre 25% et 35%': 30,
        'superieur a 35%': 40
    }
    data['taux_endettement_num'] = data['taux_endettement'].map(taux_mapping).fillna(25)
    print(f"✅ Conversion réussie: {data['taux_endettement_num'].head()}")
    
    # Test de comparaison
    test_comparison = data['taux_endettement_num'] > 0
    print(f"✅ Comparaison réussie: {test_comparison.head()}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n✅ ANALYSE TERMINÉE") 