"""Moteur d'intelligence artificielle Gemini pour Sommelier Zero Tracas."""
import asyncio
import json
import logging

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
    """Gestionnaire des appels à l'API Gemini via google-genai."""

    def __init__(self, api_key: str):
        """Initialise le moteur avec la clé API."""
        self.api_key = api_key

    def _sync_analyze(self, image_bytes: bytes) -> dict:
        """Exécution synchrone isolée dans un thread pour éviter les appels bloquants HA."""
        from google import genai
        from google.genai import types

        client = genai.Client(
            api_key=self.api_key,
            http_options=types.HttpOptions(api_version="v1"),
        )

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/jpeg",
        )

        config = types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            )
        )

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[PROMPT_ANALYSE_ETIQUETTE, image_part],
            config=config,
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        return json.loads(raw_text.strip())

    async def analyze_wine_label(self, image_bytes: bytes) -> dict:
        """Envoie l'image de l'étiquette à Gemini hors de la boucle d'événements HA."""
        try:
            return await asyncio.to_thread(self._sync_analyze, image_bytes)
        except Exception as err:
            _LOGGER.error("Erreur lors de l'analyse Gemini : %s", err)
            return {"error": str(err)}
