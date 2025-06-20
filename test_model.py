"""Test du modèle principal"""
import pickle
import os

def test_model():
    print("🔍 Test du modèle principal")
    
    model_path = "modeling/models/best_model.pkl"
    
    if os.path.exists(model_path):
        print("✅ Fichier modèle trouvé")
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"✅ Modèle chargé avec succès")
            print(f"   Type: {type(model)}")
            
            # Test simple si possible
            if hasattr(model, 'predict'):
                print("✅ Modèle a une méthode predict")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur chargement: {e}")
            return False
    else:
        print("❌ Fichier modèle non trouvé")
        return False

if __name__ == "__main__":
    test_model() 