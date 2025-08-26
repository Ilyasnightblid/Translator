import os
from googletrans import Translator
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

translator = Translator()

def translate_text(text, target_language, source_language='auto'):
    """Translate text using Google Translate API"""
    try:
        if source_language == target_language:
            return text
        
        result = translator.translate(text, src=source_language, dest=target_language)
        return result.text
    except Exception as e:
        return f"Erreur de traduction: {str(e)}"

def detect_language(text):
    """Detect the language of the given text"""
    try:
        detected = detect(text)
        return detected
    except LangDetectException:
        return 'auto'

def allowed_file(filename, extensions=None):
    """Check if file extension is allowed"""
    if extensions is None:
        extensions = ['txt', 'json']
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions

def get_language_name(code):
    """Get language name from language code"""
    languages = {
        'en': 'Anglais',
        'fr': 'Français',
        'es': 'Espagnol',
        'de': 'Allemand',
        'it': 'Italien',
        'pt': 'Portugais',
        'ru': 'Russe',
        'ja': 'Japonais',
        'ko': 'Coréen',
        'zh': 'Chinois',
        'ar': 'Arabe',
        'auto': 'Détection automatique'
    }
    return languages.get(code, code.upper())
