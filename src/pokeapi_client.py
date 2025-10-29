"""Module for fetching Pokémon data from the PokéAPI."""
from typing import Any, Dict, Optional
import httpx
from src.constants import POKEAPI_BASE_URL
from src.logger import get_logger

logger = get_logger(__name__)


async def fetch_pokemon_full_data(
    client: httpx.AsyncClient, pokemon_name: str
) -> Optional[Dict[str, Any]]:
    """Fetch Pokémon data including stats, types, and first move.

    Args:
        client: The HTTP client to use.
        pokemon_name: The name of the Pokémon to fetch.

    Returns:
        Dictionary of Pokémon data, or None if not found.
    """
    try:
        pokemon_url = f"{POKEAPI_BASE_URL}/pokemon/{pokemon_name.lower()}"
        logger.info("fetching_pokemon_data", pokemon=pokemon_name, url=pokemon_url)
        
        resp = await client.get(pokemon_url)
        if resp.status_code != 200:
            logger.warning(
                "pokemon_not_found",
                pokemon=pokemon_name,
                status_code=resp.status_code,
            )
            return None
            
        data = resp.json()
        base_stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
        types = [t["type"]["name"] for t in data["types"]]
        moves = data["moves"]
        
        if not moves:
            logger.warning("no_moves_found", pokemon=pokemon_name)
            return None
            
        # Use the first move for simplicity
        move_url = moves[0]["move"]["url"]
        move_resp = await client.get(move_url)
        if move_resp.status_code != 200:
            logger.warning("move_fetch_failed", pokemon=pokemon_name)
            return None
            
        move_data = move_resp.json()
        move_power = move_data.get("power", 50)
        move_type = move_data.get("type", {}).get("name", "normal")
        move_name = move_data.get("name", "tackle")
        move_effect = next(
            (
                e["effect"]
                for e in move_data.get("effect_entries", [])
                if e["language"]["name"] == "en"
            ),
            None,
        )
        
        logger.info("pokemon_data_fetched", pokemon=pokemon_name)
        return {
            "name": data["name"],
            "base_stats": base_stats,
            "types": types,
            "move": {
                "name": move_name,
                "power": move_power,
                "type": move_type,
                "effect": move_effect,
            },
        }
    except Exception as e:
        logger.error("pokemon_fetch_error", pokemon=pokemon_name, error=str(e))
        return None
