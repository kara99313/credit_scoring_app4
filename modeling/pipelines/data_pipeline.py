"""
Data Pipeline for Credit Scoring System

This module orchestrates the complete data processing pipeline.

Author: Credit Scoring Team
Created: 2024
"""

import sys
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Optional

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.data_processing import DataProcessor
from src.eda_analyzer import EDAAnalyzer
from src.transformers.feature_engineer import FeatureEngineer
from src.transformers.variable_transformer import VariableTransformer


class DataPipeline:
    """Pipeline de traitement des données complet"""
    
    def __init__(self, config: Dict):
        """
        Initialisation du pipeline de données
        
        Args:
            config: Configuration du projet
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def run(self, force_reprocess: bool = False):
        """
        Exécute le pipeline de données complet
        
        Args:
            force_reprocess: Force le retraitement même si les données existent
        """
        print("\n🔄 PIPELINE DE DONNÉES COMPLET")
        print("=" * 50)
        
        # Vérifier si les données finales existent déjà
        final_data_path = Path("data/processed/credit_engineered_transformed.csv")
        if final_data_path.exists() and not force_reprocess:
            print("✅ Données déjà traitées trouvées. Utilisation des données existantes.")
            print(f"📁 Fichier: {final_data_path}")
            return
        
        # 1. Chargement et nettoyage des données
        print("\n📊 1. Chargement et nettoyage des données...")
        processor = DataProcessor(self.config)
        df_cleaned = processor.load_and_clean_data()
        
        # 2. Analyse exploratoire (optionnel)
        if self.config.get('data_pipeline', {}).get('run_eda', False):
            print("\n📈 2. Analyse exploratoire des données...")
            eda_analyzer = EDAAnalyzer(self.config)
            eda_analyzer.run_complete_analysis(df_cleaned)
        
        # 3. Feature Engineering
        print("\n🔧 3. Feature Engineering...")
        feature_engineer = FeatureEngineer(self.config)
        df_engineered = feature_engineer.engineer_all_features(df_cleaned)
        
        # 4. Transformation des variables
        print("\n⚙️ 4. Transformation des variables...")
        transformer = VariableTransformer(self.config)
        
        # Séparation des features et de la cible
        X = df_engineered.drop(columns=['cible'])
        y = df_engineered['cible']
        
        # Transformation complète
        X_transformed = transformer.transform_all_variables(X, y, fit=True)
        
        # Reconstruction du DataFrame final
        df_final = X_transformed.copy()
        df_final['cible'] = y.values
        
        # 5. Sauvegarde
        print("\n💾 5. Sauvegarde des données transformées...")
        output_path = Path("data/processed")
        output_path.mkdir(exist_ok=True)
        
        # Sauvegarde du fichier final
        final_path = output_path / "credit_engineered_transformed.csv"
        df_final.to_csv(final_path, index=False)
        
        print(f"✅ Pipeline de données terminé avec succès!")
        print(f"📁 Données sauvegardées: {final_path}")
        print(f"📊 Shape finale: {df_final.shape}") 