"""Moteur IA et logique de gestion de cave pour Sommelier Zero Tracas."""
import logging
import json
import base64
import aiohttp

_LOGGER = logging.getLogger(__name__)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

class SommelierAiEngine:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def analyze_label(self, image_bytes: bytes, user_preferences: dict) -> dict:
        """Analyse l'étiquette scannée via l'IA et génère la fiche du vin."""
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        
        prompt = f"""
        Tu es un sommelier expert et pédagogique. Analyse cette étiquette de vin.
        Retourne STRICTEMENT un objet JSON valide avec la structure suivante :
        {{
            "domaine": "Nom du domaine ou château",
            "nom_cuvee": "Nom de la cuvée ou Appellation",
            "millesime": "Année (ex: 2020) ou Non précisé",
            "cepages": ["Cépage 1", "Cépage 2"],
            "profil_gustatif": {{
                "puissance": "Léger / Moyen / Puissant",
                "fruite": "Peu fruité / Fruité / Très fruité",
                "aromes": ["Arôme 1", "Arôme 2"]
            }},
            "description_simple": "Description courte et accessible du goût (sans jargon).",
            "fourchette_prix": "Ex: 12€ - 15€",
            "accords_mets": ["Plat 1", "Plat 2"],
            "score_compatibilite": 85,
            "explication_compatibilite": "Pourquoi ce vin correspond (ou non) aux goûts de l'utilisateur."
        }}

        Préférences actuelles de l'utilisateur basées sur ses notes passées :
        {json.dumps(user_preferences, ensure_ascii=False)}
        """

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}}
                ]
            }]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{GEMINI_API_URL}?key={self.api_key}", json=payload) as response:
                if response.status != 200:
                    _LOGGER.error("Erreur lors de l'appel à l'API IA: %s", await response.text())
                    return {"error": "Impossible d'analyser l'image."}
                
                result = await response.json()
                try:
                    text_response = result['candidates'][0]['content']['parts'][0]['text']
                    clean_json = text_response.replace("```json", "").replace("```", "").strip()
                    return json.loads(clean_json)
                except (KeyError, json.JSONDecodeError) as err:
                    _LOGGER.error("Erreur de formatage JSON de l'IA: %s", err)
                    return {"error": "Réponse IA illisible."}

    def process_scan(self, wine_data: dict, current_inventory: list) -> dict:
        """Détermine si le vin est déjà en cave (re-scan) ou s'il s'agit d'un ajout."""
        wine_id = f"{wine_data.get('domaine')}_{wine_data.get('nom_cuvee')}_{wine_data.get('millesime')}".lower().replace(" ", "_")
        
        for item in current_inventory:
            if item.get("id") == wine_id and item.get("stock", 0) > 0:
                return {
                    "action": "rescan_exit",
                    "wine_id": wine_id,
                    "message": f"Bouteille trouvée en cave ({item['domaine']}). Voulez-vous la sortir du stock et la noter ?",
                    "data": item
                }
        
        return {
            "action": "new_scan_entry",
            "wine_id": wine_id,
            "message": "Nouveau vin détecté.",
            "data": wine_data
        }
