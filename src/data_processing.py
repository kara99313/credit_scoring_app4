"""
Module de traitement des données pour le système de crédit scoring.
Suit le workflow ML défini dans l'architecture.
"""

import pandas as pd
import numpy as np
import os
import logging
from typing import Tuple, Dict, Any

class DataProcessor:
    """
    Classe principale pour le chargement et prétraitement des données.
    Suit l'ordre exact du workflow ML défini dans l'architecture.
    """
    
    def __init__(self):
        """Initialisation du processeur de données"""
        self.data = None
        self.cleaned_data = None
        self.quality_report = {}
        
        # Configuration du logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def load_data(self, file_path: str = "data/raw/credit.csv") -> pd.DataFrame:
        """
        ÉTAPE 1.1: Chargement et validation initiale des données
        """
        print("🔄 ÉTAPE 1.1: CHARGEMENT DES DONNÉES")
        print("=" * 50)
        
        # Chargement des données
        try:
            self.data = pd.read_csv(file_path)
            print(f"✅ Données chargées: {len(self.data)} lignes, {len(self.data.columns)} colonnes")
        except Exception as e:
            print(f"❌ Erreur de chargement: {e}")
            return None
            
        # Validation de l'intégrité du fichier
        self.validate_file_integrity()
        
        # Vérification de conformité du schéma
        self.check_schema_compliance()
        
        # Résumé statistique
        self.log_data_summary()
        
        # Génération du rapport qualité
        self.generate_quality_report()
        
        return self.data
    
    def validate_file_integrity(self):
        """Vérification de l'intégrité du fichier"""
        print("\n🔍 Validation de l'intégrité...")
        
        if self.data is None or self.data.empty:
            print("❌ Fichier vide ou non chargé")
            return False
            
        print(f"✅ Intégrité validée: {len(self.data)} enregistrements")
        return True
    
    def check_schema_compliance(self):
        """Vérification de conformité du schéma"""
        print("\n📋 Vérification du schéma...")
        
        # Colonnes attendues
        expected_columns = [
            'duree', 'historique', 'objet', 'montant', 'epargne',
            'anciennete_emploi', 'taux_endettement', 'statut', 
            'autres_debiteurs', 'domicile', 'biens', 'age',
            'credit_exterieur', 'logement', 'emploi', 'nombre_personnes',
            'telephone', 'cible', 'compte', 'nombre_credit', 'travailleur_etranger'
        ]
        
        missing_cols = set(expected_columns) - set(self.data.columns)
        
        if missing_cols:
            print(f"⚠️ Colonnes manquantes: {missing_cols}")
        else:
            print("✅ Schéma conforme")
            
        return len(missing_cols) == 0
    
    def log_data_summary(self):
        """Résumé statistique des données"""
        print("\n📊 Résumé statistique...")
        
        summary = {
            'nb_lignes': len(self.data),
            'nb_colonnes': len(self.data.columns),
            'valeurs_manquantes': self.data.isnull().sum().sum(),
            'doublons': self.data.duplicated().sum()
        }
        
        for key, value in summary.items():
            print(f"   • {key}: {value}")
            
        self.quality_report['summary'] = summary
    
    def generate_quality_report(self):
        """Génération du rapport qualité initial"""
        print("\n📝 Génération du rapport qualité...")
        
        # Analyse des valeurs manquantes
        missing_analysis = {}
        for col in self.data.columns:
            missing_count = self.data[col].isnull().sum()
            if missing_count > 0:
                missing_analysis[col] = {
                    'count': missing_count,
                    'percentage': (missing_count / len(self.data)) * 100
                }
        
        self.quality_report.update({
            'missing_values': missing_analysis,
            'duplicates': self.data.duplicated().sum()
        })
        
        print(f"✅ Rapport qualité généré")
        print(f"   • Valeurs manquantes: {len(missing_analysis)} colonnes affectées")
    
    def clean_data(self) -> pd.DataFrame:
        """
        ÉTAPE 1.2: Nettoyage des données
        """
        print("\n🧹 ÉTAPE 1.2: NETTOYAGE DES DONNÉES")
        print("=" * 50)
        
        if self.data is None:
            print("❌ Aucune donnée à nettoyer. Chargez d'abord les données.")
            return None
            
        # Copie pour le nettoyage
        self.cleaned_data = self.data.copy()
        
        # 1. Suppression des doublons
        self.remove_duplicates()
        
        # 2. Traitement des valeurs manquantes
        self.handle_missing_values()
        
        # 3. Traitement des valeurs aberrantes
        self.treat_outliers()
        
        # 4. Standardisation des formats
        self.standardize_formats()
        
        # 5. Nettoyage de la variable cible
        self.clean_target_variable()
        
        # 6. Validation finale
        self.validate_cleaned_data()
        
        return self.cleaned_data
    
    def remove_duplicates(self):
        """Suppression des doublons"""
        print("\n🔄 Suppression des doublons...")
        
        initial_count = len(self.cleaned_data)
        self.cleaned_data = self.cleaned_data.drop_duplicates()
        removed_count = initial_count - len(self.cleaned_data)
        
        if removed_count > 0:
            print(f"✅ {removed_count} doublons supprimés")
        else:
            print("✅ Aucun doublon trouvé")
    
    def handle_missing_values(self):
        """Traitement des valeurs manquantes"""
        print("\n🕳️ Traitement des valeurs manquantes...")
        
        missing_before = self.cleaned_data.isnull().sum().sum()
        
        # Stratégies par type de variable
        for col in self.cleaned_data.columns:
            missing_count = self.cleaned_data[col].isnull().sum()
            
            if missing_count > 0:
                if self.cleaned_data[col].dtype in ['int64', 'float64']:
                    # Variables numériques: imputation par la médiane
                    median_value = self.cleaned_data[col].median()
                    self.cleaned_data[col].fillna(median_value, inplace=True)
                    print(f"   • {col}: {missing_count} valeurs → médiane ({median_value:.1f})")
                    
                else:
                    # Variables catégorielles: imputation par le mode
                    mode_value = self.cleaned_data[col].mode().iloc[0] if not self.cleaned_data[col].mode().empty else 'unknown'
                    self.cleaned_data[col].fillna(mode_value, inplace=True)
                    print(f"   • {col}: {missing_count} valeurs → mode ('{mode_value}')")
        
        missing_after = self.cleaned_data.isnull().sum().sum()
        print(f"✅ Valeurs manquantes: {missing_before} → {missing_after}")
    
    def treat_outliers(self):
        """Traitement des valeurs aberrantes"""
        print("\n📈 Traitement des valeurs aberrantes...")
        
        # Variables numériques à traiter
        numeric_cols = ['duree', 'montant', 'age']
        
        for col in numeric_cols:
            if col in self.cleaned_data.columns:
                # Méthode IQR pour détecter les outliers
                Q1 = self.cleaned_data[col].quantile(0.25)
                Q3 = self.cleaned_data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Compter les outliers
                outliers_mask = (self.cleaned_data[col] < lower_bound) | (self.cleaned_data[col] > upper_bound)
                outliers_count = outliers_mask.sum()
                
                if outliers_count > 0:
                    # Écrêtage des valeurs aberrantes (winsorization)
                    self.cleaned_data.loc[self.cleaned_data[col] < lower_bound, col] = lower_bound
                    self.cleaned_data.loc[self.cleaned_data[col] > upper_bound, col] = upper_bound
                    print(f"   • {col}: {outliers_count} outliers écrêtés")
                else:
                    print(f"   • {col}: aucun outlier détecté")
    
    def standardize_formats(self):
        """Standardisation des formats"""
        print("\n🔧 Standardisation des formats...")
        
        # Nettoyage des chaînes de caractères
        for col in self.cleaned_data.columns:
            if self.cleaned_data[col].dtype == 'object':
                # Suppression des espaces en début/fin
                self.cleaned_data[col] = self.cleaned_data[col].astype(str).str.strip()
                # Conversion en minuscules pour cohérence
                self.cleaned_data[col] = self.cleaned_data[col].str.lower()
        
        print("✅ Formats standardisés")
    
    def clean_target_variable(self):
        """
        Nettoie et encode la variable cible 'classe'
        """
        self.logger.info("🎯 Nettoyage de la variable cible...")
        
        # Mapping des valeurs textuelles vers numériques pour la variable cible
        target_mapping = {
            'credit bien rembourse': 1,
            'credit mal rembourse': 0,
            'bon credit': 1,
            'mauvais credit': 0,
            'good': 1,
            'bad': 0,
            1: 1,
            0: 0
        }
        
        if 'classe' in self.cleaned_data.columns:
            # Convertir les valeurs selon le mapping
            self.cleaned_data['classe'] = self.cleaned_data['classe'].map(target_mapping)
            
            # Vérifier s'il reste des valeurs non mappées
            unmapped = self.cleaned_data['classe'].isna().sum()
            if unmapped > 0:
                self.logger.warning(f"⚠️ {unmapped} valeurs non mappées dans 'classe'")
                # Les valeurs non mappées deviennent 0 par défaut
                self.cleaned_data['classe'] = self.cleaned_data['classe'].fillna(0)
            
            self.logger.info(f"✅ Variable cible nettoyée: {self.cleaned_data['classe'].value_counts().to_dict()}")
        
        return self.cleaned_data
    
    def validate_cleaned_data(self):
        """Validation finale des données nettoyées"""
        print("\n✅ Validation finale...")
        
        # Vérifications finales
        checks = {
            'Valeurs manquantes': self.cleaned_data.isnull().sum().sum(),
            'Doublons': self.cleaned_data.duplicated().sum(),
            'Lignes finales': len(self.cleaned_data)
        }
        
        for check, value in checks.items():
            print(f"   • {check}: {value}")
        
        # Sauvegarde optionnelle
        output_path = "data/processed/credit_cleaned.csv"
        os.makedirs("data/processed", exist_ok=True)
        self.cleaned_data.to_csv(output_path, index=False)
        print(f"💾 Données nettoyées sauvegardées: {output_path}")
        
        return True
    
    def get_quality_report(self) -> Dict[str, Any]:
        """Retourne le rapport qualité"""
        return self.quality_report
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Retourne les données nettoyées"""
        return self.cleaned_data 