"""
Script de vérification complète de l'état des rapports
"""

import os
import json
from datetime import datetime

def verify_reports_status():
    """
    Vérifie l'état de mise à jour de tous les rapports
    """
    print("🔍 VÉRIFICATION DE L'ÉTAT DES RAPPORTS")
    print("=" * 60)
    
    # 1. Trouver tous les rapports de validation
    validation_dir = "modeling/validation"
    reports = [f for f in os.listdir(validation_dir) if f.startswith("validation_report_") and f.endswith(".json")]
    
    if not reports:
        print("❌ Aucun rapport de validation trouvé")
        return
    
    # Trier par timestamp
    reports.sort()
    print(f"📋 RAPPORTS DE VALIDATION TROUVÉS: {len(reports)}")
    print("-" * 40)
    
    for i, report in enumerate(reports, 1):
        timestamp = report.replace("validation_report_", "").replace(".json", "")
        report_path = os.path.join(validation_dir, report)
        
        # Charger et analyser le rapport
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        status = "✅ APPROUVÉ" if data['final_assessment']['production_ready'] else "❌ REJETÉ"
        auc = data['base_performance']['auc_roc']
        
        marker = "👑 DERNIER" if i == len(reports) else f"   {i}"
        print(f"{marker} | {timestamp} | AUC: {auc:.4f} | {status}")
    
    # 2. Analyser le dernier rapport
    latest_report = reports[-1]
    latest_timestamp = latest_report.replace("validation_report_", "").replace(".json", "")
    
    print(f"\n🎯 ANALYSE DU DERNIER RAPPORT ({latest_timestamp})")
    print("-" * 40)
    
    latest_path = os.path.join(validation_dir, latest_report)
    with open(latest_path, 'r', encoding='utf-8') as f:
        latest_data = json.load(f)
    
    # Métriques principales
    print(f"📊 MÉTRIQUES PRINCIPALES:")
    print(f"   • AUC-ROC: {latest_data['base_performance']['auc_roc']:.4f}")
    print(f"   • KS Statistic: {latest_data['base_performance']['ks_statistic']:.4f}")
    print(f"   • Gini Coefficient: {latest_data['base_performance']['gini_coefficient']:.4f}")
    
    # Conformité réglementaire
    print(f"\n📋 CONFORMITÉ RÉGLEMENTAIRE:")
    all_compliant = True
    for criterion, status in latest_data['regulatory_compliance'].items():
        status_icon = "✅" if status else "❌"
        if not status:
            all_compliant = False
        print(f"   • {criterion}: {status_icon}")
    
    # Statut final
    print(f"\n🏆 STATUT FINAL:")
    print(f"   • Validation réussie: {'✅ OUI' if latest_data['final_assessment']['production_ready'] else '❌ NON'}")
    print(f"   • Niveau de risque: {latest_data['final_assessment']['risk_level']}")
    print(f"   • Recommandation: {latest_data['final_assessment']['recommendation']}")
    
    # 3. Vérifier les modèles finaux
    final_models_dir = "modeling/models/final_models"
    if os.path.exists(final_models_dir):
        print(f"\n💾 MODÈLES FINAUX:")
        print("-" * 40)
        
        models = [f for f in os.listdir(final_models_dir) if f.endswith('.pkl')]
        metadata_files = [f for f in os.listdir(final_models_dir) if f.startswith('model_metadata_')]
        
        print(f"   • Modèles (.pkl): {len(models)}")
        print(f"   • Métadonnées: {len(metadata_files)}")
        
        if models:
            models.sort()
            latest_model = models[-1]
            print(f"   • Dernier modèle: {latest_model}")
            
            # Vérifier cohérence timestamp
            model_timestamp = ""
            for part in latest_model.split("_"):
                if len(part) == 13 and part.isdigit():
                    model_timestamp = part
                    break
            
            if model_timestamp == latest_timestamp:
                print(f"   • Cohérence timestamp: ✅ SYNCHRONISÉ")
            else:
                print(f"   • Cohérence timestamp: ⚠️ DÉSYNCHRONISÉ (modèle: {model_timestamp}, rapport: {latest_timestamp})")
    
    # 4. Vérifier les rapports de documentation
    doc_dir = "modeling/documentation"
    print(f"\n📄 RAPPORTS DE DOCUMENTATION:")
    print("-" * 40)
    
    docs = [
        ("RAPPORT_ETAPE_6_BACKTESTING_VALIDATION.md", "Rapport détaillé backtesting"),
        ("SYNTHESIS_LATEST_VALIDATION.md", "Synthèse dernière validation"),
        ("training_report_20250620_011935.txt", "Rapport d'entraînement")
    ]
    
    for doc_file, description in docs:
        doc_path = os.path.join(doc_dir, doc_file)
        if os.path.exists(doc_path):
            # Obtenir la date de modification
            mod_time = os.path.getmtime(doc_path)
            mod_date = datetime.fromtimestamp(mod_time).strftime("%d/%m/%Y %H:%M")
            print(f"   ✅ {description}: {mod_date}")
        else:
            print(f"   ❌ {description}: MANQUANT")
    
    # 5. Résumé final
    print(f"\n🎯 RÉSUMÉ DE VÉRIFICATION")
    print("=" * 60)
    
    print(f"✅ Dernière validation: {latest_timestamp}")
    print(f"✅ Status: {'APPROUVÉ' if latest_data['final_assessment']['production_ready'] else 'REJETÉ'}")
    print(f"✅ Performance: AUC-ROC {latest_data['base_performance']['auc_roc']:.4f}")
    print(f"✅ Conformité: {'100% CONFORME' if all_compliant else 'NON CONFORME'}")
    print(f"✅ Modèle final: {'CRÉÉ' if models else 'MANQUANT'}")
    
    if latest_data['final_assessment']['production_ready'] and all_compliant:
        print(f"\n🏆 CONCLUSION: TOUS LES RAPPORTS SONT À JOUR ET LE MODÈLE EST PRÊT POUR LA PRODUCTION!")
    else:
        print(f"\n⚠️  CONCLUSION: DES AMÉLIORATIONS SONT NÉCESSAIRES AVANT LA PRODUCTION")
    
    return latest_data['final_assessment']['production_ready'] and all_compliant

if __name__ == "__main__":
    success = verify_reports_status()
    print(f"\n{'🎉 VÉRIFICATION RÉUSSIE!' if success else '⚠️ ATTENTION REQUISE!'}") 