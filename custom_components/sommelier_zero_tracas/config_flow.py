"""Flux de configuration pour Sommelier Zero Tracas."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)
DOMAIN = "sommelier_zero_tracas"

class SommelierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gère le flux de configuration de l'intégration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Étape d'initialisation par l'utilisateur."""
        errors = {}

        if user_input is not None:
            api_key = user_input.get("api_key")
            
            # Validation de la présence de la clé sans import externe
            if not api_key:
                errors["base"] = "invalid_api_key"
            else:
                return self.async_create_entry(
                    title="Sommelier Zero Tracas",
                    data={"api_key": api_key}
                )

        schema = vol.Schema({
            vol.Required("api_key"): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )
