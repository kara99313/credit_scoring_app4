"""
Test de l'ÉTAPE 1 du workflow ML : DataProcessor
Suit l'ordre exact défini dans l'architecture
"""

import sys
import os
sys.path.append('src')

from data_processing import DataProcessor

def main():
    print("🚀 WORKFLOW ML - ÉTAPE 1")
    print("=" * 60)
    print("Exécution du DataProcessor selon l'architecture prévue\n")
    
    # Initialisation du processeur
    processor = DataProcessor()
    
    # ÉTAPE 1.1: Chargement et validation
    print("PHASE 1.1: CHARGEMENT ET VALIDATION")
    data = processor.load_data("data/raw/credit.csv")
    
    if data is None:
        print("❌ Échec du chargement des données")
        return
    
    print(f"\n✅ ÉTAPE 1.1 TERMINÉE")
    print(f"Données chargées et validées: {len(data)} lignes")
    
    # ÉTAPE 1.2: Nettoyage
    print("\n" + "="*60)
    print("PHASE 1.2: NETTOYAGE DES DONNÉES")
    cleaned_data = processor.clean_data()
    
    if cleaned_data is None:
        print("❌ Échec du nettoyage des données")
        return
        
    print(f"\n✅ ÉTAPE 1.2 TERMINÉE")
    print(f"Données nettoyées: {len(cleaned_data)} lignes")
    
    # Résumé final
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DE L'ÉTAPE 1")
    print("="*60)
    print(f"📊 Données initiales: {len(data)} lignes")
    print(f"🧹 Données nettoyées: {len(cleaned_data)} lignes")
    print(f"💾 Fichier sauvegardé: data/processed/credit_cleaned.csv")
    print(f"✅ ÉTAPE 1 COMPLÈTE - Prêt pour l'ÉTAPE 2 (EDA)")

if __name__ == "__main__":
    main() 