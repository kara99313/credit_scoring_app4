"""
Localization Module for Credit Scoring System

This module provides multilingual support for the credit scoring application.

Author: Credit Scoring Team
Created: 2024
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
import logging


class Localizer:
    """
    Handles localization and internationalization for the application.
    
    Supports multiple languages with dynamic loading of translation files.
    """
    
    def __init__(self, default_language: str = "fr", translations_path: str = "locales"):
        """
        Initialize the localizer.
        
        Args:
            default_language: Default language code (fr, en, es, de)
            translations_path: Path to translation files
        """
        self.default_language = default_language
        self.current_language = default_language
        self.translations_path = Path(translations_path)
        self.translations: Dict[str, Dict] = {}
        
        # Load all available translations
        self._load_translations()
        
        logging.info(f"Localizer initialized with default language: {default_language}")
    
    def _load_translations(self) -> None:
        """Load all translation files from the translations directory."""
        try:
            if not self.translations_path.exists():
                logging.warning(f"Translations path not found: {self.translations_path}")
                return
            
            # Load translations for each supported language
            for lang_dir in self.translations_path.iterdir():
                if lang_dir.is_dir() and lang_dir.name != "__pycache__":
                    lang_code = lang_dir.name
                    messages_file = lang_dir / "messages.json"
                    
                    if messages_file.exists():
                        try:
                            with open(messages_file, 'r', encoding='utf-8') as f:
                                self.translations[lang_code] = json.load(f)
                            logging.info(f"Loaded translations for language: {lang_code}")
                        except (json.JSONDecodeError, FileNotFoundError) as e:
                            logging.error(f"Error loading translations for {lang_code}: {e}")
            
            # Validate that default language is available
            if self.default_language not in self.translations:
                logging.warning(f"Default language '{self.default_language}' not found in translations")
                # Fallback to first available language
                if self.translations:
                    self.default_language = list(self.translations.keys())[0]
                    logging.info(f"Using fallback language: {self.default_language}")
                    
        except Exception as e:
            logging.error(f"Error loading translations: {e}")
    
    def set_language(self, language_code: str) -> bool:
        """
        Set the current language.
        
        Args:
            language_code: Language code to set (fr, en, es, de)
            
        Returns:
            True if language was set successfully, False otherwise
        """
        if language_code in self.translations:
            self.current_language = language_code
            logging.info(f"Language changed to: {language_code}")
            return True
        else:
            logging.warning(f"Language '{language_code}' not available")
            return False
    
    def get_available_languages(self) -> Dict[str, str]:
        """
        Get available languages with their display names.
        
        Returns:
            Dictionary mapping language codes to display names
        """
        language_names = {
            "fr": "Français",
            "en": "English", 
            "es": "Español",
            "de": "Deutsch"
        }
        
        return {
            code: language_names.get(code, code.upper())
            for code in self.translations.keys()
        }
    
    def get_text(self, key: str, **kwargs) -> str:
        """
        Get translated text for a given key.
        
        Args:
            key: Translation key in dot notation (e.g., 'app.title')
            **kwargs: Variables for string formatting
            
        Returns:
            Translated text or key if translation not found
        """
        try:
            # Get current language translations
            current_translations = self.translations.get(self.current_language, {})
            
            # Navigate through nested dictionary using dot notation
            keys = key.split('.')
            value = current_translations
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    # Fallback to default language
                    if self.current_language != self.default_language:
                        default_translations = self.translations.get(self.default_language, {})
                        value = default_translations
                        for k in keys:
                            if isinstance(value, dict) and k in value:
                                value = value[k]
                            else:
                                value = key  # Return key if not found
                                break
                    else:
                        value = key  # Return key if not found
                    break
            
            # If value is string, format with kwargs
            if isinstance(value, str) and kwargs:
                try:
                    value = value.format(**kwargs)
                except (KeyError, ValueError) as e:
                    logging.warning(f"Error formatting translation '{key}': {e}")
            
            return str(value)
            
        except Exception as e:
            logging.error(f"Error getting translation for key '{key}': {e}")
            return key
    
    def get_date_format(self) -> str:
        """Get date format for current language."""
        date_formats = {
            "fr": "%d/%m/%Y",
            "en": "%m/%d/%Y",
            "es": "%d/%m/%Y",
            "de": "%d.%m.%Y"
        }
        return date_formats.get(self.current_language, "%d/%m/%Y")
    
    def get_number_format(self) -> str:
        """Get number format for current language."""
        number_formats = {
            "fr": "european",
            "en": "american", 
            "es": "european",
            "de": "german"
        }
        return number_formats.get(self.current_language, "european")
    
    def format_number(self, number: float, decimals: int = 2) -> str:
        """
        Format number according to current language convention.
        
        Args:
            number: Number to format
            decimals: Number of decimal places
            
        Returns:
            Formatted number string
        """
        format_type = self.get_number_format()
        
        if format_type == "american":
            # American format: 1,234.56
            return f"{number:,.{decimals}f}"
        elif format_type == "german":
            # German format: 1.234,56
            formatted = f"{number:,.{decimals}f}"
            return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            # European format: 1 234,56
            formatted = f"{number:,.{decimals}f}"
            return formatted.replace(",", " ").replace(".", ",")
    
    def format_currency(self, amount: float, currency: str = "EUR") -> str:
        """
        Format currency according to current language convention.
        
        Args:
            amount: Amount to format
            currency: Currency code
            
        Returns:
            Formatted currency string
        """
        formatted_number = self.format_number(amount, 2)
        
        currency_symbols = {
            "EUR": "€",
            "USD": "$",
            "GBP": "£"
        }
        
        symbol = currency_symbols.get(currency, currency)
        
        if self.current_language == "en":
            return f"{symbol}{formatted_number}"
        else:
            return f"{formatted_number} {symbol}"
    
    def get_risk_class_translation(self, risk_class: str) -> str:
        """Get translated risk class name."""
        return self.get_text(f"risk_classes.{risk_class}")
    
    def get_decision_translation(self, decision: str) -> str:
        """Get translated decision name."""
        return self.get_text(f"decisions.{decision}")
    
    def validate_translations(self) -> Dict[str, Any]:
        """
        Validate translation completeness.
        
        Returns:
            Validation report
        """
        report = {
            "languages": list(self.translations.keys()),
            "missing_keys": {},
            "total_keys": 0,
            "completeness": {}
        }
        
        if not self.translations:
            return report
        
        # Use default language as reference
        reference_lang = self.default_language
        if reference_lang not in self.translations:
            reference_lang = list(self.translations.keys())[0]
        
        reference_translations = self.translations[reference_lang]
        
        def get_all_keys(d, prefix=""):
            """Recursively get all translation keys."""
            keys = []
            for k, v in d.items():
                full_key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    keys.extend(get_all_keys(v, full_key))
                else:
                    keys.append(full_key)
            return keys
        
        all_keys = get_all_keys(reference_translations)
        report["total_keys"] = len(all_keys)
        
        # Check each language for missing keys
        for lang_code, translations in self.translations.items():
            if lang_code == reference_lang:
                continue
                
            missing = []
            for key in all_keys:
                if not self._key_exists(translations, key):
                    missing.append(key)
            
            report["missing_keys"][lang_code] = missing
            report["completeness"][lang_code] = (
                (len(all_keys) - len(missing)) / len(all_keys) * 100
                if all_keys else 100
            )
        
        return report
    
    def _key_exists(self, translations: Dict, key: str) -> bool:
        """Check if a key exists in translations dictionary."""
        keys = key.split('.')
        current = translations
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return False
        
        return True


# Global localizer instance
_localizer = None


def get_localizer() -> Localizer:
    """Get global localizer instance."""
    global _localizer
    if _localizer is None:
        _localizer = Localizer()
    return _localizer


def init_localizer(default_language: str = "fr", translations_path: str = "locales") -> Localizer:
    """Initialize global localizer."""
    global _localizer
    _localizer = Localizer(default_language, translations_path)
    return _localizer


def t(key: str, **kwargs) -> str:
    """
    Shorthand function for getting translations.
    
    Args:
        key: Translation key
        **kwargs: Variables for string formatting
        
    Returns:
        Translated text
    """
    return get_localizer().get_text(key, **kwargs)


def set_language(language_code: str) -> bool:
    """Set current language."""
    return get_localizer().set_language(language_code)


def get_available_languages() -> Dict[str, str]:
    """Get available languages."""
    return get_localizer().get_available_languages() 