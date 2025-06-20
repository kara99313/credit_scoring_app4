"""
🔍 Script de vérification complète - Prêt pour Phase 2
"""

import os
import pickle
import pandas as pd
import json
from datetime import datetime

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def check_item(name, condition, details=""):
    icon = "✅" if condition else "❌"
    print(f"{icon} {name}")
    if details:
        print(f"   → {details}")
    return condition

def main():
    print("🔍 VÉRIFICATION PRÉPARATION PHASE 2")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_checks = 0
    passed_checks = 0
    
    # 1. Vérification Modèles
    print_header("MODÈLES")
    
    # Modèle principal
    model_exists = os.path.exists("modeling/models/best_model.pkl")
    if check_item("Modèle principal", model_exists):
        try:
            with open("modeling/models/best_model.pkl", 'rb') as f:
                model = pickle.load(f)
            check_item("Modèle chargeable", True, "Chargement réussi")
            passed_checks += 1
        except:
            check_item("Modèle chargeable", False, "Erreur de chargement")
    total_checks += 1
    
    # Modèles finaux
    final_models = os.path.exists("modeling/models/final_models")
    if check_item("Modèles finaux", final_models):
        if final_models:
            count = len([f for f in os.listdir("modeling/models/final_models") if f.endswith('.pkl')])
            check_item("Nombre modèles finaux", count > 0, f"{count} modèle(s)")
            if count > 0:
                passed_checks += 1
    total_checks += 1
    
    # 2. Vérification Données
    print_header("DONNÉES")
    
    # Données raw
    raw_data = os.path.exists("data/raw/credit.csv")
    if check_item("Données raw", raw_data):
        if raw_data:
            df = pd.read_csv("data/raw/credit.csv")
            check_item("Données raw lisibles", True, f"{len(df)} échantillons")
            passed_checks += 1
    total_checks += 1
    
    # Données transformées
    processed_data = os.path.exists("data/processed/credit_all_transformed.csv")
    if check_item("Données transformées", processed_data):
        if processed_data:
            df = pd.read_csv("data/processed/credit_all_transformed.csv")
            check_item("Données transformées lisibles", True, f"{len(df)} échantillons")
            passed_checks += 1
    total_checks += 1
    
    # 3. Vérification Validation
    print_header("VALIDATION")
    
    # Rapports validation
    validation_dir = os.path.exists("modeling/validation")
    if check_item("Dossier validation", validation_dir):
        if validation_dir:
            reports = [f for f in os.listdir("modeling/validation") if f.endswith('.json')]
            if check_item("Rapports JSON", len(reports) > 0, f"{len(reports)} rapport(s)"):
                # Vérifier le dernier rapport
                reports.sort()
                latest = reports[-1]
                try:
                    with open(f"modeling/validation/{latest}", 'r') as f:
                        report = json.load(f)
                    validation_passed = report.get('validation_passed', False)
                    auc = report.get('auc_roc', 0)
                    if check_item("Dernière validation", validation_passed, f"AUC: {auc:.4f}"):
                        passed_checks += 1
                except:
                    check_item("Lecture rapport", False, "Erreur lecture")
    total_checks += 1
    
    # 4. Vérification Documentation
    print_header("DOCUMENTATION")
    
    # Rapport principal
    main_report = os.path.exists("modeling/documentation/RAPPORT_ETAPE_6_BACKTESTING_VALIDATION.md")
    if check_item("Rapport principal", main_report):
        passed_checks += 1
    total_checks += 1
    
    # Résumé créé
    resume_exists = os.path.exists("RESUME_PROJET_COMPLET.md")
    if check_item("Résumé complet", resume_exists):
        if resume_exists:
            size = os.path.getsize("RESUME_PROJET_COMPLET.md")
            check_item("Résumé détaillé", size > 10000, f"Taille: {size//1024}KB")
            passed_checks += 1
    total_checks += 1
    
    # Roadmap créée
    roadmap_exists = os.path.exists("ROADMAP_PHASE_2.md")
    if check_item("Roadmap Phase 2", roadmap_exists):
        passed_checks += 1
    total_checks += 1
    
    # 5. Vérification Structure
    print_header("STRUCTURE PROJET")
    
    required_dirs = ["data", "modeling", "reports", "src", "scripts"]
    structure_ok = all(os.path.exists(d) for d in required_dirs)
    if check_item("Structure de base", structure_ok):
        passed_checks += 1
    total_checks += 1
    
    # 6. Vérification Dépendances
    print_header("DÉPENDANCES")
    
    packages = ['pandas', 'numpy', 'scikit-learn', 'matplotlib']
    deps_ok = True
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            deps_ok = False
            break
    
    if check_item("Packages Python", deps_ok):
        passed_checks += 1
    total_checks += 1
    
    # RÉSUMÉ FINAL
    print_header("RÉSUMÉ FINAL")
    
    score = (passed_checks / total_checks) * 100
    print(f"🎯 SCORE: {passed_checks}/{total_checks} ({score:.1f}%)")
    
    if score >= 90:
        print("🎉 EXCELLENT! Projet prêt pour Phase 2")
        print("✅ Recommandation: Commencer par Streamlit")
        print("\n📋 ACTIONS IMMÉDIATES:")
        print("1. mkdir streamlit_app")
        print("2. pip install streamlit plotly shap")
        print("3. Créer premier prototype")
    elif score >= 70:
        print("⚠️  BON mais quelques améliorations nécessaires")
        print("🔧 Corriger les points manquants avant Phase 2")
    else:
        print("❌ INSUFFISANT - Corrections importantes nécessaires")
        print("🛠️  Reprendre les éléments manquants")
    
    print(f"\n🚀 STATUT: {'PRÊT POUR PHASE 2' if score >= 90 else 'CORRECTIONS NÉCESSAIRES'}")

if __name__ == "__main__":
    main() 