"""
Script pour mettre à jour le rapport markdown principal avec les dernières données
"""

import os
import json
from datetime import datetime

def update_main_report():
    """
    Met à jour le rapport markdown principal avec les dernières données de validation
    """
    print("📝 MISE À JOUR DU RAPPORT PRINCIPAL")
    print("=" * 50)
    
    # 1. Trouver le dernier rapport de validation
    validation_dir = "modeling/validation"
    reports = [f for f in os.listdir(validation_dir) if f.startswith("validation_report_") and f.endswith(".json")]
    
    if not reports:
        print("❌ Aucun rapport de validation trouvé")
        return False
    
    reports.sort()
    latest_report = reports[-1]
    latest_timestamp = latest_report.replace("validation_report_", "").replace(".json", "")
    
    print(f"📋 Dernier rapport: {latest_report}")
    print(f"⏰ Timestamp: {latest_timestamp}")
    
    # 2. Charger les données du dernier rapport
    report_path = os.path.join(validation_dir, latest_report)
    with open(report_path, 'r', encoding='utf-8') as f:
        latest_data = json.load(f)
    
    # 3. Mettre à jour le rapport principal
    main_report_path = "modeling/documentation/RAPPORT_ETAPE_6_BACKTESTING_VALIDATION.md"
    
    if not os.path.exists(main_report_path):
        print(f"❌ Rapport principal non trouvé: {main_report_path}")
        return False
    
    # Lire le contenu actuel
    with open(main_report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n📄 MISE À JOUR DU CONTENU")
    print("-" * 40)
    
    # Mettre à jour la date
    current_date = datetime.now().strftime("%d %B %Y")
    content = content.replace("20 Juin 2025", current_date)
    
    # Créer la section d'historique des validations
    history_section = f"""

---

## 📅 HISTORIQUE DES VALIDATIONS

### **Dernière Validation Effectuée**
**Timestamp :** `{latest_timestamp}`  
**Date :** {datetime.now().strftime('%d/%m/%Y à %H:%M')}  
**Méthode :** {latest_data['validation_summary']['validation_method']}  

### **Résultats de la Dernière Validation**
- **Status :** {'✅ APPROUVÉ' if latest_data['final_assessment']['production_ready'] else '❌ REJETÉ'}
- **AUC-ROC :** {latest_data['base_performance']['auc_roc']:.4f}
- **KS Statistic :** {latest_data['base_performance']['ks_statistic']:.4f}
- **Gini Coefficient :** {latest_data['base_performance']['gini_coefficient']:.4f}
- **Niveau de Risque :** {latest_data['final_assessment']['risk_level']}
- **Recommandation :** {latest_data['final_assessment']['recommendation']}

### **Tests de Stress - Dernière Validation**
"""
    
    for scenario, results in latest_data['stress_tests'].items():
        history_section += f"- **{scenario.title()} :** AUC = {results['auc_roc']:.4f}, Dégradation = {results['degradation']:.4f}\n"
    
    history_section += f"""

### **Conformité Réglementaire - Dernière Validation**
"""
    
    for criterion, status in latest_data['regulatory_compliance'].items():
        status_icon = "✅" if status else "❌"
        history_section += f"- {criterion} : {status_icon}\n"
    
    history_section += f"""

### **Évolution des Validations**

| Timestamp | Status | AUC-ROC | Recommandation |
|-----------|--------|---------|----------------|"""
    
    # Ajouter toutes les validations
    for report in reports:
        timestamp = report.replace("validation_report_", "").replace(".json", "")
        report_path_temp = os.path.join(validation_dir, report)
        
        with open(report_path_temp, 'r', encoding='utf-8') as f:
            data_temp = json.load(f)
        
        status = "✅ APPROUVÉ" if data_temp['final_assessment']['production_ready'] else "❌ REJETÉ"
        auc = data_temp['base_performance']['auc_roc']
        recommendation = data_temp['final_assessment']['recommendation']
        
        history_section += f"\n| `{timestamp}` | {status} | {auc:.4f} | {recommendation} |"
    
    history_section += f"""

### **Conclusion de l'Historique**
- **Nombre total de validations :** {len(reports)}
- **Validations réussies :** {sum(1 for r in reports if json.load(open(os.path.join(validation_dir, r), 'r'))['final_assessment']['production_ready'])}
- **Dernière décision :** {'✅ MODÈLE APPROUVÉ POUR PRODUCTION' if latest_data['final_assessment']['production_ready'] else '❌ MODÈLE REJETÉ'}

---

*Section d'historique mise à jour automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*

"""
    
    # Ajouter ou remplacer la section d'historique
    if "## 📅 HISTORIQUE DES VALIDATIONS" in content:
        # Remplacer la section existante
        start_marker = "## 📅 HISTORIQUE DES VALIDATIONS"
        start_idx = content.find(start_marker)
        
        if start_idx != -1:
            # Chercher la fin de la section (prochaine section ## ou fin du fichier)
            end_idx = content.find("\n## ", start_idx + len(start_marker))
            if end_idx == -1:
                end_idx = len(content)
            
            content = content[:start_idx] + history_section + "\n" + content[end_idx:]
        else:
            content = content + history_section
    else:
        # Ajouter la section à la fin
        content = content + history_section
    
    # Sauvegarder le rapport mis à jour
    with open(main_report_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Rapport principal mis à jour: {main_report_path}")
    print(f"✅ Section d'historique ajoutée avec {len(reports)} validations")
    print(f"✅ Dernière validation: {latest_timestamp}")
    
    return True

if __name__ == "__main__":
    success = update_main_report()
    if success:
        print("\n🎉 MISE À JOUR DU RAPPORT PRINCIPAL RÉUSSIE!")
    else:
        print("\n❌ ÉCHEC DE LA MISE À JOUR") 