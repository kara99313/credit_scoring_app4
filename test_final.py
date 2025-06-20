#!/usr/bin/env python3
"""
Test final des analyses EDA - Version stable
Système de crédit scoring
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

# Configuration matplotlib pour éviter les problèmes
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif

def main():
    print("🚀 ANALYSES EDA AVANCÉES - VERSION FINALE")
    print("=" * 60)
    
    try:
        # 1. Chargement des données
        print("\n📊 1. CHARGEMENT DES DONNÉES")
        data_path = "data/processed/credit_cleaned.csv"
        data = pd.read_csv(data_path)
        print(f"✅ {len(data)} clients, {len(data.columns)} variables")
        
        # 2. Analyses de base
        print("\n🔍 2. ANALYSES DE BASE")
        
        # Variables numériques vs cible
        print("📈 Variables numériques vs cible :")
        numeric_cols = ['duree', 'montant', 'age']
        for col in numeric_cols:
            stats = data.groupby('cible')[col].agg(['mean', 'std', 'median'])
            means = stats['mean']
            diff_pct = abs((means.iloc[0] - means.iloc[1]) / means.mean()) * 100
            print(f"   • {col.upper()}: {diff_pct:.0f}% d'écart entre groupes")
        
        # Variables catégorielles les plus discriminantes
        print("\n📋 Variables catégorielles les plus discriminantes :")
        categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
        categorical_cols.remove('cible')
        
        discriminant_vars = []
        for col in categorical_cols[:10]:  # Top 10 seulement
            crosstab = pd.crosstab(data[col], data['cible'], normalize='index') * 100
            if len(crosstab.columns) >= 2:
                max_diff = crosstab.max(axis=1) - crosstab.min(axis=1)
                avg_diff = max_diff.mean()
                discriminant_vars.append((col, avg_diff))
                print(f"   • {col.upper()}: {avg_diff:.0f}% d'écart moyen")
        
        # 3. NOUVELLE ANALYSE : Information mutuelle
        print("\n🧠 3. INFORMATION MUTUELLE (NOUVEAU)")
        
        try:
            from sklearn.feature_selection import mutual_info_classif
            from sklearn.preprocessing import LabelEncoder
            
            # Préparer les données
            features_data = data.copy()
            
            # Encoder toutes les variables catégorielles
            for col in features_data.select_dtypes(include=['object']).columns:
                le = LabelEncoder()
                features_data[col] = le.fit_transform(features_data[col].astype(str))
            
            # Séparer features et target
            X = features_data.drop('cible', axis=1)
            y = features_data['cible']
            
            # Calculer l'information mutuelle
            mi_scores = mutual_info_classif(X, y, random_state=42)
            
            # Créer un DataFrame des scores
            mi_df = pd.DataFrame({
                'Variable': X.columns,
                'Mutual_Information': mi_scores
            }).sort_values('Mutual_Information', ascending=False)
            
            print("🎯 Variables classées par importance (Information Mutuelle) :")
            for i, (_, row) in enumerate(mi_df.head(10).iterrows()):
                print(f"   {i+1}. {row['Variable']}: {row['Mutual_Information']:.4f}")
            
            # Visualisation
            plt.figure(figsize=(12, 8))
            top_15 = mi_df.head(15)
            plt.barh(range(len(top_15)), top_15['Mutual_Information'], color='purple', alpha=0.7)
            plt.yticks(range(len(top_15)), top_15['Variable'])
            plt.xlabel('Information Mutuelle')
            plt.title('INFORMATION MUTUELLE AVEC LA VARIABLE CIBLE', fontweight='bold')
            plt.gca().invert_yaxis()
            
            # Créer le dossier s'il n'existe pas
            os.makedirs('reports/eda', exist_ok=True)
            
            plt.tight_layout()
            plt.savefig('reports/eda/information_mutuelle_finale.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("✅ Graphique information mutuelle sauvegardé")
            
        except ImportError:
            print("❌ sklearn non disponible pour l'information mutuelle")
        
        # 4. NOUVELLE ANALYSE : Segmentation par risque simple
        print("\n📊 4. SEGMENTATION PAR RISQUE (NOUVEAU)")
        
        # Score de risque basé sur les variables numériques
        risk_score = 0
        for col in numeric_cols:
            normalized = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
            if col == 'duree':
                risk_score += normalized * 0.4
            elif col == 'montant':
                risk_score += normalized * 0.4
            elif col == 'age':
                risk_score += (1 - normalized) * 0.2
        
        # Créer des quartiles de risque
        data['risk_quartile'] = pd.qcut(risk_score, 4, labels=['Q1_Faible', 'Q2_Moyen', 'Q3_Élevé', 'Q4_Très_Élevé'])
        
        print("🎯 Analyse par quartile de risque :")
        for quartile in ['Q1_Faible', 'Q2_Moyen', 'Q3_Élevé', 'Q4_Très_Élevé']:
            quartile_data = data[data['risk_quartile'] == quartile]
            if len(quartile_data) > 0:
                default_rate = len(quartile_data[quartile_data['cible'] == 'credit avec impaye'])/len(quartile_data)*100
                avg_amount = quartile_data['montant'].mean()
                print(f"   • {quartile}: {default_rate:.1f}% de défaut, {avg_amount:.0f}€ moyen")
        
        # 5. NOUVELLE ANALYSE : Détection d'outliers
        print("\n🔍 5. DÉTECTION D'OUTLIERS (NOUVEAU)")
        
        for col in numeric_cols:
            data_col = data[col].dropna()
            
            # Méthode IQR
            Q1 = data_col.quantile(0.25)
            Q3 = data_col.quantile(0.75)
            IQR = Q3 - Q1
            iqr_outliers = data_col[(data_col < Q1 - 1.5*IQR) | (data_col > Q3 + 1.5*IQR)]
            
            # Méthode Z-score
            z_scores = np.abs((data_col - data_col.mean()) / data_col.std())
            zscore_outliers = data_col[z_scores > 3]
            
            print(f"   • {col.upper()}:")
            print(f"     - IQR: {len(iqr_outliers)} outliers ({len(iqr_outliers)/len(data_col)*100:.1f}%)")
            print(f"     - Z-score: {len(zscore_outliers)} outliers ({len(zscore_outliers)/len(data_col)*100:.1f}%)")
        
        # 6. Génération du rapport final
        print("\n📋 6. GÉNÉRATION DU RAPPORT FINAL")
        
        # Rapport JSON avec toutes les analyses
        final_report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'dataset_info': {
                'n_clients': len(data),
                'n_variables': len(data.columns),
                'target_distribution': data['cible'].value_counts().to_dict()
            },
            'numeric_analysis': {
                col: {
                    'mean_good': float(data[data['cible'] == 'credit bien rembourse'][col].mean()),
                    'mean_bad': float(data[data['cible'] == 'credit avec impaye'][col].mean()),
                    'difference_pct': float(abs((data[data['cible'] == 'credit bien rembourse'][col].mean() - 
                                               data[data['cible'] == 'credit avec impaye'][col].mean()) / 
                                              data[col].mean()) * 100)
                } for col in numeric_cols
            },
            'categorical_discrimination': dict(discriminant_vars[:10]),
            'mutual_information': mi_df.head(10).to_dict('records') if 'mi_df' in locals() else {},
            'risk_segmentation': {
                quartile: {
                    'size': int(len(data[data['risk_quartile'] == quartile])),
                    'default_rate': float(len(data[(data['risk_quartile'] == quartile) & 
                                                  (data['cible'] == 'credit avec impaye')])/len(data[data['risk_quartile'] == quartile])*100)
                } for quartile in ['Q1_Faible', 'Q2_Moyen', 'Q3_Élevé', 'Q4_Très_Élevé']
            }
        }
        
        # Sauvegarder le rapport
        with open('reports/eda/rapport_final_avance.json', 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        print("✅ Rapport final sauvegardé : reports/eda/rapport_final_avance.json")
        
        # 7. Résumé des découvertes
        print("\n🎉 ANALYSES TERMINÉES - DÉCOUVERTES CLÉS :")
        print("\n🔥 Variables les plus discriminantes :")
        
        # Top 3 numériques
        numeric_importance = [(col, final_report['numeric_analysis'][col]['difference_pct']) 
                             for col in numeric_cols]
        numeric_importance.sort(key=lambda x: x[1], reverse=True)
        
        for i, (var, diff) in enumerate(numeric_importance[:3]):
            print(f"   {i+1}. {var.upper()}: {diff:.0f}% d'écart")
        
        # Top 3 catégorielles
        for i, (var, diff) in enumerate(discriminant_vars[:3]):
            print(f"   {i+4}. {var.upper()}: {diff:.0f}% d'écart moyen")
        
        print(f"\n📊 Segmentation par risque :")
        print(f"   • Quartile le moins risqué: {final_report['risk_segmentation']['Q1_Faible']['default_rate']:.1f}% défaut")
        print(f"   • Quartile le plus risqué: {final_report['risk_segmentation']['Q4_Très_Élevé']['default_rate']:.1f}% défaut")
        
        print(f"\n📁 Tous les résultats dans : reports/eda/")
        print(f"🚀 Prêt pour l'étape 3 : Feature Engineering !")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR : {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 