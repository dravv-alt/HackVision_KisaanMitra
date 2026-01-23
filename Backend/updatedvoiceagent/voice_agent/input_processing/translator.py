"""
Translator Module - Hindi ↔ English Translation
Uses Argos Translate for offline translation
"""

import argostranslate.package
import argostranslate.translate
from typing import Optional


class ArgosTranslator:
    """
    Argos Translate-based translator for Hindi ↔ English
    Offline translation with no API dependencies
    """
    
    def __init__(self):
        """Initialize Argos Translate with Hindi-English packages"""
        self.initialized = False
        self._install_packages()
    
    def _install_packages(self):
        """Install required translation packages"""
        try:
            # Update package index
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            
            # Install Hindi to English
            hi_to_en = next(
                (pkg for pkg in available_packages 
                 if pkg.from_code == "hi" and pkg.to_code == "en"),
                None
            )
            if hi_to_en and not hi_to_en.is_installed():
                argostranslate.package.install_from_path(hi_to_en.download())
            
            # Install English to Hindi
            en_to_hi = next(
                (pkg for pkg in available_packages 
                 if pkg.from_code == "en" and pkg.to_code == "hi"),
                None
            )
            if en_to_hi and not en_to_hi.is_installed():
                argostranslate.package.install_from_path(en_to_hi.download())
            
            self.initialized = True
            print("✅ Argos Translate packages installed successfully")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not install Argos Translate packages: {e}")
            print("   Translation will use fallback method")
            self.initialized = False
    
    def hindi_to_english(self, hindi_text: str) -> str:
        """
        Translate Hindi text to English
        
        Args:
            hindi_text: Hindi input text
        
        Returns:
            English translation
        """
        if not self.initialized:
            return self._fallback_translate(hindi_text, "hi_to_en")
        
        try:
            translated = argostranslate.translate.translate(
                hindi_text,
                from_code="hi",
                to_code="en"
            )
            return translated
        except Exception as e:
            print(f"⚠️  Translation error: {e}, using fallback")
            return self._fallback_translate(hindi_text, "hi_to_en")
    
    def english_to_hindi(self, english_text: str) -> str:
        """
        Translate English text to Hindi
        
        Args:
            english_text: English input text
        
        Returns:
            Hindi translation
        """
        if not self.initialized:
            return self._fallback_translate(english_text, "en_to_hi")
        
        try:
            translated = argostranslate.translate.translate(
                english_text,
                from_code="en",
                to_code="hi"
            )
            return translated
        except Exception as e:
            print(f"⚠️  Translation error: {e}, using fallback")
            return self._fallback_translate(english_text, "en_to_hi")
    
    def _fallback_translate(self, text: str, direction: str) -> str:
        """
        Fallback translation using basic dictionary
        Only used if Argos Translate fails
        """
        # Basic fallback - return original text
        # In production, this could use a simple dictionary
        print(f"⚠️  Using fallback translation for: {text[:50]}...")
        return text


# Singleton instance
_translator = None

def get_translator() -> ArgosTranslator:
    """Get or create translator instance"""
    global _translator
    if _translator is None:
        _translator = ArgosTranslator()
    return _translator
