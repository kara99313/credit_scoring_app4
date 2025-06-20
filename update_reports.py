"""
Script de mise à jour des rapports avec les dernières données
"""

import os
import json
from datetime import datetime

def update_reports():
    """
    Met à jour tous les rapports avec les dernières données de validation
    """
    print("🔄 MISE À JOUR DES RAPPORTS")
    print("=" * 50)
    
    # Trouver le rapport de validation le plus récent
    validation_dir = "modeling/validation"
    reports = [f for f in os.listdir(validation_dir) if f.startswith("validation_report_") and f.endswith(".json")]
    
    if not reports:
        print("❌ Aucun rapport de validation trouvé")
        return False
    
    # Trier par timestamp (le plus récent en dernier)
    reports.sort()
    latest_report = reports[-1]
    latest_timestamp = latest_report.replace("validation_report_", "").replace(".json", "")
    
    print(f"📋 Rapport le plus récent: {latest_report}")
    print(f"⏰ Timestamp: {latest_timestamp}")
    
    # Charger les données du rapport le plus récent
    report_path = os.path.join(validation_dir, latest_report)
    with open(report_path, 'r', encoding='utf-8') as f:
        latest_data = json.load(f)
    
    print(f"✅ Données chargées du rapport: {report_path}")
    
    # Créer un rapport de synthèse
    summary_path = "modeling/documentation/SYNTHESIS_LATEST_VALIDATION.md"
    
    print(f"\n📊 CRÉATION RAPPORT DE SYNTHÈSE")
    print("-" * 40)
    
    synthesis_content = f"""# 📊 SYNTHÈSE DE LA DERNIÈRE VALIDATION

**Timestamp :** {latest_timestamp}  
**Date :** {datetime.now().strftime('%d/%m/%Y %H:%M')}  

## 🎯 Résultats de Validation

**Status Global :** {'✅ APPROUVÉ' if latest_data['final_assessment']['production_ready'] else '❌ REJETÉ'}  
**Niveau de Risque :** {latest_data['final_assessment']['risk_level']}  
**Recommandation :** {latest_data['final_assessment']['recommendation']}  

## 📈 Métriques Principales

| Métrique | Valeur | Seuil | Status |
|----------|--------|-------|--------|
| AUC-ROC | {latest_data['base_performance']['auc_roc']:.4f} | ≥ 0.75 | {'✅' if latest_data['regulatory_compliance']['AUC minimum (≥0.75)'] else '❌'} |
| KS Statistic | {latest_data['base_performance']['ks_statistic']:.4f} | ≥ 0.30 | {'✅' if latest_data['regulatory_compliance']['KS minimum (≥0.30)'] else '❌'} |
| Gini Coefficient | {latest_data['base_performance']['gini_coefficient']:.4f} | ≥ 0.40 | {'✅' if latest_data['regulatory_compliance']['Gini minimum (≥0.40)'] else '❌'} |

## 🕐 Stabilité Temporelle

**Évaluation :** {latest_data['temporal_stability']['stability_assessment']}  
**Déclin AUC :** {latest_data['temporal_stability']['auc_decline']:.4f} (seuil < 0.10)  

### Performances par Période
"""
    
    for period in latest_data['temporal_stability']['period_results']:
        synthesis_content += f"- **Période {period['period']} :** AUC = {period['auc_roc']:.4f}, KS = {period['ks_statistic']:.4f}\n"
    
    synthesis_content += f"""

## 💥 Tests de Stress

"""
    
    for scenario, results in latest_data['stress_tests'].items():
        synthesis_content += f"- **{scenario.title()} :** AUC = {results['auc_roc']:.4f}, Dégradation = {results['degradation']:.4f}\n"
    
    synthesis_content += f"""

## 📋 Conformité Réglementaire

"""
    
    for criterion, status in latest_data['regulatory_compliance'].items():
        status_icon = "✅" if status else "❌"
        synthesis_content += f"- {criterion} : {status_icon}\n"
    
    synthesis_content += f"""

---
*Rapport généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*
"""
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(synthesis_content)
    
    print(f"✅ Rapport de synthèse créé: {summary_path}")
    
    # Affichage du résumé
    print(f"\n🎯 RÉSUMÉ DE LA MISE À JOUR")
    print("-" * 40)
    print(f"📅 Dernière validation: {latest_timestamp}")
    print(f"🎯 Status: {'✅ APPROUVÉ' if latest_data['final_assessment']['production_ready'] else '❌ REJETÉ'}")
    print(f"📊 AUC-ROC: {latest_data['base_performance']['auc_roc']:.4f}")
    print(f"🔒 Stabilité: {latest_data['temporal_stability']['stability_assessment']}")
    print(f"💪 Prêt pour production: {'Oui' if latest_data['final_assessment']['production_ready'] else 'Non'}")
    
    return True

if __name__ == "__main__":
    success = update_reports()
    if success:
        print("\n🎉 MISE À JOUR TERMINÉE AVEC SUCCÈS!")
    else:
        print("\n❌ ÉCHEC DE LA MISE À JOUR") 