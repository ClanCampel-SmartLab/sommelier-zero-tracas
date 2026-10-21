"""Initialisation de l'integration Sommelier Zero Tracas."""
import logging
import os
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry

from .ai_engine import SommelierAIEngine

_LOGGER = logging.getLogger(__name__)
DOMAIN = "sommelier_zero_tracas"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configuration de l'integration depuis l'UI."""
    api_key = entry.data.get("api_key")
    ai_engine = SommelierAIEngine(api_key)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "engine": ai_engine,
        "inventory": []
    }

    async def handle_scan_etiquette(call: ServiceCall):
        """Service pour scanner une image de vin enregistree sur le serveur HA."""
        image_path = call.data.get("image_path")
        if not os.path.exists(image_path):
            _LOGGER.error("Fichier image introuvable : %s", image_path)
            return

        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()

        res = await ai_engine.analyze_wine_label(img_bytes)
        _LOGGER.info("Resultat de l'analyse Gemini : %s", res)
        
        # Publication d'un evenement Home Assistant avec le resultat
        hass.bus.async_fire("sommelier_wine_scanned", {"result": res})

    hass.services.async_register(
        DOMAIN,
        "scan_etiquette",
        handle_scan_etiquette,
        schema=vol.Schema({
            vol.Required("image_path"): cv.string,
        })
    )

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Dechargement de l'integration."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
