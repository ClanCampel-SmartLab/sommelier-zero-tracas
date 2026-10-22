"""Moteur d'intelligence artificielle Gemini pour Sommelier Zero Tracas."""

import asyncio
import json
import logging

_LOGGER = logging.getLogger(__name__)

# Alias de modele : sa version cible peut evoluer chez Google.
GEMINI_MODEL = "gemini-flash-latest"

PROMPT_ANALYSE_ETIQUETTE = """
Tu es un sommelier expert.

Analyse cette photo d'etiquette de vin et extrais les informations
lisibles. N'invente pas de faits sur ce vin.

Reponds exclusivement avec un objet JSON valide, sans balises Markdown,
avec exactement les cles suivantes :

{
  "domaine": "Nom du domaine ou chateau",
  "cuvee": "Nom de la cuvee s'il y en a une, sinon null",
  "millesime": 2020,
  "appellation": "AOP/AOC/IGP, par exemple Saint-Emilion",
  "region": "Region viticole, par exemple Bordeaux",
  "couleur": "Rouge, Blanc, Rose ou Etincelant",
  "cepages": ["Cepage 1", "Cepage 2"],
  "garde_conseillee_annees": "Plage d'apogee, par exemple 2025-2030",
  "accord_mets": ["Accord 1", "Accord 2"],
  "description_sommelier": "Courte description en deux phrases."
}

Regles :
- Si une information factuelle est illisible, absente ou incertaine,
  utilise la valeur JSON null, et non la chaine de caracteres "null".
- Le millesime doit etre un nombre entier ou null.
- Les cepages doivent etre une liste de textes ou null.
- Les accords mets doivent etre une liste de textes ou null.
- Les recommandations de garde, les accords et la description sont
  des estimations : indique-le clairement dans les textes concernes.
- Ne presente pas une estimation comme une information lue sur l'etiquette.
- Si la photo ne permet pas d'identifier suffisamment le vin, utilise
  null pour les recommandations et la description.
"""


class SommelierAIEngine:
    """Gestionnaire des appels a l'API Gemini via google-genai."""

    def __init__(self, api_key: str):
        """Initialise le moteur avec la cle API."""
        self.api_key = api_key.strip()

    def _sync_analyze(self, image_bytes: bytes) -> dict:
        """Execute l'appel synchrone dans un thread distinct."""
        from google import genai
        from google.genai import types

        if not self.api_key:
            raise ValueError("La cle API Gemini est vide.")

        if not image_bytes:
            raise ValueError("L'image envoyee est vide.")

        client = genai.Client(api_key=self.api_key)

        try:
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg",
            )

            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                automatic_function_calling=(
                    types.AutomaticFunctionCallingConfig(
                        disable=True,
                    )
                ),
            )

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[
                    PROMPT_ANALYSE_ETIQUETTE,
                    image_part,
                ],
                config=config,
            )

            raw_text = (response.text or "").strip()

            if not raw_text:
                raise ValueError(
                    "Gemini n'a renvoye aucun texte exploitable. "
                    "La reponse peut avoir ete bloquee ou etre incomplete."
                )

            try:
                result = json.loads(raw_text)
            except json.JSONDecodeError as err:
                raise ValueError(
                    "La reponse de Gemini n'est pas un JSON valide "
                    f"(ligne {err.lineno}, colonne {err.colno})."
                ) from err

            if not isinstance(result, dict):
                raise ValueError(
                    "Gemini a renvoye un JSON, mais pas un objet."
                )

            expected_keys = (
                "domaine",
                "cuvee",
                "millesime",
                "appellation",
                "region",
                "couleur",
                "cepages",
                "garde_conseillee_annees",
                "accord_mets",
                "description_sommelier",
            )

            # Conserve les cles attendues et complete les absentes.
            return {
                key: result.get(key)
                for key in expected_keys
            }

        finally:
            client.close()

    async def analyze_wine_label(self, image_bytes: bytes) -> dict:
        """Analyse l'image sans bloquer la boucle d'evenements HA."""
        try:
            return await asyncio.to_thread(
                self._sync_analyze,
                image_bytes,
            )
        except Exception as err:
            _LOGGER.exception(
                "Erreur lors de l'analyse Gemini avec le modele %s",
                GEMINI_MODEL,
            )
            return {"error": str(err)}
