"""
Utility Functions for Credit Scoring System

This module contains common utility functions used across the credit scoring system.

Author: Credit Scoring Team
Created: 2024
"""

import os
import logging
import logging.config
import yaml
import json
import pickle
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


def setup_logging(
    config_path: str = "config/logging_config.yaml",
    default_level: int = logging.INFO
) -> None:
    """
    Setup logging configuration.
    
    Args:
        config_path: Path to logging configuration file
        default_level: Default logging level if config file not found
    """
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            level=default_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/app.log')
            ]
        )
    
    logging.info("Logging configuration loaded successfully")


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is malformed
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        logging.info(f"Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error parsing configuration file: {e}")
        raise


def save_model(
    model: Any,
    filepath: str,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Save model to disk with metadata.
    
    Args:
        model: Model object to save
        filepath: Path to save the model
        metadata: Optional metadata to save with model
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save model
    if filepath.endswith('.pkl'):
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
    else:
        joblib.dump(model, filepath)
    
    # Save metadata if provided
    if metadata:
        metadata_path = filepath.replace('.pkl', '_metadata.json').replace('.joblib', '_metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, default=str)
    
    logging.info(f"Model saved to {filepath}")


def load_model(filepath: str) -> Tuple[Any, Optional[Dict[str, Any]]]:
    """
    Load model from disk with metadata.
    
    Args:
        filepath: Path to model file
        
    Returns:
        Tuple of (model, metadata)
    """
    # Load model
    if filepath.endswith('.pkl'):
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
    else:
        model = joblib.load(filepath)
    
    # Load metadata if exists
    metadata_path = filepath.replace('.pkl', '_metadata.json').replace('.joblib', '_metadata.json')
    metadata = None
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    
    logging.info(f"Model loaded from {filepath}")
    return model, metadata


def calculate_ks_statistic(y_true: np.ndarray, y_proba: np.ndarray) -> float:
    """
    Calculate Kolmogorov-Smirnov statistic.
    
    Args:
        y_true: True binary labels
        y_proba: Predicted probabilities
        
    Returns:
        KS statistic value
    """
    from scipy.stats import ks_2samp
    
    # Split predictions by actual class
    pos_scores = y_proba[y_true == 1]
    neg_scores = y_proba[y_true == 0]
    
    # Calculate KS statistic
    ks_stat, _ = ks_2samp(pos_scores, neg_scores)
    return ks_stat


def calculate_gini_coefficient(y_true: np.ndarray, y_proba: np.ndarray) -> float:
    """
    Calculate Gini coefficient from ROC AUC.
    
    Args:
        y_true: True binary labels
        y_proba: Predicted probabilities
        
    Returns:
        Gini coefficient
    """
    from sklearn.metrics import roc_auc_score
    
    auc = roc_auc_score(y_true, y_proba)
    gini = 2 * auc - 1
    return gini


def calculate_psi(
    expected: np.ndarray,
    actual: np.ndarray,
    buckets: int = 10
) -> float:
    """
    Calculate Population Stability Index (PSI).
    
    Args:
        expected: Expected (reference) distribution
        actual: Actual (current) distribution
        buckets: Number of buckets for binning
        
    Returns:
        PSI value
    """
    # Create bins based on expected distribution
    breakpoints = np.arange(0, buckets + 1) / buckets * 100
    
    # Calculate percentiles
    expected_percents = np.percentile(expected, breakpoints)
    
    # Bin both distributions
    expected_counts = np.histogram(expected, expected_percents)[0]
    actual_counts = np.histogram(actual, expected_percents)[0]
    
    # Convert to percentages
    expected_percents = expected_counts / len(expected)
    actual_percents = actual_counts / len(actual)
    
    # Avoid division by zero
    expected_percents = np.where(expected_percents == 0, 0.0001, expected_percents)
    actual_percents = np.where(actual_percents == 0, 0.0001, actual_percents)
    
    # Calculate PSI
    psi = np.sum((actual_percents - expected_percents) * np.log(actual_percents / expected_percents))
    
    return psi


def create_score_bands(
    probabilities: np.ndarray,
    score_min: int = 300,
    score_max: int = 850,
    reverse: bool = True
) -> np.ndarray:
    """
    Convert probabilities to credit scores.
    
    Args:
        probabilities: Default probabilities
        score_min: Minimum score value
        score_max: Maximum score value
        reverse: If True, lower probability = higher score
        
    Returns:
        Credit scores
    """
    if reverse:
        # Lower probability of default = higher score
        scores = score_max - (probabilities * (score_max - score_min))
    else:
        # Higher probability of default = higher score
        scores = score_min + (probabilities * (score_max - score_min))
    
    return np.round(scores).astype(int)


def assign_risk_class(
    scores: np.ndarray,
    risk_bands: Dict[str, List[int]]
) -> List[str]:
    """
    Assign risk classes based on scores.
    
    Args:
        scores: Credit scores
        risk_bands: Dictionary mapping risk levels to score ranges
        
    Returns:
        List of risk classes
    """
    risk_classes = []
    
    for score in scores:
        assigned = False
        for risk_level, (min_score, max_score) in risk_bands.items():
            if min_score <= score <= max_score:
                risk_classes.append(risk_level)
                assigned = True
                break
        
        if not assigned:
            risk_classes.append("unknown")
    
    return risk_classes


def validate_data_quality(
    df: pd.DataFrame,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validate data quality and return quality metrics.
    
    Args:
        df: DataFrame to validate
        config: Configuration dictionary
        
    Returns:
        Dictionary with quality metrics
    """
    quality_metrics = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_data': {},
        'duplicate_rows': df.duplicated().sum(),
        'data_types': df.dtypes.to_dict(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'quality_score': 0.0
    }
    
    # Missing data analysis
    missing_threshold = config.get('data', {}).get('max_missing_percentage', 0.3)
    
    for column in df.columns:
        missing_pct = df[column].isnull().sum() / len(df)
        quality_metrics['missing_data'][column] = {
            'count': df[column].isnull().sum(),
            'percentage': missing_pct,
            'acceptable': missing_pct <= missing_threshold
        }
    
    # Calculate overall quality score
    acceptable_columns = sum(
        1 for col_info in quality_metrics['missing_data'].values()
        if col_info['acceptable']
    )
    
    quality_score = (
        (acceptable_columns / len(df.columns)) * 0.5 +
        ((len(df) - quality_metrics['duplicate_rows']) / len(df)) * 0.3 +
        (1 if quality_metrics['memory_usage_mb'] < 1000 else 0.8) * 0.2
    )
    
    quality_metrics['quality_score'] = round(quality_score, 3)
    
    return quality_metrics


def create_timestamp() -> str:
    """Create timestamp string for file naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_directory(path: str) -> None:
    """Ensure directory exists, create if not."""
    os.makedirs(path, exist_ok=True)


def get_memory_usage(df: pd.DataFrame) -> str:
    """Get formatted memory usage string."""
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    return f"{memory_mb:.2f} MB"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage string."""
    return f"{value * 100:.{decimals}f}%"


def format_number(value: float, decimals: int = 2) -> str:
    """Format number with thousands separator."""
    return f"{value:,.{decimals}f}"


class Timer:
    """Context manager for timing operations."""
    
    def __init__(self, operation_name: str = "Operation"):
        self.operation_name = operation_name
        self.start_time = None
        
    def __enter__(self):
        self.start_time = datetime.now()
        logging.info(f"Starting {self.operation_name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = datetime.now() - self.start_time
        logging.info(f"{self.operation_name} completed in {duration}")


def log_dataframe_info(df: pd.DataFrame, name: str = "DataFrame") -> None:
    """Log basic information about a DataFrame."""
    logging.info(f"{name} shape: {df.shape}")
    logging.info(f"{name} memory usage: {get_memory_usage(df)}")
    logging.info(f"{name} missing values: {df.isnull().sum().sum()}")
    logging.info(f"{name} duplicates: {df.duplicated().sum()}")


# Configuration validation schemas
CONFIG_SCHEMA = {
    'project': {
        'required': ['name', 'version'],
        'optional': ['description']
    },
    'data': {
        'required': ['raw_data_path', 'processed_data_path', 'target_column'],
        'optional': ['external_data_path', 'max_missing_percentage']
    },
    'model': {
        'required': ['algorithm'],
        'optional': ['hyperparameters', 'hyperparameter_tuning']
    }
}


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration against schema.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if valid, False otherwise
    """
    try:
        for section, requirements in CONFIG_SCHEMA.items():
            if section not in config:
                logging.error(f"Missing required section: {section}")
                return False
                
            section_config = config[section]
            
            # Check required fields
            for field in requirements.get('required', []):
                if field not in section_config:
                    logging.error(f"Missing required field: {section}.{field}")
                    return False
        
        logging.info("Configuration validation passed")
        return True
        
    except Exception as e:
        logging.error(f"Configuration validation error: {e}")
        return False 