"""Initialisation de l'intégration Sommelier Zero Tracas pour Home Assistant."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)
DOMAIN = "sommelier_zero_tracas"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configuration de l'intégration via l'interface UI."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    _LOGGER.info("Sommelier Zero Tracas est correctement chargé !")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Déchargement de l'intégration."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
