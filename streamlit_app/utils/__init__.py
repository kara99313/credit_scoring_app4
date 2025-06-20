"""
Utilities package for Credit Scoring Dashboard
"""

from .model_loader import ModelLoader
from .data_processor import CreditScoringProcessor

# Alias pour compatibilité
ModelManager = ModelLoader

__all__ = ['ModelLoader', 'ModelManager', 'CreditScoringProcessor'] 