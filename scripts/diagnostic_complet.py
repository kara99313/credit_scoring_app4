import pandas as pd
import numpy as np

print("🔍 DIAGNOSTIC COMPLET DES DONNÉES")
print("=" * 60)

# Charger les données
df = pd.read_csv('data/raw/credit.csv')

print(f"📊 RÉSUMÉ : {len(df)} clients, {len(df.columns)} colonnes\n")

# ===============================
# 1. VALEURS MANQUANTES
# ===============================
print("🕳️  1. VALEURS MANQUANTES")
print("-" * 30)
missing = df.isnull().sum()
if missing.sum() == 0:
    print("✅ Aucune donnée manquante !")
else:
    print("⚠️ Valeurs manquantes trouvées :")
    for col, count in missing[missing > 0].items():
        percentage = (count / len(df)) * 100
        print(f"   • {col}: {count} ({percentage:.1f}%)")

# ===============================
# 2. DOUBLONS
# ===============================
print(f"\n📋 2. DOUBLONS")
print("-" * 30)
doublons_total = df.duplicated().sum()
if doublons_total == 0:
    print("✅ Aucun doublon trouvé !")
else:
    print(f"⚠️ {doublons_total} doublons trouvés")
    print("Exemple de doublons :")
    print(df[df.duplicated()].head())

# ===============================
# 3. VALEURS ABERRANTES - Variables numériques
# ===============================
print(f"\n📈 3. VALEURS ABERRANTES (Variables numériques)")
print("-" * 30)

# Variables numériques
numeric_cols = ['duree', 'montant', 'age']

for col in numeric_cols:
    if col in df.columns:
        # Ignorer les valeurs manquantes pour le calcul
        data = df[col].dropna()
        
        if len(data) > 0:
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data < lower_bound) | (data > upper_bound)]
            
            print(f"\n   • {col.upper()}:")
            print(f"     Min: {data.min():.1f} | Max: {data.max():.1f}")
            print(f"     Médiane: {data.median():.1f} | Moyenne: {data.mean():.1f}")
            
            if len(outliers) > 0:
                print(f"     ⚠️ {len(outliers)} valeurs aberrantes détectées")
                print(f"     Plage normale: {lower_bound:.1f} à {upper_bound:.1f}")
                print(f"     Valeurs aberrantes: {sorted(outliers.tolist())}")
            else:
                print("     ✅ Aucune valeur aberrante")

# ===============================
# 4. COHÉRENCE DES DONNÉES
# ===============================
print(f"\n🔍 4. COHÉRENCE DES DONNÉES")
print("-" * 30)

# Vérifications de cohérence
problemes = []

# Âge cohérent ?
if 'age' in df.columns:
    ages_negatifs = df[df['age'] < 0]['age'].count() if not df[df['age'] < 0].empty else 0
    ages_trop_eleves = df[df['age'] > 100]['age'].count() if not df[df['age'] > 100].empty else 0
    
    if ages_negatifs > 0:
        problemes.append(f"Âges négatifs: {ages_negatifs}")
    if ages_trop_eleves > 0:
        problemes.append(f"Âges > 100 ans: {ages_trop_eleves}")

# Montant cohérent ?
if 'montant' in df.columns:
    montants_negatifs = df[df['montant'] <= 0]['montant'].count() if not df[df['montant'] <= 0].empty else 0
    
    if montants_negatifs > 0:
        problemes.append(f"Montants <= 0: {montants_negatifs}")

# Durée cohérente ?
if 'duree' in df.columns:
    durees_negatives = df[df['duree'] <= 0]['duree'].count() if not df[df['duree'] <= 0].empty else 0
    
    if durees_negatives > 0:
        problemes.append(f"Durées <= 0: {durees_negatives}")

if len(problemes) == 0:
    print("✅ Données cohérentes !")
else:
    print("⚠️ Problèmes de cohérence trouvés :")
    for probleme in problemes:
        print(f"   • {probleme}")

# ===============================
# 5. RÉSUMÉ FINAL
# ===============================
print(f"\n📋 5. RÉSUMÉ FINAL")
print("-" * 30)
total_problemes = missing.sum() + doublons_total + len(problemes)

if total_problemes == 0:
    print("🎉 Données parfaites ! Prêtes pour l'analyse.")
else:
    print(f"📝 Actions à effectuer :")
    print(f"   • Corriger {missing.sum()} valeurs manquantes")
    print(f"   • Supprimer {doublons_total} doublons")
    print(f"   • Traiter les valeurs aberrantes")
    print(f"   • Résoudre {len(problemes)} problèmes de cohérence") 