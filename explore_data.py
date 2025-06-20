import pandas as pd

print("🔍 ANALYSE DES DONNÉES CRÉDIT")
print("=" * 50)

# Charger les données
df = pd.read_csv('data/raw/credit.csv')

print(f"📊 Nombre de clients dans le fichier : {len(df)}")
print(f"📋 Nombre d'informations par client : {len(df.columns)}")

print("\n📝 LISTE DES INFORMATIONS DISPONIBLES :")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

print("\n👥 EXEMPLE DE 3 PREMIERS CLIENTS :")
print(df.head(3).to_string())

print("\n📈 TYPES D'INFORMATIONS :")
print(df.dtypes)

print("\n🎯 Y A-T-IL DES DONNÉES MANQUANTES ?")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("✅ Aucune donnée manquante !")
else:
    print("⚠️ Données manquantes trouvées :")
    print(missing[missing > 0]) 