"""Flux de configuration pour Sommelier Zero Tracas."""
import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "sommelier_zero_tracas"

class SommelierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gère le formulaire d'installation du composant."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Sommelier Zero Tracas",
                data=user_input
            )

        data_schema = vol.Schema({
            vol.Required("api_key"): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "api_info": "Obtenez votre clé gratuite en 1 clic sur [Google AI Studio](https://aistudio.google.com/app/apikey)."
            }
        )
