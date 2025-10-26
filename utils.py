from azure.storage.blob import BlobServiceClient
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
# --- FONCTIONS AZURE BLOB STORAGE ---

def get_blob_service_client():
    """
    Crée un client de service blob à partir de la chaîne de connexion
    stockée dans les variables d'environnement.
    """
    connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    if not connect_str:
        print("ERREUR: AZURE_STORAGE_CONNECTION_STRING n'est pas définie.")
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING n'est pas définie.")

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    return blob_service_client

def upload_to_blob(file_stream, container_name, blob_name):
    """
    Téléverse un flux de fichier (file.stream) vers Azure Blob Storage
    et retourne l'URL complète du blob.
    """
    try:
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Rembobiner le flux au début
        file_stream.seek(0)

        # Uploader le fichier
        blob_client.upload_blob(file_stream, overwrite=True)

        # Retourner l'URL publique
        return blob_client.url
    except Exception as e:
        print(f"Erreur lors de l'upload vers Azure Blob Storage: {e}")
        return None

def delete_blob(container_name, blob_url):
    """
    Supprime un blob d'Azure Storage en utilisant son URL complète.
    """
    # Ne pas essayer de supprimer l'URL par défaut
    DEFAULT_AVATAR_URL = "https://translatorstorageilyas.blob.core.windows.net/profile-photos/default_avatar.png"
    if blob_url == DEFAULT_AVATAR_URL:
        print("Ignorer la suppression de l'avatar par défaut.")
        return True

    # Ne pas essayer de supprimer si ce n'est pas une URL Azure
    if not blob_url.startswith('https://translatorstorageilyas.blob.core.windows.net'):
         print(f"Tentative de suppression d'un blob non-URL ignorée: {blob_url}")
         return True # Ignorer sans erreur

    try:
        blob_service_client = get_blob_service_client()

        # Extraire le nom du blob à partir de l'URL
        blob_name = blob_url.split(f'/{container_name}/')[-1]

        print(f"Tentative de suppression du blob: {blob_name}")

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        if blob_client.exists():
            blob_client.delete_blob()
            print(f"Blob {blob_name} supprimé.")
        else:
            print(f"Blob {blob_name} n'existe pas, suppression ignorée.")

        return True
    except Exception as e:
        print(f"Erreur lors de la suppression du blob {blob_url}: {e}")
        return False
