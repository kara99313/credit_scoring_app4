"""
Script de débogage pour comprendre le problème d'import du modèle
"""
import os
import sys

# Ajout de tous les imports possibles avant de charger le modèle
print("🔍 DÉBOGAGE DU MODÈLE")
print("=" * 50)

# Imports sklearn complets
print("\n📦 IMPORTS SKLEARN COMPLETS...")
try:
    import sklearn
    from sklearn.linear_model import LogisticRegression
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler, RobustScaler
    from sklearn.pipeline import Pipeline
    from sklearn.base import BaseEstimator, TransformerMixin
    from sklearn.metrics import accuracy_score, roc_auc_score
    print("✅ Tous les imports sklearn réussis")
except Exception as e:
    print(f"❌ Erreur import sklearn: {e}")

# Ajout des chemins du projet
sys.path.append('.')
sys.path.append('src')
sys.path.append('modeling')

# Test d'ouverture du fichier modèle
model_path = "modeling/models/best_model.pkl"
print(f"\n🔍 ANALYSE DU FICHIER MODÈLE: {model_path}")
print(f"Fichier existe: {os.path.exists(model_path)}")

if os.path.exists(model_path):
    print(f"Taille du fichier: {os.path.getsize(model_path)} bytes")
    
    # Tentative de lecture du contenu du pickle sans le désérialiser
    print("\n📋 CONTENU DU PICKLE (premiers bytes):")
    with open(model_path, 'rb') as f:
        first_bytes = f.read(200)
        print(f"Premiers bytes: {first_bytes[:100]}")
    
    # Tentative de chargement avec gestion d'erreur détaillée
    print("\n🔄 TENTATIVE DE CHARGEMENT...")
    try:
        import pickle
        
        # Création d'un unpickler personnalisé pour voir ce qui pose problème
        class DebugUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                print(f"Recherche classe: {module}.{name}")
                try:
                    return super().find_class(module, name)
                except Exception as e:
                    print(f"❌ Erreur pour {module}.{name}: {e}")
                    raise
        
        with open(model_path, 'rb') as f:
            unpickler = DebugUnpickler(f)
            model = unpickler.load()
        
        print(f"✅ Modèle chargé avec succès: {type(model)}")
        
        # Test de base
        if hasattr(model, 'predict_proba'):
            print("✅ Méthode predict_proba disponible")
        
    except Exception as e:
        print(f"❌ Erreur chargement détaillée: {e}")
        print(f"Type d'erreur: {type(e)}")
        
        # Si c'est un problème d'import spécifique, on essaie de l'importer
        error_str = str(e)
        if "CalibratedClassifierCV" in error_str:
            print("\n🔧 TENTATIVE DE CORRECTION CalibratedClassifierCV...")
            try:
                # Import explicite
                from sklearn.calibration import CalibratedClassifierCV
                print("✅ CalibratedClassifierCV importé")
                
                # Re-tentative de chargement
                import pickle
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                print(f"✅ Modèle chargé après correction: {type(model)}")
                
            except Exception as e2:
                print(f"❌ Échec après correction: {e2}")

print("\n" + "=" * 50)
print("Analyse terminée") 