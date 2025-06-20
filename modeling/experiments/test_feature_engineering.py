#!/usr/bin/env python3
"""
Script de test pour valider le pipeline de Feature Engineering et Transformation
Teste les ÉTAPES 3 et 4 selon les spécifications PROJET_COMPLET_SPECIFICATION.md

Author: Credit Scoring Team
Created: 2024
"""

import sys
import os
from pathlib import Path

# Ajout du dossier src au path
sys.path.append(str(Path(__file__).parent / "src"))

import pandas as pd
import numpy as np
from src.data_processing import DataProcessor
from src.transformers.feature_engineer import FeatureEngineer
from src.transformers.variable_transformer import VariableTransformer


def test_feature_engineering_pipeline():
    """
    Test complet du pipeline de Feature Engineering selon l'ordre des spécifications :
    ÉTAPE 1-2: Chargement et nettoyage (DataProcessor)
    ÉTAPE 3: Feature Engineering Métier (FeatureEngineer)
    ÉTAPE 4: Transformation Variables (VariableTransformer)
    """
    
    print("🚀 TEST DU PIPELINE DE FEATURE ENGINEERING")
    print("=" * 60)
    
    # ÉTAPE 1-2: Chargement et nettoyage des données
    print("\n📊 ÉTAPE 1-2: CHARGEMENT ET NETTOYAGE DES DONNÉES")
    print("-" * 50)
    
    processor = DataProcessor()
    
    # Chargement des données
    data = processor.load_data("data/raw/credit.csv")
    if data is None:
        print("❌ Erreur: Impossible de charger les données")
        return False
    
    # Nettoyage des données
    cleaned_data = processor.clean_data()
    if cleaned_data is None:
        print("❌ Erreur: Impossible de nettoyer les données")
        return False
    
    print(f"✅ Données chargées et nettoyées: {cleaned_data.shape}")
    
    # ÉTAPE 3: Feature Engineering Métier
    print("\n🔧 ÉTAPE 3: FEATURE ENGINEERING MÉTIER")
    print("-" * 40)
    
    engineer = FeatureEngineer()
    
    # Pipeline complet de feature engineering
    try:
        engineered_data = engineer.engineer_all_features(cleaned_data)
        
        # Vérification des résultats
        feature_info = engineer.get_feature_info()
        
        print(f"\n📈 Résultats Feature Engineering:")
        print(f"   • Features originales: {len(feature_info.get('original_features', []))}")
        print(f"   • Features business: {len(feature_info.get('business_features', []))}")
        print(f"   • Features interaction: {len(feature_info.get('interaction_features', []))}")
        print(f"   • Features temporelles: {len(feature_info.get('temporal_features', []))}")
        print(f"   • Total features: {feature_info.get('total_features', 0)}")
        
    except Exception as e:
        print(f"❌ Erreur dans le Feature Engineering: {e}")
        return False
    
    # ÉTAPE 4: Transformation des Variables
    print("\n🔄 ÉTAPE 4: TRANSFORMATION DES VARIABLES")
    print("-" * 45)
    
    transformer = VariableTransformer()
    
    # Préparation de la variable cible
    target = engineered_data['cible'] if 'cible' in engineered_data.columns else None
    features_data = engineered_data.drop(columns=['cible']) if 'cible' in engineered_data.columns else engineered_data
    
    try:
        # ÉTAPE 4.1 + 4.2: Encodage et Scaling (SANS sélection)
        print("\n🔄 Phase 1: Encodage + Scaling (toutes les variables)")
        data_encoded = transformer.categorical_encoding(features_data, target, fit=True)
        data_encoded_scaled = transformer.numerical_scaling(data_encoded, fit=True)
        
        # Sauvegarde du fichier COMPLET transformé (AVANT sélection)
        if target is not None:
            complete_data = data_encoded_scaled.copy()
            complete_data['cible'] = target.reset_index(drop=True)
        else:
            complete_data = data_encoded_scaled
            
        complete_output_path = "data/processed/credit_all_transformed.csv"
        complete_data.to_csv(complete_output_path, index=False)
        print(f"💾 Fichier COMPLET sauvegardé: {complete_output_path}")
        print(f"   📊 Forme: {complete_data.shape} ({complete_data.shape[1]-1} features + cible)")
        
        # ÉTAPE 4.3: Sélection des features
        print("\n🎯 Phase 2: Sélection des meilleures features")
        transformed_data = transformer.feature_selection(data_encoded_scaled, target, fit=True)
        
        # Vérification des résultats
        transformation_info = transformer.get_transformation_info()
        
        print(f"\n📊 Résultats Transformation:")
        if 'categorical_encoding' in transformation_info:
            print(f"   • Variables catégorielles encodées: {len(transformation_info['categorical_encoding'])}")
        if 'numerical_scaling' in transformation_info:
            print(f"   • Variables numériques scalées: {len(transformation_info['numerical_scaling'].get('features_scaled', []))}")
        if 'feature_selection' in transformation_info:
            selection_info = transformation_info['feature_selection']
            print(f"   • Features sélectionnées: {selection_info.get('final_features', 0)}")
            print(f"   • Réduction features: {transformation_info.get('feature_reduction', 0)}")
        
    except Exception as e:
        print(f"❌ Erreur dans la Transformation: {e}")
        return False
    
    # RÉSUMÉ FINAL
    print("\n🎯 RÉSUMÉ FINAL DU PIPELINE")
    print("=" * 35)
    print(f"✅ Données initiales: {data.shape}")
    print(f"✅ Après nettoyage: {cleaned_data.shape}")
    print(f"✅ Après feature engineering: {engineered_data.shape}")
    print(f"✅ Après encodage + scaling: {complete_data.shape}")
    print(f"✅ Après sélection features: {transformed_data.shape}")
    
    # Sauvegarde des données finales (features sélectionnées)
    output_path = "data/processed/credit_engineered_transformed.csv"
    try:
        # Ajout de la cible si disponible
        if target is not None:
            final_data = transformed_data.copy()
            final_data['cible'] = target.reset_index(drop=True)
        else:
            final_data = transformed_data
            
        final_data.to_csv(output_path, index=False)
        print(f"💾 Données FINALES sauvegardées: {output_path}")
        print(f"   📊 Forme: {final_data.shape} ({final_data.shape[1]-1} features sélectionnées)")
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde: {e}")
    
    # RAPPORT DES FICHIERS GÉNÉRÉS
    print(f"\n📂 FICHIERS GÉNÉRÉS:")
    print(f"   1. {complete_output_path}")
    print(f"      → TOUTES les variables transformées ({complete_data.shape[1]-1} features)")
    print(f"   2. {output_path}")
    print(f"      → Features sélectionnées optimisées ({final_data.shape[1]-1} features)")
    print(f"   📉 Réduction: {complete_data.shape[1] - final_data.shape[1]} features supprimées")
    
    print("\n🎉 PIPELINE DE FEATURE ENGINEERING TERMINÉ AVEC SUCCÈS!")
    return True


