"""Intégration Sommelier Zero Tracas pour Home Assistant."""

import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .ai_engine import SommelierAIEngine
from .storage import SommelierStorage

_LOGGER = logging.getLogger(__name__)

DOMAIN = "sommelier_zero_tracas"
SERVICE_SCAN_WINE = "scan_wine"

SERVICE_SCAN_SCHEMA = vol.Schema(
    {
        vol.Required("image_path"): cv.string,
        vol.Optional("quantite", default=1): cv.positive_int,
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initialise l'intégration depuis une entrée de configuration."""
    api_key = entry.data.get("api_key")

    if not api_key:
        _LOGGER.error("Clé API Gemini manquante.")
        return False

    ai_engine = SommelierAIEngine(api_key=api_key)
    storage = SommelierStorage(hass)

    # Chargement de la base de données locale JSON
    await storage.async_load()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "ai_engine": ai_engine,
        "storage": storage,
    }

    async def handle_scan_wine(call: ServiceCall) -> None:
        """Service pour scanner une étiquette et l'ajouter automatiquement à la cave."""
        image_path = call.data["image_path"]
        quantite = call.data.get("quantite", 1)

        try:
            # Lecture du fichier image
            def read_image():
                with open(image_path, "rb") as image_file:
                    return image_file.read()

            image_bytes = await hass.async_add_executor_job(read_image)
        except Exception as err:
            _LOGGER.error("Impossible de lire l'image %s : %s", image_path, err)
            return

        # Analyse par Gemini
        res_ai = await ai_engine.analyze_wine_label(image_bytes)

        if "error" in res_ai:
            _LOGGER.error("Échec de l'analyse IA : %s", res_ai["error"])
            return

        # Sauvegarde ou incrémentation en cave via storage
        wine_entry = await storage.async_add_or_update_wine(
            wine_info=res_ai, quantite_ajout=quantite
        )

        _LOGGER.info(
            "Résultat de l'analyse Gemini enregistrée en cave : %s", wine_entry
        )

        # Notification événementielle dans HA (pour automatisations / cartes Lovelace)
        hass.bus.async_fire(
            f"{DOMAIN}_wine_scanned",
            {"wine": wine_entry},
        )

    # Enregistrement du service dans Home Assistant
    hass.services.async_register(
        DOMAIN,
        SERVICE_SCAN_WINE,
        handle_scan_wine,
        schema=SERVICE_SCAN_SCHEMA,
    )

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Décharge l'intégration."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, ["sensor"]
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
