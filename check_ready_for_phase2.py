"""
Script de vérification complète - Prêt pour Phase 2
"""

import os
import pickle
import pandas as pd
import json
from datetime import datetime
import sys

def print_header(title):
    """Affiche un header stylisé"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_check(item, status, details=""):
    """Affiche un check avec status"""
    icon = "✅" if status else "❌"
    print(f"{icon} {item}")
    if details:
        print(f"   → {details}")

def check_model_files():
    """Vérifie la présence et validité des modèles"""
    print_header("VÉRIFICATION MODÈLES")
    
    checks = []
    
    # Vérifier modèle principal
    model_path = "modeling/models/best_model.pkl"
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            checks.append(("Modèle principal chargé", True, f"Taille: {os.path.getsize(model_path)//1024} KB"))
        except Exception as e:
            checks.append(("Modèle principal", False, f"Erreur: {str(e)}"))
    else:
        checks.append(("Modèle principal", False, "Fichier non trouvé"))
    
    # Vérifier modèles finaux
    final_models_dir = "modeling/models/final_models"
    if os.path.exists(final_models_dir):
        final_models = [f for f in os.listdir(final_models_dir) if f.endswith('.pkl')]
        if final_models:
            checks.append(("Modèles finaux", True, f"{len(final_models)} modèle(s) trouvé(s)"))
        else:
            checks.append(("Modèles finaux", False, "Aucun modèle final trouvé"))
    else:
        checks.append(("Dossier modèles finaux", False, "Dossier non trouvé"))
    
    # Afficher résultats
    for item, status, details in checks:
        print_check(item, status, details)
    
    return all(check[1] for check in checks)

def check_data_files():
    """Vérifie la présence et validité des données"""
    print_header("VÉRIFICATION DONNÉES")
    
    checks = []
    
    # Données originales
    raw_data = "data/raw/credit.csv"
    if os.path.exists(raw_data):
        try:
            df = pd.read_csv(raw_data)
            checks.append(("Données raw", True, f"{len(df)} échantillons, {len(df.columns)} colonnes"))
        except Exception as e:
            checks.append(("Données raw", False, f"Erreur lecture: {str(e)}"))
    else:
        checks.append(("Données raw", False, "Fichier non trouvé"))
    
    # Données transformées
    processed_data = "data/processed/credit_all_transformed.csv"
    if os.path.exists(processed_data):
        try:
            df = pd.read_csv(processed_data)
            checks.append(("Données transformées", True, f"{len(df)} échantillons, {len(df.columns)} features"))
        except Exception as e:
            checks.append(("Données transformées", False, f"Erreur lecture: {str(e)}"))
    else:
        checks.append(("Données transformées", False, "Fichier non trouvé"))
    
    # Afficher résultats
    for item, status, details in checks:
        print_check(item, status, details)
    
    return all(check[1] for check in checks)

def check_validation_reports():
    """Vérifie les rapports de validation"""
    print_header("VÉRIFICATION RAPPORTS VALIDATION")
    
    checks = []
    
    # Rapports JSON
    validation_dir = "modeling/validation"
    if os.path.exists(validation_dir):
        json_reports = [f for f in os.listdir(validation_dir) if f.endswith('.json')]
        if json_reports:
            # Trouver le plus récent
            json_reports.sort()
            latest = json_reports[-1]
            checks.append(("Rapports JSON", True, f"{len(json_reports)} rapports, dernier: {latest}"))
            
            # Vérifier contenu du dernier
            try:
                with open(f"{validation_dir}/{latest}", 'r') as f:
                    report = json.load(f)
                if report.get('validation_passed'):
                    checks.append(("Validation réussie", True, f"AUC: {report.get('auc_roc', 'N/A')}"))
                else:
                    checks.append(("Validation réussie", False, "Dernière validation échouée"))
            except Exception as e:
                checks.append(("Lecture rapport", False, f"Erreur: {str(e)}"))
        else:
            checks.append(("Rapports JSON", False, "Aucun rapport trouvé"))
    else:
        checks.append(("Dossier validation", False, "Dossier non trouvé"))
    
    # Rapport markdown principal
    main_report = "modeling/documentation/RAPPORT_ETAPE_6_BACKTESTING_VALIDATION.md"
    if os.path.exists(main_report):
        size = os.path.getsize(main_report)
        checks.append(("Rapport principal", True, f"Taille: {size//1024} KB"))
    else:
        checks.append(("Rapport principal", False, "Rapport non trouvé"))
    
    # Afficher résultats
    for item, status, details in checks:
        print_check(item, status, details)
    
    return all(check[1] for check in checks)

def check_documentation():
    """Vérifie la documentation"""
    print_header("VÉRIFICATION DOCUMENTATION")
    
    checks = []
    
    # Fichiers documentation créés
    docs = [
        ("Résumé complet", "RESUME_PROJET_COMPLET.md"),
        ("Roadmap Phase 2", "ROADMAP_PHASE_2.md"),
        ("Architecture", "ARCHITECTURE_COMPLETE.md")
    ]
    
    for name, filename in docs:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            checks.append((name, True, f"Taille: {size//1024} KB"))
        else:
            checks.append((name, False, "Fichier non trouvé"))
    
    # Rapports EDA
    eda_dir = "reports/eda"
    if os.path.exists(eda_dir):
        eda_files = [f for f in os.listdir(eda_dir) if f.endswith('.png')]
        checks.append(("Graphiques EDA", True, f"{len(eda_files)} graphiques générés"))
    else:
        checks.append(("Graphiques EDA", False, "Dossier non trouvé"))
    
    # Afficher résultats
    for item, status, details in checks:
        print_check(item, status, details)
    
    return all(check[1] for check in checks)

def check_dependencies():
    """Vérifie les dépendances Python"""
    print_header("VÉRIFICATION DÉPENDANCES")
    
    required_packages = [
        'pandas', 'numpy', 'scikit-learn', 'xgboost',
        'matplotlib', 'seaborn', 'plotly', 'pickle'
    ]
    
    checks = []
    
    for package in required_packages:
        try:
            __import__(package)
            checks.append((f"Package {package}", True, "Installé"))
        except ImportError:
            checks.append((f"Package {package}", False, "Non installé"))
    
    # Afficher résultats
    for item, status, details in checks:
        print_check(item, status, details)
    
    return all(check[1] for check in checks)

def check_structure():
    """Vérifie la structure du projet"""
    print_header("VÉRIFICATION STRUCTURE PROJET")
    
    required_dirs = [
        "data/raw", "data/processed", "modeling/models", 
        "modeling/validation", "modeling/documentation",
        "reports/eda", "src", "scripts", "config"
    ]
    
    checks = []
    
    for directory in required_dirs:
        if os.path.exists(directory):
            files_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
            checks.append((f"Dossier {directory}", True, f"{files_count} fichier(s)"))
        else:
            checks.append((f"Dossier {directory}", False, "Manquant"))
    
    # Afficher résultats
    for item, status, details in checks:
        print_check(item, status, details)
    
    return all(check[1] for check in checks)

def generate_readiness_report():
    """Génère un rapport de préparation"""
    print_header("RAPPORT DE PRÉPARATION PHASE 2")
    
    # Exécuter toutes les vérifications
    checks = {
        "Modèles": check_model_files(),
        "Données": check_data_files(),
        "Validation": check_validation_reports(),
        "Documentation": check_documentation(),
        "Dépendances": check_dependencies(),
        "Structure": check_structure()
    }
    
    # Résumé global
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ GLOBAL")
    print(f"{'='*60}")
    
    total_checks = len(checks)
    passed_checks = sum(checks.values())
    
    for category, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {category}")
    
    print(f"\n🎯 SCORE GLOBAL: {passed_checks}/{total_checks} ({passed_checks/total_checks*100:.1f}%)")
    
    # Recommandations
    print(f"\n{'='*60}")
    print("🎯 RECOMMANDATIONS")
    print(f"{'='*60}")
    
    if passed_checks == total_checks:
        print("🎉 PARFAIT! Toutes les vérifications sont passées.")
        print("✅ Le projet est PRÊT pour la Phase 2!")
        print("🚀 Recommandation: Commencer immédiatement par l'interface Streamlit")
        
        # Actions immédiates
        print(f"\n📋 ACTIONS IMMÉDIATES:")
        print("1. mkdir streamlit_app")
        print("2. pip install streamlit plotly shap")
        print("3. Créer streamlit_app/main.py")
        print("4. Lancer le premier prototype")
        
    else:
        print("⚠️  Certaines vérifications ont échoué.")
        print("🔧 Corrigez les problèmes avant de commencer la Phase 2.")
        
        # Lister les problèmes
        failed = [cat for cat, status in checks.items() if not status]
        print(f"\n❌ CATÉGORIES À CORRIGER: {', '.join(failed)}")
    
    return passed_checks == total_checks

def main():
    """Fonction principale"""
    print("🔍 VÉRIFICATION PRÉPARATION PHASE 2")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        is_ready = generate_readiness_report()
        
        # Status de sortie
        if is_ready:
            print(f"\n🎉 PHASE 2 READY - SUCCESS!")
            sys.exit(0)
        else:
            print(f"\n⚠️  PHASE 2 NOT READY - ISSUES FOUND")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ ERREUR LORS DE LA VÉRIFICATION: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 