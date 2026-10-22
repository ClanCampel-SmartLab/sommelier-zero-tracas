"""Capteur pour Sommelier Zero Tracas."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .ai_engine import SommelierAIEngine

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration de la plateforme de capteur."""
    async_add_entities([SommelierCaveSensor(entry)], True)

class SommelierCaveSensor(SensorEntity):
    """Capteur représentant le statut de la cave."""

    def __init__(self, entry: ConfigEntry):
        """Initialisation du capteur."""
        self._attr_name = "Sommelier Zero Tracas Cave"
        self._attr_unique_id = f"{entry.entry_id}_cave"
        self._attr_icon = "mdi:wine"
        self._attr_native_value = 0

    @property
    def extra_state_attributes(self):
        """Attributs supplémentaires du capteur."""
        return {
            "statut": "Opérationnel",
            "bouteilles_totales": 0
        }
