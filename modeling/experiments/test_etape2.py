"""
Test de l'ÉTAPE 2 du workflow ML : EDA Analyzer
Génère des analyses complètes avec commentaires et interprétations
"""

import sys
import os
sys.path.append('src')

from eda_analyzer import EDAAnalyzer

def main():
    print("🔍 WORKFLOW ML - ÉTAPE 2")
    print("=" * 60)
    print("Analyse Exploratoire des Données (EDA) avec interprétations automatiques\n")
    
    # Vérification des données nettoyées
    if not os.path.exists("data/processed/credit_cleaned.csv"):
        print("❌ Données nettoyées non trouvées!")
        print("Veuillez d'abord exécuter l'ÉTAPE 1 (test_etape1.py)")
        return
    
    # Initialisation de l'analyseur EDA
    analyzer = EDAAnalyzer("data/processed/credit_cleaned.csv")
    
    print("🎯 OBJECTIFS DE L'ANALYSE :")
    print("   • Comprendre les distributions de toutes les variables")
    print("   • Analyser la variable cible (remboursement)")
    print("   • Identifier les relations entre variables")
    print("   • Détecter les corrélations importantes")
    print("   • Effectuer des tests statistiques")
    print("   • Générer des recommandations pour la modélisation")
    
    print("\n" + "="*60)
    
    # Exécution de l'analyse complète
    try:
        analyzer.comprehensive_analysis()
        
        print("\n" + "="*60)
        print("🎉 ÉTAPE 2 TERMINÉE AVEC SUCCÈS!")
        print("="*60)
        
        print("\n📁 FICHIERS GÉNÉRÉS :")
        output_dir = "reports/eda"
        
        # Liste des fichiers créés
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            for file in files:
                file_path = os.path.join(output_dir, file)
                size_kb = os.path.getsize(file_path) / 1024
                print(f"   📄 {file} ({size_kb:.1f} KB)")
        
        print(f"\n✅ RÉSULTATS DISPONIBLES DANS : {output_dir}")
        print("\n🎯 PROCHAINE ÉTAPE : Feature Engineering (ÉTAPE 3)")
        print("   Les analyses et recommandations sont prêtes pour guider")
        print("   la création de nouvelles variables métier.")
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DE L'ANALYSE : {e}")
        print("Vérifiez que toutes les dépendances sont installées:")
        print("   pip install matplotlib seaborn scipy")

if __name__ == "__main__":
    main() 