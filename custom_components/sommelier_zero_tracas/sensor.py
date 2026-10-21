"""Capteur d'inventaire pour Sommelier Zero Tracas."""
from homeassistant.helpers.entity import Entity
from .ai_engine import SommelierAIEngine

DOMAIN = "sommelier_zero_tracas"

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Configuration du capteur de cave."""
    api_key = config_entry.data.get("api_key")
    ai_engine = SommelierAIEngine(api_key)
    
    sensor = SommelierWineCellarSensor(hass, ai_engine)
    async_add_entities([sensor], True)

class SommelierWineCellarSensor(Entity):
    """Représente l'état de la cave à vin."""

    def __init__(self, hass, ai_engine):
        self.hass = hass
        self.ai_engine = ai_engine
        self._state = 0
        self._attr_unique_id = "sommelier_wine_cellar_total"
        self._attr_name = "Sommelier Cave à Vin"
        self._attr_icon = "mdi:wine"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "version": "1.0.0",
            "statut": "Prêt pour le scan",
            "derniere_analyse": "Aucune"
        }
