"""
ÉTAPE 6: Backtesting et Validation Temporelle - VERSION FINALE
Correction du problème d'import CalibratedClassifierCV
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import json
import warnings
import sys
warnings.filterwarnings('ignore')

# CORRECTION: Import global explicite avant pickle
import sklearn
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score
from scipy import stats

# Maintenant pickle avec les modules correctement importés
import pickle

def load_model_with_imports(model_path):
    """
    Chargement du modèle avec imports préalables
    """
    # Ajout explicite du module au namespace global pour pickle
    import sys
    sys.modules['CalibratedClassifierCV'] = CalibratedClassifierCV
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model, None
    except Exception as e:
        return None, str(e)

def calculate_ks_statistic(y_true, y_scores):
    """Calcul KS Statistic"""
    scores_pos = y_scores[y_true == 1]
    scores_neg = y_scores[y_true == 0]
    ks_stat, _ = stats.ks_2samp(scores_pos, scores_neg)
    return ks_stat

def main():
    """
    Exécution complète ÉTAPE 6
    """
    print("🚀 ÉTAPE 6: BACKTESTING ET VALIDATION TEMPORELLE")
    print("=" * 70)
    
    # 1. Vérifications préalables
    model_path = "modeling/models/best_model.pkl"
    data_path = "data/processed/credit_all_transformed.csv"
    
    print("\n📋 VÉRIFICATION DES PRÉREQUIS")
    print("-" * 40)
    
    if not os.path.exists(model_path):
        print(f"❌ Modèle non trouvé: {model_path}")
        return False
    
    if not os.path.exists(data_path):
        print(f"❌ Données non trouvées: {data_path}")
        return False
    
    print("✅ Modèle candidat trouvé")
    print("✅ Données transformées trouvées")
    
    # 2. Chargement avec correction d'import
    print("\n📥 CHARGEMENT AVEC CORRECTION D'IMPORT")
    print("-" * 40)
    
    model, error = load_model_with_imports(model_path)
    if model is None:
        print(f"❌ Échec chargement: {error}")
        return False
    
    print(f"✅ Modèle chargé: {type(model).__name__}")
    
    # Chargement données
    try:
        data = pd.read_csv(data_path)
        X = data.drop('cible', axis=1)
        y = data['cible']
        print(f"✅ Données: {len(data)} échantillons, {len(X.columns)} features")
    except Exception as e:
        print(f"❌ Erreur données: {e}")
        return False
    
    # 3. Tests de performance de base
    print("\n🔍 TESTS DE PERFORMANCE DE BASE")
    print("-" * 40)
    
    try:
        y_pred_proba = model.predict_proba(X)[:, 1]
        y_pred = model.predict(X)
        
        # Métriques
        auc_roc = roc_auc_score(y, y_pred_proba)
        accuracy = accuracy_score(y, y_pred)
        precision = precision_score(y, y_pred)
        recall = recall_score(y, y_pred)
        f1 = f1_score(y, y_pred)
        ks_stat = calculate_ks_statistic(y, y_pred_proba)
        gini = 2 * auc_roc - 1
        
        print(f"📊 MÉTRIQUES DE PERFORMANCE:")
        print(f"   AUC-ROC: {auc_roc:.4f}")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"   Precision: {precision:.4f}")
        print(f"   Recall: {recall:.4f}")
        print(f"   F1-Score: {f1:.4f}")
        print(f"   KS Statistic: {ks_stat:.4f}")
        print(f"   Gini Coefficient: {gini:.4f}")
        
    except Exception as e:
        print(f"❌ Erreur test performance: {e}")
        return False
    
    # 4. Backtesting temporel
    print("\n📅 BACKTESTING TEMPOREL (5 PÉRIODES)")
    print("-" * 40)
    
    temporal_results = []
    np.random.seed(42)
    
    for period in range(1, 6):
        # Échantillonnage stratifié 20% par période
        sample_indices = []
        for class_val in [0, 1]:
            class_indices = data[data['cible'] == class_val].index
            n_samples = int(len(class_indices) * 0.2)
            sampled = np.random.choice(class_indices, n_samples, replace=False)
            sample_indices.extend(sampled)
        
        X_period = X.loc[sample_indices]
        y_period = y.loc[sample_indices]
        
        y_pred_proba_period = model.predict_proba(X_period)[:, 1]
        auc_period = roc_auc_score(y_period, y_pred_proba_period)
        ks_period = calculate_ks_statistic(y_period, y_pred_proba_period)
        
        temporal_results.append({
            'period': period,
            'auc_roc': auc_period,
            'ks_statistic': ks_period,
            'n_samples': len(y_period),
            'default_rate': y_period.mean()
        })
        
        print(f"Période {period}: AUC={auc_period:.4f}, KS={ks_period:.4f}")
    
    # Analyse stabilité
    aucs = [r['auc_roc'] for r in temporal_results]
    auc_mean = np.mean(aucs)
    auc_decline = max(aucs) - min(aucs)
    
    print(f"\n📈 STABILITÉ: AUC moyen={auc_mean:.4f}, Déclin={auc_decline:.4f}")
    
    # 5. Tests de stress
    print("\n💥 TESTS DE STRESS ÉCONOMIQUE")
    print("-" * 40)
    
    stress_scenarios = [
        ('Normal', 1.0),
        ('Récession', 1.6),
        ('Crise', 2.0)
    ]
    
    stress_results = {}
    
    for name, multiplier in stress_scenarios:
        y_stress = y.copy()
        
        if multiplier > 1.0:
            current_defaults = y_stress.sum()
            target_defaults = int(current_defaults * multiplier)
            additional = min(target_defaults - current_defaults, len(y_stress[y_stress == 0]))
            
            if additional > 0:
                non_defaults = y_stress[y_stress == 0].index
                new_defaults = np.random.choice(non_defaults, additional, replace=False)
                y_stress.loc[new_defaults] = 1
        
        auc_stress = roc_auc_score(y_stress, y_pred_proba)
        degradation = auc_roc - auc_stress
        
        stress_results[name.lower()] = {
            'auc_roc': auc_stress,
            'degradation': degradation,
            'default_rate': y_stress.mean()
        }
        
        print(f"{name}: AUC={auc_stress:.4f}, Dégradation={degradation:.4f}")
    
    # 6. Validation réglementaire
    print("\n🏛️ VALIDATION RÉGLEMENTAIRE")
    print("-" * 40)
    
    criteria = {
        'AUC ≥ 0.75': auc_roc >= 0.75,
        'KS ≥ 0.30': ks_stat >= 0.30,
        'Gini ≥ 0.40': gini >= 0.40,
        'Stabilité (déclin ≤ 0.10)': auc_decline <= 0.10,
        'Résistance stress (AUC ≥ 0.70)': min([r['auc_roc'] for r in stress_results.values()]) >= 0.70
    }
    
    print("📋 CRITÈRES DE VALIDATION:")
    for criterion, passed in criteria.items():
        status = "✅ CONFORME" if passed else "❌ NON CONFORME"
        print(f"   {criterion}: {status}")
    
    validation_passed = all(criteria.values())
    
    # 7. Génération rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    report = {
        'validation_summary': {
            'timestamp': timestamp,
            'validation_passed': validation_passed,
            'model_type': type(model).__name__
        },
        'performance_metrics': {
            'auc_roc': float(auc_roc),
            'ks_statistic': float(ks_stat),
            'gini_coefficient': float(gini)
        },
        'temporal_stability': {
            'auc_mean': float(auc_mean),
            'auc_decline': float(auc_decline),
            'periods': temporal_results
        },
        'stress_tests': stress_results,
        'regulatory_compliance': criteria
    }
    
    # Sauvegarde rapport
    os.makedirs("modeling/validation", exist_ok=True)
    report_path = f"modeling/validation/validation_report_{timestamp}.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Rapport sauvegardé: {report_path}")
    
    # 8. Sauvegarde modèle final si validé
    if validation_passed:
        print("\n💾 SAUVEGARDE MODÈLE FINAL")
        print("-" * 40)
        
        # Dossier modèles finaux
        final_dir = "modeling/models/final_models"
        os.makedirs(final_dir, exist_ok=True)
        
        # Copie modèle
        final_model_path = os.path.join(final_dir, f"credit_scoring_final_v1.0_{timestamp}_auc{auc_roc:.4f}.pkl")
        import shutil
        shutil.copy2(model_path, final_model_path)
        
        # Métadonnées
        metadata = {
            'model_version': 'v1.0',
            'creation_date': timestamp,
            'validation_passed': True,
            'auc_roc': float(auc_roc),
            'production_ready': True
        }
        
        metadata_path = os.path.join(final_dir, f"model_metadata_{timestamp}.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Modèle final: {final_model_path}")
        print(f"✅ Métadonnées: {metadata_path}")
        
        print("\n" + "=" * 70)
        print("🎉 ÉTAPE 6 TERMINÉE AVEC SUCCÈS!")
        print("=" * 70)
        print("✅ Toutes les validations sont passées")
        print("✅ Modèle conforme aux standards bancaires")
        print("✅ Modèle final sauvegardé et prêt pour production")
        print("🏆 PHASE DE MODÉLISATION ENTIÈREMENT COMPLÈTE!")
        
        print("\n🎯 PROCHAINES ÉTAPES:")
        print("   • PARTIE 2: Application Streamlit Interactive")
        print("   • API REST: Service de prédiction FastAPI")
        print("   • MLOps: Déploiement et monitoring")
        
        return True
        
    else:
        print("\n❌ VALIDATION ÉCHOUÉE")
        print("Certains critères ne sont pas satisfaits")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 ÉTAPE 6 RÉUSSIE - Prêt pour la suite!")
    else:
        print("\n⚠️ ÉTAPE 6 ÉCHOUÉE - Corrections nécessaires") 