"""Gestionnaire de stockage local pour Sommelier Zero Tracas."""

import logging
from typing import Any, Dict, List, Optional
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

_LOGGER = logging.getLogger(__name__)

STORAGE_KEY = "sommelier_zero_tracas_cave"
STORAGE_VERSION = 1


class SommelierStorage:
    """Gestion de la base de données locale de la cave à vin."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialise le stockage HA."""
        self.hass = hass
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._data: Dict[str, Any] = {"vins": []}

    async def async_load(self) -> None:
        """Charge les données depuis le fichier JSON local."""
        stored = await self._store.async_load()
        if stored and isinstance(stored, dict):
            self._data = stored
        else:
            self._data = {"vins": []}
            await self._async_save()

    async def _async_save(self) -> None:
        """Sauvegarde les données sur le disque."""
        await self._store.async_save(self._data)

    def get_all_wines(self) -> List[Dict[str, Any]]:
        """Retourne la liste complète des vins en cave."""
        return self._data.get("vins", [])

    async def async_add_or_update_wine(self, wine_info: Dict[str, Any], quantite_ajout: int = 1) -> Dict[str, Any]:
        """Ajoute un vin ou incrémente sa quantité s'il existe déjà."""
        vins = self._data.setdefault("vins", [])
        
        # Recherche d'un doublon (Même domaine, cuvée et millésime)
        domaine = wine_info.get("domaine")
        cuvee = wine_info.get("cuvee")
        millesime = wine_info.get("millesime")

        wine_entry = None
        for v in vins:
            if (
                v.get("domaine") == domaine
                and v.get("cuvee") == cuvee
                and v.get("millesime") == millesime
            ):
                wine_entry = v
                break

        if wine_entry:
            # Incrémentation de la quantité
            wine_entry["quantite"] = wine_entry.get("quantite", 0) + quantite_ajout
            _LOGGER.info("Stock mis à jour pour %s (Nouveau stock : %s)", domaine, wine_entry["quantite"])
        else:
            # Création d'une nouvelle fiche
            wine_entry = {
                "id": f"{domaine}_{millesime}_{len(vins)+1}".replace(" ", "_").lower(),
                "domaine": domaine,
                "cuvee": cuvee,
                "millesime": millesime,
                "appellation": wine_info.get("appellation"),
                "region": wine_info.get("region"),
                "couleur": wine_info.get("couleur"),
                "cepages": wine_info.get("cepages"),
                "garde_conseillee_annees": wine_info.get("garde_conseillee_annees"),
                "accord_mets": wine_info.get("accord_mets"),
                "description_sommelier": wine_info.get("description_sommelier"),
                "quantite": quantite_ajout,
                "note": None,  # Note sur 5
                "aime": None,  # True / False
                "commentaire_perso": None,
            }
            vins.append(wine_entry)
            _LOGGER.info("Nouveau vin ajouté en cave : %s %s", domaine, millesime)

        await self._async_save()
        return wine_entry

    async def async_update_appreciation(self, wine_id: str, note: Optional[int] = None, aime: Optional[bool] = None, commentaire: Optional[str] = None) -> bool:
        """Met à jour la note et l'avis sur un vin."""
        for v in self._data.get("vins", []):
            if v.get("id") == wine_id:
                if note is not None:
                    v["note"] = note
                if aime is not None:
                    v["aime"] = aime
                if commentaire is not None:
                    v["commentaire_perso"] = commentaire
                await self._async_save()
                return True
        return False