def analyze_feature_importance():
    """
    Analyse rapide de l'importance des features créées
    """
    
    print("\n🔍 ANALYSE DE L'IMPORTANCE DES FEATURES")
    print("=" * 50)
    
    try:
        # Chargement des données transformées
        data = pd.read_csv("data/processed/credit_engineered_transformed.csv")
        
        if 'cible' not in data.columns:
            print("⚠️ Variable cible non trouvée")
            return
        
        X = data.drop(columns=['cible'])
        y = data['cible']
        
        print(f"📊 Données chargées: {X.shape}")
        
        # Analyse rapide avec Random Forest
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        
        # Division des données
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Entraînement d'un modèle simple
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        
        # Importance des features
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': rf.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\n🏆 TOP 10 FEATURES LES PLUS IMPORTANTES:")
        print("-" * 40)
        for i, (_, row) in enumerate(feature_importance.head(10).iterrows(), 1):
            print(f"{i:2d}. {row['feature']:<30} {row['importance']:.4f}")
        
        # Score du modèle
        score = rf.score(X_test, y_test)
        print(f"\n📈 Score du modèle Random Forest: {score:.4f}")
        
    except Exception as e:
        print(f"❌ Erreur dans l'analyse: {e}")


if __name__ == "__main__":
    """
    Exécution du test complet du pipeline de Feature Engineering
    """
    
    # Test du pipeline principal
    success = test_feature_engineering_pipeline()
    
    if success:
        # Analyse de l'importance des features
        analyze_feature_importance()
        
        print("\n" + "="*60)
        print("🎯 PROCHAINES ÉTAPES SELON LES SPÉCIFICATIONS:")
        print("   • ÉTAPE 5: Modélisation Optimisée")
        print("   • ÉTAPE 6: Backtesting et Validation")
        print("   • PARTIE 2: Application Streamlit Interactive")
        print("="*60)
    else:
        print("\n❌ ÉCHEC DU PIPELINE - Vérifiez les erreurs ci-dessus")
        sys.exit(1) 