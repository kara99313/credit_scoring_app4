"""
Credit Scoring System - Source Package

This package contains the core modules for the credit scoring system:
- data_processing: Data loading, cleaning and validation
- feature_engineering: Feature creation and transformation
- modeling: Machine learning model training and evaluation
- backtesting: Model validation and performance testing
- utils: Utility functions and helpers

Author: Credit Scoring Team
Created: 2024
"""

__version__ = "1.0.0"
__author__ = "Credit Scoring Team"

# Import main classes for easy access
from .data_processing import DataProcessor
from .utils import setup_logging, load_config

# Import transformers
try:
    from .transformers.feature_engineer import FeatureEngineer
    from .transformers.variable_transformer import VariableTransformer
except ImportError:
    FeatureEngineer = None
    VariableTransformer = None

__all__ = [
    "DataProcessor",
    "setup_logging",
    "load_config"
]

# Add transformers if available
if FeatureEngineer is not None:
    __all__.extend(["FeatureEngineer", "VariableTransformer"]) 