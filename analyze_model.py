"""
Analyse complète du modèle entraîné - Finalisation Étape 1
"""

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def analyze_trained_model():
    """Analyse complète du modèle pour finaliser l'étape 1"""
    
    print('🔍 ANALYSE COMPLÈTE DU MODÈLE ENTRAÎNÉ')
    print('=' * 50)
    
    # 1. Chargement du modèle
    try:
        model = joblib.load('models/best_model.pkl')
        print('✅ Modèle chargé avec succès')
    except Exception as e:
        print(f'❌ Erreur chargement modèle: {e}')
        return
    
    # 2. Chargement des données
    try:
        data = pd.read_csv('data/processed/credit_engineered_transformed.csv')
        X = data.drop('cible', axis=1)
        y = data['cible']
        print(f'✅ Données chargées: {X.shape[0]} échantillons, {X.shape[1]} features')
    except Exception as e:
        print(f'❌ Erreur chargement données: {e}')
        return
    
    # 3. Prédictions
    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)[:, 1]
    print('✅ Prédictions générées')
    
    # 4. Matrice de confusion
    cm = confusion_matrix(y, y_pred)
    print('\n📊 MATRICE DE CONFUSION:')
    print('    Prédiction')
    print('Réel    0    1')
    print(f'  0   {cm[0,0]:3d}  {cm[0,1]:3d}')
    print(f'  1   {cm[1,0]:3d}  {cm[1,1]:3d}')
    
    # 5. Métriques détaillées
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred)
    recall = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    
    print('\n📈 MÉTRIQUES DÉTAILLÉES:')
    print(f'Accuracy:  {accuracy:.4f} ({accuracy*100:.1f}%)')
    print(f'Precision: {precision:.4f} ({precision*100:.1f}%)')
    print(f'Recall:    {recall:.4f} ({recall*100:.1f}%)')
    print(f'F1-Score:  {f1:.4f} ({f1*100:.1f}%)')
    
    # 6. Importance des features
    if hasattr(model, 'coef_'):
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': abs(model.coef_[0])
        }).sort_values('importance', ascending=False)
        
        print('\n🔍 TOP 10 FEATURES IMPORTANTES:')
        for i, (_, row) in enumerate(feature_importance.head(10).iterrows()):
            print(f'{i+1:2d}. {row["feature"]:30s} : {row["importance"]:.4f}')
        
        # Sauvegarde importance features
        feature_importance.to_csv('reports/feature_importance.csv', index=False)
        print('\n💾 Importance des features sauvegardée: reports/feature_importance.csv')
    
    # 7. Distribution des scores
    print('\n📊 DISTRIBUTION DES SCORES DE PRÉDICTION:')
    
    # Scores pour classe 0 (pas défaut)
    scores_0 = y_pred_proba[y == 0]
    scores_1 = y_pred_proba[y == 1]
    
    print(f'Classe 0 (Pas défaut): moyenne={scores_0.mean():.3f}, std={scores_0.std():.3f}')
    print(f'Classe 1 (Défaut):     moyenne={scores_1.mean():.3f}, std={scores_1.std():.3f}')
    
    # 8. Seuils de décision
    print('\n⚖️ ANALYSE DES SEUILS:')
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
    
    for threshold in thresholds:
        y_pred_thresh = (y_pred_proba >= threshold).astype(int)
        precision_thresh = precision_score(y, y_pred_thresh)
        recall_thresh = recall_score(y, y_pred_thresh)
        
        print(f'Seuil {threshold:.1f}: Precision={precision_thresh:.3f}, Recall={recall_thresh:.3f}')
    
    # 9. Résumé final
    print('\n' + '='*50)
    print('🎯 RÉSUMÉ - ÉTAPE 1 MODÉLISATION COMPLÉTÉE')
    print('='*50)
    print(f'✅ Modèle: Régression Logistique')
    print(f'✅ Performance globale: {accuracy*100:.1f}% accuracy')
    print(f'✅ Capacité de détection défauts: {recall*100:.1f}% recall')
    print(f'✅ Précision des prédictions: {precision*100:.1f}% precision')
    print(f'✅ Features les plus importantes identifiées')
    print(f'✅ Seuils de décision analysés')
    print('✅ ÉTAPE 1 MODÉLISATION: TERMINÉE !')
    print('\n🎯 PRÊT POUR ÉTAPE 2: APPLICATION & DÉPLOIEMENT')
    
if __name__ == "__main__":
    analyze_trained_model() 