"""Moteur d'intelligence artificielle Gemini pour Sommelier Zero Tracas."""
import logging
import json
import google.generativeai as genai

_LOGGER = logging.getLogger(__name__)

PROMPT_ANALYSE_ETIQUETTE = """
Tu es un sommelier expert. Analyse cette photo d'étiquette de vin et extrais les informations suivantes.
Réponds EXCLUSIVEMENT sous la forme d'un objet JSON valide sans balises Markdown supplémentaires, avec cette structure exacte :

{
  "domaine": "Nom du domaine ou chateau",
  "cuvee": "Nom de la cuvee s'il y en a une, sinon null",
  "millesime": 2020,
  "appellation": "AOP/AOC/IGP (ex: Saint-Emilion, Cotes du Rhone)",
  "region": "Region viticole (ex: Bordeaux, Val de Loire)",
  "couleur": "Rouge, Blanc, Rose, ou Etincelant",
  "cepages": ["Cepage 1", "Cepage 2"],
  "garde_conseillee_annees": "Plage d'apogee recommandee (ex: 2025-2030)",
  "accord_mets": ["Accord 1", "Accord 2"],
  "description_sommelier": "Une courte description du profil gustatif en 2 phrases."
}

Si une information est illisible ou absente, met la valeur null.
"""

class SommelierAIEngine:
    """Gestionnaire des appels à l'API Gemini."""

    def __init__(self, api_key: str):
        """Initialise le moteur avec la clé API."""
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def analyze_wine_label(self, image_bytes: bytes) -> dict:
        """Envoie l'image de l'étiquette à Gemini et retourne les données du vin."""
        try:
            image_data = {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }

            response = await self.model.generate_content_async(
                [PROMPT_ANALYSE_ETIQUETTE, image_data]
            )

            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]

            return json.loads(raw_text.strip())

        except Exception as err:
            _LOGGER.error("Erreur lors de l'analyse Gemini : %s", err)
            return {"error": str(err)}
