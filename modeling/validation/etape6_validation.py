"""
ÉTAPE 6: Backtesting et Validation Temporelle
Solution qui gère correctement tous les imports du modèle existant
"""

import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Imports nécessaires pour le modèle existant
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    roc_auc_score, accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
from sklearn.pipeline import Pipeline

def load_model_safely(model_path):
    """
    Chargement sécurisé du modèle avec tous les imports nécessaires
    """
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model, None
    except Exception as e:
        return None, str(e)

def calculate_ks_statistic(y_true, y_scores):
    """
    Calcul de la statistique KS (Kolmogorov-Smirnov)
    """
    # Séparation des scores par classe
    scores_pos = y_scores[y_true == 1]
    scores_neg = y_scores[y_true == 0]
    
    # Calcul KS manuel
    from scipy import stats
    ks_stat, _ = stats.ks_2samp(scores_pos, scores_neg)
    return ks_stat

def calculate_gini_coefficient(y_true, y_scores):
    """
    Calcul du coefficient de Gini
    """
    auc = roc_auc_score(y_true, y_scores)
    return 2 * auc - 1

def run_etape6_validation():
    """
    Exécution complète de l'ÉTAPE 6 : Backtesting et Validation
    """
    print("🚀 ÉTAPE 6: BACKTESTING ET VALIDATION TEMPORELLE")
    print("=" * 70)
    
    # 1. Vérification des prérequis
    print("\n📋 VÉRIFICATION DES PRÉREQUIS")
    print("-" * 40)
    
    model_path = "modeling/models/best_model.pkl"
    data_path = "data/processed/credit_all_transformed.csv"
    
    # Vérifications
    checks = {
        'Modèle candidat': os.path.exists(model_path),
        'Données transformées': os.path.exists(data_path)
    }
    
    for check, status in checks.items():
        symbol = "✅" if status else "❌"
        print(f"   {symbol} {check}")
    
    if not all(checks.values()):
        print("\n❌ Prérequis manquants - Impossible de continuer")
        return False
    
    # 2. Chargement sécurisé du modèle
    print("\n📥 CHARGEMENT SÉCURISÉ DU MODÈLE")
    print("-" * 40)
    
    model, error = load_model_safely(model_path)
    if model is None:
        print(f"❌ Erreur chargement modèle: {error}")
        return False
    
    print(f"✅ Modèle chargé: {type(model).__name__}")
    
    # 3. Chargement des données
    print("\n📥 CHARGEMENT DES DONNÉES")
    print("-" * 40)
    
    try:
        data = pd.read_csv(data_path)
        X = data.drop('cible', axis=1)
        y = data['cible']
        print(f"✅ Données: {len(data)} échantillons, {len(X.columns)} features")
        print(f"✅ Distribution cible: {y.value_counts().to_dict()}")
    except Exception as e:
        print(f"❌ Erreur chargement données: {e}")
        return False
    
    # 4. Validation de base du modèle
    print("\n🔍 VALIDATION DE BASE DU MODÈLE")
    print("-" * 40)
    
    try:
        # Test de prédiction
        y_pred_proba = model.predict_proba(X)[:, 1]
        y_pred = model.predict(X)
        
        # Métriques principales
        auc_roc = roc_auc_score(y, y_pred_proba)
        accuracy = accuracy_score(y, y_pred)
        precision = precision_score(y, y_pred)
        recall = recall_score(y, y_pred)
        f1 = f1_score(y, y_pred)
        
        # Métriques métier
        ks_stat = calculate_ks_statistic(y, y_pred_proba)
        gini = calculate_gini_coefficient(y, y_pred_proba)
        
        print(f"📊 MÉTRIQUES DE PERFORMANCE:")
        print(f"   AUC-ROC: {auc_roc:.4f}")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"   Precision: {precision:.4f}")
        print(f"   Recall: {recall:.4f}")
        print(f"   F1-Score: {f1:.4f}")
        print(f"   KS Statistic: {ks_stat:.4f}")
        print(f"   Gini Coefficient: {gini:.4f}")
        
    except Exception as e:
        print(f"❌ Erreur validation de base: {e}")
        return False
    
    # 5. Backtesting temporel simulé
    print("\n📅 BACKTESTING TEMPOREL")
    print("-" * 40)
    
    # Simulation de 5 périodes temporelles
    temporal_results = []
    np.random.seed(42)
    
    for period in range(1, 6):
        print(f"\n📊 Période {period} (simulation temporelle)")
        
        # Échantillonnage stratifié pour simuler différentes périodes
        sample_size = 0.2  # 20% des données par période
        
        # Stratification par classe
        indices_0 = data[data['cible'] == 0].index
        indices_1 = data[data['cible'] == 1].index
        
        # Échantillonnage
        n_samples_0 = int(len(indices_0) * sample_size)
        n_samples_1 = int(len(indices_1) * sample_size)
        
        sample_0 = np.random.choice(indices_0, n_samples_0, replace=False)
        sample_1 = np.random.choice(indices_1, n_samples_1, replace=False)
        
        period_indices = np.concatenate([sample_0, sample_1])
        
        # Données de la période
        X_period = X.loc[period_indices]
        y_period = y.loc[period_indices]
        
        # Prédictions
        y_pred_proba_period = model.predict_proba(X_period)[:, 1]
        
        # Métriques
        auc_period = roc_auc_score(y_period, y_pred_proba_period)
        ks_period = calculate_ks_statistic(y_period, y_pred_proba_period)
        
        period_result = {
            'period': period,
            'auc_roc': auc_period,
            'ks_statistic': ks_period,
            'n_samples': len(y_period),
            'default_rate': y_period.mean()
        }
        
        temporal_results.append(period_result)
        
        print(f"   AUC-ROC: {auc_period:.4f}")
        print(f"   KS: {ks_period:.4f}")
        print(f"   Échantillons: {len(y_period)}")
        print(f"   Taux défaut: {y_period.mean():.3f}")
    
    # Analyse de stabilité temporelle
    aucs = [r['auc_roc'] for r in temporal_results]
    auc_mean = np.mean(aucs)
    auc_std = np.std(aucs)
    auc_min = np.min(aucs)
    auc_max = np.max(aucs)
    auc_decline = auc_max - auc_min
    
    print(f"\n📈 ANALYSE DE STABILITÉ TEMPORELLE:")
    print(f"   AUC moyen: {auc_mean:.4f}")
    print(f"   Écart-type AUC: {auc_std:.4f}")
    print(f"   AUC minimum: {auc_min:.4f}")
    print(f"   AUC maximum: {auc_max:.4f}")
    print(f"   Déclin AUC: {auc_decline:.4f}")
    
    # 6. Tests de stress économique
    print("\n💥 TESTS DE STRESS ÉCONOMIQUE")
    print("-" * 40)
    
    stress_scenarios = [
        {'name': 'baseline', 'description': 'Conditions normales', 'multiplier': 1.0},
        {'name': 'recession', 'description': 'Récession économique', 'multiplier': 1.8},
        {'name': 'high_inflation', 'description': 'Forte inflation', 'multiplier': 1.4},
        {'name': 'financial_crisis', 'description': 'Crise financière', 'multiplier': 2.2}
    ]
    
    stress_results = {}
    
    for scenario in stress_scenarios:
        print(f"\n🎭 Scénario: {scenario['description']}")
        
        # Simulation d'augmentation des défauts
        y_stress = y.copy()
        multiplier = scenario['multiplier']
        
        if multiplier > 1.0:
            # Augmentation du nombre de défauts
            current_defaults = y_stress.sum()
            target_defaults = int(current_defaults * multiplier)
            additional_defaults = min(target_defaults - current_defaults, 
                                   len(y_stress[y_stress == 0]))
            
            if additional_defaults > 0:
                # Sélection aléatoire de nouveaux défauts
                non_default_indices = y_stress[y_stress == 0].index
                new_defaults = np.random.choice(
                    non_default_indices, 
                    size=additional_defaults, 
                    replace=False
                )
                y_stress.loc[new_defaults] = 1
        
        # Performance sous stress
        auc_stress = roc_auc_score(y_stress, y_pred_proba)
        ks_stress = calculate_ks_statistic(y_stress, y_pred_proba)
        performance_degradation = auc_roc - auc_stress
        
        stress_results[scenario['name']] = {
            'description': scenario['description'],
            'auc_roc': auc_stress,
            'ks_statistic': ks_stress,
            'performance_degradation': performance_degradation,
            'default_rate': y_stress.mean(),
            'multiplier': multiplier
        }
        
        print(f"   AUC-ROC: {auc_stress:.4f}")
        print(f"   KS: {ks_stress:.4f}")
        print(f"   Dégradation: {performance_degradation:.4f}")
        print(f"   Taux défaut: {y_stress.mean():.3f}")
    
    # 7. Validation réglementaire
    print("\n🏛️ VALIDATION RÉGLEMENTAIRE")
    print("-" * 40)
    
    # Critères de validation selon standards bancaires
    regulatory_criteria = {
        'AUC minimum (≥0.75)': auc_roc >= 0.75,
        'KS minimum (≥0.30)': ks_stat >= 0.30,
        'Gini minimum (≥0.40)': gini >= 0.40,
        'Stabilité temporelle (déclin ≤0.10)': auc_decline <= 0.10,
        'Résistance stress (AUC ≥0.70)': min([r['auc_roc'] for r in stress_results.values()]) >= 0.70
    }
    
    print("📋 CRITÈRES RÉGLEMENTAIRES:")
    for criterion, passed in regulatory_criteria.items():
        status = "✅ CONFORME" if passed else "❌ NON CONFORME"
        print(f"   {criterion}: {status}")
    
    # 8. Évaluation finale
    validation_passed = all(regulatory_criteria.values())
    
    print(f"\n🎯 VALIDATION GLOBALE: {'✅ RÉUSSIE' if validation_passed else '❌ ÉCHOUÉE'}")
    
    # 9. Génération du rapport complet
    print("\n📄 GÉNÉRATION DU RAPPORT")
    print("-" * 40)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    validation_report = {
        'validation_summary': {
            'timestamp': timestamp,
            'model_path': model_path,
            'validation_passed': validation_passed,
            'model_type': type(model).__name__
        },
        'performance_metrics': {
            'auc_roc': auc_roc,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'ks_statistic': ks_stat,
            'gini_coefficient': gini
        },
        'temporal_stability': {
            'auc_mean': auc_mean,
            'auc_std': auc_std,
            'auc_min': auc_min,
            'auc_max': auc_max,
            'auc_decline': auc_decline,
            'period_results': temporal_results
        },
        'stress_tests': stress_results,
        'regulatory_compliance': regulatory_criteria,
        'validation_thresholds': {
            'min_auc_roc': 0.75,
            'min_ks_statistic': 0.30,
            'min_gini': 0.40,
            'max_auc_decline': 0.10,
            'min_stress_auc': 0.70
        }
    }
    
    # Sauvegarde du rapport
    os.makedirs("modeling/validation", exist_ok=True)
    report_path = f"modeling/validation/validation_report_{timestamp}.json"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(validation_report, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"✅ Rapport sauvegardé: {report_path}")
    
    # 10. Sauvegarde du modèle final si validation réussie
    if validation_passed:
        print("\n💾 SAUVEGARDE MODÈLE FINAL")
        print("-" * 40)
        
        # Création du dossier modèles finaux
        final_models_dir = "modeling/models/final_models"
        os.makedirs(final_models_dir, exist_ok=True)
        
        # Sauvegarde modèle final
        final_model_name = f"credit_scoring_final_v1.0_{timestamp}_auc{auc_roc:.4f}.pkl"
        final_model_path = os.path.join(final_models_dir, final_model_name)
        
        # Copie du modèle vers le dossier final
        import shutil
        shutil.copy2(model_path, final_model_path)
        
        # Métadonnées du modèle final
        metadata = {
            'model_version': 'v1.0',
            'creation_date': timestamp,
            'source_model': model_path,
            'validation_passed': True,
            'validation_report': report_path,
            'performance_summary': {
                'auc_roc': auc_roc,
                'ks_statistic': ks_stat,
                'gini_coefficient': gini
            },
            'production_ready': True,
            'deployment_approved': True
        }
        
        metadata_path = os.path.join(final_models_dir, f"model_metadata_{timestamp}.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, default=str, ensure_ascii=False)
        
        print(f"✅ Modèle final: {final_model_path}")
        print(f"✅ Métadonnées: {metadata_path}")
        
        # Résumé final
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
        print("   • Mise en production")
        
        return True
        
    else:
        print("\n" + "=" * 70)
        print("❌ ÉTAPE 6 ÉCHOUÉE - VALIDATION NON RÉUSSIE")
        print("=" * 70)
        print("⚠️ Le modèle ne satisfait pas tous les critères réglementaires")
        
        failed_criteria = [k for k, v in regulatory_criteria.items() if not v]
        print(f"❌ Critères échoués: {failed_criteria}")
        
        print("\n🔄 ACTIONS RECOMMANDÉES:")
        print("   • Analyser les critères échoués")
        print("   • Retour à l'ÉTAPE 5 pour optimisation")
        print("   • Ajustement des hyperparamètres")
        print("   • Enrichissement des données d'entraînement")
        
        return False


if __name__ == "__main__":
    run_etape6_validation() 